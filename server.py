from github import Github, Auth
from git import Repo
import requests
from mcp.server.fastmcp import FastMCP
from pathlib import Path
import sys
from dotenv import load_dotenv
import os

mcp = FastMCP("GitHub Management")

# Global variable for Github client
g = None

def load_environment():
    """Load environment variables from .env file with enhanced debugging"""
    env_path = Path(__file__).parent / '.env'
    print(f"Looking for .env file at: {env_path}", file=sys.stderr)
    
    if not env_path.exists():
        raise ValueError(f".env file not found at {env_path}")
    
    if not os.access(env_path, os.R_OK):
        raise ValueError(f".env file is not readable at {env_path}")
        
    print(f"Found .env file, loading environment variables...", file=sys.stderr)
    
    # Read the file first to verify its contents
    with open(env_path, 'r') as f:
        env_contents = f.read().strip()
        
    if not env_contents:
        raise ValueError(".env file is empty")
    
    # Load the environment variables
    load_dotenv(env_path, override=True)
    
    # Verify that variables were loaded
    token = os.getenv('GITHUB_TOKEN')
    if token:
        print(f"Successfully loaded GITHUB_TOKEN (length: {len(token)})", file=sys.stderr)
    else:
        raise ValueError("GITHUB_TOKEN not loaded from .env file")
        
    return env_path

def verify_token(token):
    headers = {
        'Authorization': f'token {token}',  # Cambiado de 'Bearer' a 'token'
        'Accept': 'application/vnd.github.v3+json'
    }
    response = requests.get('https://api.github.com/user', headers=headers)
    print(f"Response status: {response.status_code}")
    print(f"Response headers: {response.headers}")
    if response.status_code == 200:
        return True, response.json()
    return False, response.status_code

def get_github_config():
    """Get GitHub configuration from environment variables."""
    token = os.getenv('GITHUB_TOKEN')
    if not token:
        print("WARNING: GITHUB_TOKEN not found in environment", file=sys.stderr)
        print("Environment variables available:", file=sys.stderr)
        for key, value in os.environ.items():
            if 'TOKEN' in key or 'GITHUB' in key:
                print(f"  {key}: {'[HIDDEN]' if 'TOKEN' in key else value}", file=sys.stderr)
    
    return {
        'token': token,
        'username': os.getenv('GITHUB_USERNAME', 'alvnavraii'),
        'defaultBranch': os.getenv('GITHUB_DEFAULT_BRANCH', 'master'),
        'repository': os.getenv('GITHUB_REPOSITORY', 'MCPGithub')
    }

# Initialize MCP server
def init_github_client():
    """Initialize the GitHub client with proper error handling"""
    global g
    config = get_github_config()
    token = config.get('token')
    
    if not token:
        raise ValueError("GITHUB_TOKEN environment variable is not set")
    
    # Validate token before initializing Github client
    is_valid, result = verify_token(token)
    if not is_valid:
        raise ValueError(f"Invalid GitHub token. Status code: {result}")
    
    print(f"Token valid. Authenticated as: {result.get('login')}", file=sys.stderr)
    g = Github(auth=Auth.Token(token))
    return g

def get_repository(repository_full_name=None):
    """
    Get a GitHub repository.
    If no repository_full_name is provided, use the default from environment variables.
    Format for repository_full_name: "username/repository"
    """
    try:
        global g
        if g is None:
            init_github_client()
            
        # Si no se proporciona un repositorio, usar el de la configuración por defecto
        if not repository_full_name:
            config = get_github_config()
            username = config.get('username')
            repository = config.get('repository')
            repository_full_name = f"{username}/{repository}"
            
        # Obtener el repositorio especificado
        repo = g.get_repo(repository_full_name)
        return repo, None
    except Exception as e:
        return None, str(e)

