from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Test")

if __name__ == "__main__":
    mcp.run(transport="stdio")
