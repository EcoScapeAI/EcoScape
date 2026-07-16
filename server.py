import os
from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.security.api_key import APIKeyHeader
from mcp.server.fastapi import FastApiServerOptions, create_server_application
from mcp.server.models import InitializationOptions
from mcp.server import Server

# Secure server with an API Key
API_KEY = os.getenv("MCP_API_KEY", "change-this-in-production")
api_key_header = APIKeyHeader(name="X-MCP-API-Key", auto_error=False)

def verify_api_key(header_value: str = Security(api_key_header)):
    if not header_value or header_value != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid or missing API Key")
    return header_value

# Define MCP Server instance
mcp_server = Server("my-cloud-mcp-server")

@mcp_server.list_tools()
async def handle_list_tools():
    return [
        {
            "name": "fetch_cloud_data",
            "description": "A template tool that returns cloud data.",
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
            "text": f"Successfully processed your cloud query: '{query}'"
        }]
    raise ValueError(f"Unknown tool: {name}")

options = FastApiServerOptions(
    server_options=InitializationOptions(
        server_name="my-cloud-mcp-server",
        server_version="1.0.0",
        capabilities=mcp_server.get_capabilities()
    )
)

# Crucial fix: The application instance variable name is app
app = create_server_application(
    mcp_server, 
    options,
    dependencies=[Depends(verify_api_key)]
)

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    # Corrected target variable to app instead of server
    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=False)

