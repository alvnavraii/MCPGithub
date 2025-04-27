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

## Environment Variables Configuration (.env) ⚙️
This project uses a `.env` file to manage sensitive environment variables, such as the GitHub token. The server validates the existence, readability, and content of the `.env` file before starting. If the file is missing, unreadable, empty, or the `GITHUB_TOKEN` is missing, the server will display a clear error message and will not start.

### Example of a `.env` file:
```env
GITHUB_TOKEN=your_personal_github_token
```
Place the `.env` file in the root of the project (`MCPGithub/`).

## Installation 🛠️
1. Clone the repository:
```bash
git clone https://github.com/alvnavraii/MCPGithub.git
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root of the project with the following content:
```env
GITHUB_TOKEN=your_personal_github_token
```

> **Note:** You no longer need to manually export the `GITHUB_TOKEN` environment variable.

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

## Troubleshooting and Configuration Validation ⚠️
When starting the server, the following validations are performed:
- 🗂️ Checks that the `.env` file exists in the project root.
- 👁️ Ensures the `.env` file is readable.
- 📄 Ensures the `.env` file is not empty.
- 🛡️ Validates that the `GITHUB_TOKEN` variable is present and not empty.

### Common Error Messages
- ❗ `.env file not found at ...`: The `.env` file does not exist at the expected path.
- ❗ `.env file is not readable at ...`: The file exists but does not have read permissions.
- ❗ `.env file is empty`: The file exists but is empty.
- ❗ `GITHUB_TOKEN not loaded from .env file`: The `GITHUB_TOKEN` variable is missing or empty.

If you encounter any of these errors, check the existence, permissions, and content of your `.env` file.

## Startup and Validation Flow ⚙️
When running the server, it first loads and validates the `.env` file. If everything is correct, the GitHub client is initialized and the MCP server starts. If any validation error occurs, the server displays a descriptive message and will not continue execution.

## MCP Server Configuration 🔧

### Claude Desktop Configuration 🤖

1. Locate the Claude configuration file:
```bash
~/.config/Claude/claude_desktop_config.json
```
2. Add the MCP server configuration in the `mcpServers` section (only command and args are required):
```json
{
  "mcpServers": {
    "GitHubManagement": {
      "command": "/path/to/your/venv/python",
      "args": [
        "/path/to/your/project/MCPGithub/server.py"
      ]
    }
  }
}
```
> **Note:** All sensitive data (username, token, defaultBranch, etc.) is now managed exclusively via the `.env` file in your project root. Do not include these fields in the JSON configuration.

### Windsurf Desktop Configuration 🌊

1. Locate the Windsurf configuration file:
```bash
~/.config/Windsurf/windsurf_desktop_config.json
```
2. Add the MCP server configuration in the `mcpServers` section (only command and args are required):
```json
{
  "mcpServers": {
    "GitHubManagement": {
      "command": "/path/to/your/venv/python",
      "args": [
        "/path/to/your/project/MCPGithub/server.py"
      ]
    }
  }
}
```
> **Note:** All credentials and configuration details are handled via the `.env` file. The JSON should only specify how to launch the MCP server.

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
- **Rafael Álvarez Navarrete** - [@alvnavraii](https://github.com/alvnavraii)

## Acknowledgments 💎
- GitHub API
- MCP Framework
- All contributors