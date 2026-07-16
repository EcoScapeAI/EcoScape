import os
import uvicorn
from fastapi import FastAPI, HTTPException, Security, Depends
from fastapi.security.api_key import APIKeyHeader
from mcp.server import Server
from mcp.server.sse import SseServerTransport

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

# Create the standard FastAPI app
app = FastAPI(dependencies=[Depends(verify_api_key)])
sse_transport = SseServerTransport(mcp_server)

@app.get("/sse")
async def handle_sse_endpoint():
    return await sse_transport.handle_sse()

@app.post("/messages")
async def handle_messages_endpoint():
    return await sse_transport.handle_messages()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("server:app", host="0.0.0.0", port=port)
