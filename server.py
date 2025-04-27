# Small edit for demo: Change tracked by Cascade AI
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
        g.get_user().create_repo(repository_name, private=private)
        print(f"Repository {repository_name} created")
    except Exception as e:
        print(f"Repository {repository_name} already exists")

@mcp.tool()
def delete_repository(repository_name):
    try:
        global g
        if g is None:
            init_github_client()
        user = g.get_user()
        repo = user.get_repo(repository_name)
        repo.delete()
        print(f"Repository {repository_name} deleted")
    except Exception as e:
        print(f"Repository {repository_name} not found or not accessible: {e}")

@mcp.tool()
def create_pull_request(repository_full_name, head_branch, base_branch):
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
    print(f"Pull request created: {pull_request.html_url}")

@mcp.tool()
def list_pull_requests(repository_full_name):
    global g
    if g is None:
        init_github_client()
    repo = g.get_repo(repository_full_name)
    pull_requests = repo.get_pulls(state='open')
    for pr in pull_requests:
        print(f"PR #{pr.number}: {pr.title} - {pr.html_url}")

@mcp.tool()
def merge_pull_request(repository_full_name, pull_request_number):
    global g
    if g is None:
        init_github_client()
    repo = g.get_repo(repository_full_name)
    pull_request = repo.get_pull(pull_request_number)
    if pull_request.is_mergeable():
        pull_request.merge()
        print(f"Pull request #{pull_request_number} merged")
    else:
        print(f"Pull request #{pull_request_number} is not mergeable")

@mcp.tool()
def list_commits(repository_full_name, branch="master"):
    global g
    if g is None:
        init_github_client()
    repo = g.get_repo(repository_full_name)
    commits = repo.get_commits(sha=branch)
    for commit in commits:
        print(f"Commit: {commit.sha} - {commit.commit.message}")

@mcp.tool()
def create_issue(repository_full_name, title, body):
    global g
    if g is None:
        init_github_client()
    repo = g.get_repo(repository_full_name)
    issue = repo.create_issue(title=title, body=body)
    print(f"Issue created: {issue.html_url}")

@mcp.tool()
def list_branches(repository_full_name):
    global g
    if g is None:
        init_github_client()
    repo = g.get_repo(repository_full_name)
    for branch in repo.get_branches():
        print(branch.name)

@mcp.tool()
def create_branch(repository_full_name, branch_name, source_branch="master"):
    global g
    if g is None:
        init_github_client()
    repo = g.get_repo(repository_full_name)
    source = repo.get_branch(source_branch)
    repo.create_git_ref(ref=f"refs/heads/{branch_name}", sha=source.commit.sha)
    print(f"Branch {branch_name} created from {source_branch}")

@mcp.tool("delete_branch")
def force_delete_branch(repository_full_name, branch_name, token):
    url = f"https://api.github.com/repos/{repository_full_name}/git/refs/heads/{branch_name}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.delete(url, headers=headers)
    if response.status_code == 204:
        print(f"Branch {branch_name} deleted via REST API")
    else:
        print(f"Failed to delete branch {branch_name}: {response.status_code} {response.text}")

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
    repo = Repo(repo_path)
    repo.git.add(A=True)
    print("Files added to staging area")

# Improved commit function with better logging and timestamp
@mcp.tool()
def git_commit(message = "First Commit", repo_path = "."):
    try:
        from datetime import datetime
        repo = Repo(repo_path)
        if repo.is_dirty(untracked_files=True):
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            commit_message = f"Changes in server ({current_time}): {message}"
            repo.git.commit(m=commit_message)
            print(f"Successfully committed: {commit_message}")
        else:
            print("No changes to commit. Working directory is clean.")
    except Exception as e:
        print(f"Error during commit: {str(e)}")
        raise

@mcp.tool()
def git_push(branch="master", repo_path=".", token=None, usuario=None, repo_name=None):
    try:
        repo = Repo(repo_path)
        config = get_github_config()
        
        if not token and config:
            token = config.get('token')
        if not usuario and config:
            usuario = config.get('username')
        
        if token and repo_name and usuario:
            # Usar la función existente para configurar el remote con el token
            set_remote_with_token(repo_path, token, usuario, repo_name)
            
            print(f"Intentando push a {repo_name}...")
            repo.git.push('origin', branch)
            print("Push completado exitosamente")
            
        else:
            missing = []
            if not token: missing.append("token")
            if not usuario: missing.append("usuario")
            if not repo_name: missing.append("nombre del repositorio")
            raise Exception(f"Faltan parámetros requeridos: {', '.join(missing)}")
    except Exception as e:
        print(f"Error durante el push: {str(e)}")
        raise

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
