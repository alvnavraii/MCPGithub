from mcp.client.stdio import stdio_client
from mcp.client.session import ClientSession
from mcp import StdioServerParameters
import asyncio
import json
from typing import Any

def format_commit(commit: dict) -> str:
    """Format a single commit for display"""
    return f"Commit {commit['sha'][:7]}:\n" \
           f"  Message: {commit['message']}\n" \
           f"  Author:  {commit['author']}\n" \
           f"  Date:    {commit['date']}\n" \
           f"  URL:     {commit['url']}\n"

def get_text_content(obj: Any) -> str:
    """Extract text from TextContent object or return string as is"""
    if hasattr(obj, 'text'):
        return obj.text
    return str(obj)

async def main():
    server_params = StdioServerParameters(
        command = "python",
        args = ["server.py"]
    )

    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            print("Conectado al servidor MCP")
            tools_result = await session.list_tools()
            print("\nHerramientas disponibles:")
            list_commits_found = False
            for key, value in tools_result:
                if key == "tools" and value:
                    for tool in value:
                        print(f" - {tool.name}: {tool.description}")
                        if tool.name == "list_commits":
                            list_commits_found = True
                            print("\nLlamando a list_commits para MCPGithub...")
                            result = await session.call_tool("list_commits", {
                                "repository_full_name": "alvnavraii/MCPGithub"
                            })
                            
                            print("\nRespuesta de list_commits:")
                            # Extract and parse the nested JSON response
                            result_dict = {}
                            for key, value in result:
                                result_dict[key] = value
                                
                            if result_dict.get("content"):
                                content = result_dict["content"][0]
                                content_str = get_text_content(content)
                                content_data = json.loads(content_str)
                                
                                if "result" in content_data:
                                    commits = content_data["result"]
                                    print(f"\nEncontrados {len(commits)} commits:\n")
                                    for commit in commits:
                                        print(format_commit(commit))
                                else:
                                    print("No se encontraron commits en la respuesta")
                            else:
                                print("Respuesta vacía del servidor")
                    
            if not list_commits_found:
                print("Tool 'list_commits' not found")

if __name__ == "__main__":
    asyncio.run(main())