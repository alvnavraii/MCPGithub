# MCPGithub 🚀

## Description 📝
MCPGithub is a GitHub repository management tool integrated with the Model Context Protocol (MCP). This project allows you to interact with the GitHub API efficiently and securely, facilitating repository, branch, and pull request management.

## Features ✨
- 📦 Repository management (create, list, delete)
- 🌿 Branch control (create, list, delete)
- 🔄 Pull Request handling
- 🔐 Secure token authentication
- ⚡ MCP integration for a smooth experience

## Prerequisites 📋
- Python 3.x
- GitHub account
- GitHub token with necessary permissions
- Configured environment variables

## Installation 🛠️
1. Clone the repository:
```bash
git clone https://github.com/alvnavraii/MCPGithub.git
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure your GitHub token as an environment variable:
```bash
export GITHUB_TOKEN='your_token_here'
```

## Usage 💻
The project runs as an MCP server and provides the following tools:

### Repository Management
- `list_repositories()` 📚: Lists all repositories owned by the authenticated user
- `create_repository(repository_name, private=True)` ➕: Creates a new repository with optional privacy setting
- `delete_repository(repository_name)` ❌: Deletes an existing repository

### Branch Management
- `list_branches(repository_full_name)` 🌳: Lists all branches in a specified repository
- `create_branch(repository_full_name, branch_name, source_branch="master")` 🌱: Creates a new branch from a source branch
- `delete_branch(repository_full_name, branch_name, token)` 🗑️: Force deletes a branch from the repository

### Pull Request Management
- `create_pull_request(repository_full_name, head_branch, base_branch)` 🔄: Creates a new pull request
- `list_pull_requests(repository_full_name)` 📋: Lists all open pull requests in a repository
- `merge_pull_request(repository_full_name, pull_request_number)` 🔀: Merges a pull request if it's mergeable

### Commit Management
- `list_commits(repository_full_name, branch="master")` 📜: Lists all commits in a specified branch

### Issue Management
- `create_issue(repository_full_name, title, body)` 📝: Creates a new issue in the specified repository

### Git Operations
- `git_add(repo_path=".")` ➕: Stages all changes in the repository
- `git_commit(repo_path=".", message="First Commit")` ✔️: Commits staged changes with a message
- `git_push(branch="test", repo_path=".", token=None, usuario=None, repo_name=None)` ⬆️: Pushes commits to remote repository

## MCP Server Configuration 🔧

### Claude Desktop Configuration 🤖

1. Locate the Claude configuration file:
```bash
~/.config/Claude/claude_desktop_config.json
```

2. Add the MCP server configuration in the `mcpServers` section:
```json
{
  "mcpServers": {
    "GitHubManagement": {
      "command": "/path/to/your/venv/python",
      "args": [
        "/path/to/your/project/MCPGithub/server.py"
      ],
      "defaultBranch": "master",
      "username": "your-github-username",
      "token": "your-github-token"
    }
  }
}
```

### Windsurf Desktop Configuration 🌊

1. Locate the Windsurf configuration file:
```bash
~/.config/Windsurf/windsurf_desktop_config.json
```

2. Add the MCP server configuration in the `mcpServers` section:
```json
{
  "mcpServers": {
    "GitHubManagement": {
      "command": "/path/to/your/venv/python",
      "args": [
        "/path/to/your/project/MCPGithub/server.py"
      ],
      "defaultBranch": "master",
      "username": "your-github-username",
      "token": "your-github-token"
    }
  }
}
```

### Important Configuration Notes ⚠️

- Make sure to replace `/path/to/your/venv/python` with the actual path to your Python virtual environment
- Replace `/path/to/your/project/MCPGithub/server.py` with the actual path to the server.py file
- Replace `your-github-username` with your GitHub username
- Replace `your-github-token` with your GitHub personal access token
- The `defaultBranch` can be modified according to your preferences (defaults to "master")

### Configuration Verification ✅

To verify that the configuration has been set up correctly, you can use the `mcp_config_reader.py` script included in this project:

```bash
python mcp_config_reader.py
```

This script will show you the current configurations for both Claude and Windsurf.

## Security 🔒
- Tokens are handled through environment variables
- Secure authentication implementation
- Permission and access validation

## Contributing 🤝
Contributions are welcome. Please make sure to:
1. Fork the project
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License 📄
This project is under the MIT License. See the `LICENSE` file for more details.

## Author ✍️
- **Alvaro Navarro** - [@alvnavraii](https://github.com/alvnavraii)

## Acknowledgments 💎
- GitHub API
- MCP Framework
- All contributors