@mcp.tool()
def list_repositories():
    try:
        global g
        if g is None:
            init_github_client()
        user = g.get_user()
        repos = user.get_repos()
        repo_list = [{"name": repo.name, "private": repo.private} for repo in repos]
        return {"result": repo_list}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def create_repository(repository_name, private=True):
    try:
        global g
        if g is None:
            init_github_client()
        repo = g.get_user().create_repo(repository_name, private=private)
        return {
            "result": {
                "name": repo.name,
                "private": repo.private,
                "url": repo.html_url
            }
        }
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def delete_repository(repository_name=None, repository_full_name=None):
    """
    Delete a GitHub repository.
    
    Args:
        repository_name: Name of the repository (without username)
        repository_full_name: Full name of the repository (username/repo)
    """
    try:
        global g
        if g is None:
            init_github_client()
            
        # Si se proporciona repository_full_name, usarlo directamente
        if repository_full_name:
            repo, error = get_repository(repository_full_name)
            if error:
                return {"error": error}
            repo.delete()
            return {"result": {"message": f"Repository {repository_full_name} deleted successfully"}}
        
        # Si no hay repository_full_name pero hay repository_name, usar el usuario por defecto
        elif repository_name:
            config = get_github_config()
            username = config.get('username')
            repo, error = get_repository(f"{username}/{repository_name}")
            if error:
                return {"error": error}
            repo.delete()
            return {"result": {"message": f"Repository {repository_name} deleted successfully"}}
        else:
            return {"error": "Either repository_name or repository_full_name must be provided"}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def create_pull_request(repository_full_name, head_branch, base_branch):
    try:
        global g
        if g is None:
            init_github_client()
        repo = g.get_repo(repository_full_name)
        pull_request = repo.create_pull(
            title="Create pull request",
            body="This is a pull request created by the script",
            head=head_branch,
            base=base_branch,
        )
        return {
            "result": {
                "number": pull_request.number,
                "title": pull_request.title,
                "url": pull_request.html_url
            }
        }
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def list_pull_requests(repository_full_name):
    try:
        global g
        if g is None:
            init_github_client()
        repo = g.get_repo(repository_full_name)
        pull_requests = repo.get_pulls(state='open')
        pr_list = [{
            "number": pr.number,
            "title": pr.title,
            "url": pr.html_url,
            "state": pr.state
        } for pr in pull_requests]
        return {"result": pr_list}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def merge_pull_request(repository_full_name, pull_request_number):
    try:
        global g
        if g is None:
            init_github_client()
        repo = g.get_repo(repository_full_name)
        pull_request = repo.get_pull(pull_request_number)
        if pull_request.is_mergeable():
            result = pull_request.merge()
            return {
                "result": {
                    "message": f"Pull request #{pull_request_number} merged successfully",
                    "sha": result.sha
                }
            }
        else:
            return {"error": f"Pull request #{pull_request_number} is not mergeable"}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def list_commits(repository_full_name, branch="master"):
    try:
        global g
        if g is None:
            init_github_client()
        repo = g.get_repo(repository_full_name)
        commits = repo.get_commits(sha=branch)
        commit_list = [{
            "sha": commit.sha,
            "message": commit.commit.message,
            "author": commit.commit.author.name,
            "date": commit.commit.author.date.isoformat(),
            "url": commit.html_url
        } for commit in commits]
        return {"result": commit_list}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def create_issue(repository_full_name, title, body):
    try:
        global g
        if g is None:
            init_github_client()
        repo = g.get_repo(repository_full_name)
        issue = repo.create_issue(title=title, body=body)
        return {
            "result": {
                "number": issue.number,
                "title": issue.title,
                "url": issue.html_url
            }
        }
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def list_branches(repository_full_name):
    try:
        global g
        if g is None:
            init_github_client()
        repo = g.get_repo(repository_full_name)
        branches = [{"name": branch.name} for branch in repo.get_branches()]
        return {"result": branches}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def create_branch(repository_full_name, branch_name, source_branch="master"):
    try:
        global g
        if g is None:
            init_github_client()
        repo = g.get_repo(repository_full_name)
        source = repo.get_branch(source_branch)
        repo.create_git_ref(ref=f"refs/heads/{branch_name}", sha=source.commit.sha)
        return {"result": {"message": f"Branch {branch_name} created from {source_branch}"}}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool("delete_branch")
