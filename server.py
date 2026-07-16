import os
from fastapi import FastAPI
from mcp.server.fastapi import FastApiServerOptions, create_server_application
from mcp.server.models import InitializationOptions
from mcp.server import Server

# Initialize standard MCP server
mcp_server = Server("EcoScape MCP Server")

# Explicit tool registration using the official standard decorator
@mcp_server.list_tools()
async def handle_list_tools():
    return [
        {
            "name": "fetch_cloud_data",
            "description": "A tool that returns environmental cloud data.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "What to look up"}
                },
                "required": ["query"]
            }
        }
    ]

@mcp_server.call_tool()
async def handle_call_tool(name: str, arguments: dict):
    if name == "fetch_cloud_data":
        query = arguments.get("query", "")
        return [{
            "type": "text",
            "text": f"EcoScapeAI successfully processed your cloud query: '{query}'"
        }]
    raise ValueError(f"Unknown tool: {name}")

options = FastApiServerOptions(
    server_options=InitializationOptions(
        server_name="ecoscape-server",
        server_version="1.0.0",
        capabilities=mcp_server.get_capabilities()
    )
)

# Standard application creation
app = create_server_application(mcp_server, options)

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("server:app", host="0.0.0.0", port=port)
