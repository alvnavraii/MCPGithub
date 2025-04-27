from mcp.client.stdio import stdio_client
from mcp.client.session import ClientSession
from mcp import StdioServerParameters
import asyncio

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
            print("Herramientas disponibles:")
            list_commits_found = False
            for key, value in tools_result:
                if key == "tools" and value:
                    for tool in value:
                        print(f" - {tool.name}: {tool.description}")
                        if tool.name == "list_commits":
                            list_commits_found = True
                            await session.call_tool("list_commits", {"repository_full_name": "alvnavraii/MCPGithub"})
                    
            if not list_commits_found:
                print("Tool 'list_commits' not found")

if __name__ == "__main__":
    asyncio.run(main())