def force_delete_branch(repository_full_name, branch_name, token):
    try:
        url = f"https://api.github.com/repos/{repository_full_name}/git/refs/heads/{branch_name}"
        headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }
        response = requests.delete(url, headers=headers)
        if response.status_code == 204:
            return {"result": {"message": f"Branch {branch_name} deleted via REST API"}}
        else:
            return {"error": f"Failed to delete branch {branch_name}: {response.status_code} {response.text}"}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def get_repository_info(repository_full_name):
    """
    Get information about a specific GitHub repository.
    
    Args:
        repository_full_name: Full name of the repository in format 'username/repository'
    
    Returns:
        Information about the repository including name, owner, description, etc.
    """
    try:
        repo, error = get_repository(repository_full_name)
        if error:
            return {"error": error}
            
        return {
            "result": {
                "name": repo.name,
                "full_name": repo.full_name,
                "owner": repo.owner.login,
                "description": repo.description,
                "html_url": repo.html_url,
                "default_branch": repo.default_branch,
                "private": repo.private,
                "created_at": repo.created_at.isoformat() if repo.created_at else None,
                "updated_at": repo.updated_at.isoformat() if repo.updated_at else None,
                "stars": repo.stargazers_count,
                "forks": repo.forks_count,
                "language": repo.language
            }
        }
    except Exception as e:
        return {"error": str(e)}

def set_remote_with_token(repo_path, token, usuario, repo_name):
    repo = Repo(repo_path)
    # Si tenemos token, la URL se construye solo con el token
    if token:
        remote_url = f"https://{token}@github.com/{usuario}/{repo_name}.git"
    else:
        remote_url = f"https://github.com/{usuario}/{repo_name}.git"
        
    if 'origin' in [remote.name for remote in repo.remotes]:
        repo.remote('origin').set_url(remote_url)
    else:
        repo.create_remote('origin', remote_url)
    # No imprimimos la URL completa para no exponer el token
    print(f"Remote origin configurado para {usuario}/{repo_name}")

@mcp.tool()
def git_add(repo_path = "."):
    try:
        repo = Repo(repo_path)
        repo.git.add(A=True)
        return {"result": {"message": "Files added to staging area"}}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def git_commit(message = "First Commit", repo_path = "."):
    try:
        from datetime import datetime
        repo = Repo(repo_path)
        if repo.is_dirty(untracked_files=True):
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            commit_message = f"Changes in server ({current_time}): {message}"
            repo.git.commit(m=commit_message)
            return {"result": {"message": f"Committed: {commit_message}"}}
        else:
            return {"error": "No changes to commit"}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def git_push(branch="master", repo_path=".", token=None, usuario=None, repo_name=None, repository_full_name=None):
    """
    Push changes to a remote repository.
    
    Args:
        branch: The branch to push to.
        repo_path: Local path to the repository.
        token: GitHub token for authentication. If not provided, uses the one from the environment.
        usuario: GitHub username. If not provided, uses the one from the environment.
        repo_name: Repository name. If not provided, uses the one from the environment.
        repository_full_name: Full repository name in the format "username/repo". If provided, overrides usuario and repo_name.
    """
    try:
        repo = Repo(repo_path)
        config = get_github_config()
        
        if not token and config:
            token = config.get('token')
            
        # Si se proporciona repository_full_name, extraer usuario y nombre del repo
        if repository_full_name:
            parts = repository_full_name.split('/')
            if len(parts) == 2:
                usuario = parts[0]
                repo_name = parts[1]
            else:
                return {"error": "Invalid repository_full_name format. Should be 'username/repository'"}
        else:
            if not usuario and config:
                usuario = config.get('username')
            if not repo_name and config:
                repo_name = config.get('repository')
        
        if token and repo_name and usuario:
            # Usar la función existente para configurar el remote con el token
            set_remote_with_token(repo_path, token, usuario, repo_name)
            
            repo.git.push('origin', branch)
            return {
                "result": {
                    "message": "Push completado exitosamente",
                    "repository": f"{usuario}/{repo_name}",
                    "branch": branch
                }
            }
        else:
            missing = []
            if not token: missing.append("token")
            if not usuario: missing.append("usuario")
            if not repo_name: missing.append("nombre del repositorio")
            return {"error": f"Faltan parámetros requeridos: {', '.join(missing)}"}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    try:
        # Load environment variables explicitly
        env_path = load_environment()
        print(f"Loading environment from: {env_path}", file=sys.stderr)
        
        init_github_client()
        print("Starting MCP server...", file=sys.stderr)
        mcp.run(transport="stdio")
    except Exception as e:
        print(f"Fatal error: {str(e)}", file=sys.stderr)
        sys.exit(1)
