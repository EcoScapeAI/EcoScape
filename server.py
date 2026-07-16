import os
from fastapi import FastAPI
from fastapi_mcp import FastApiMCP

# 1. Initialize standard FastAPI
app = FastAPI()

# 2. Initialize and link the MCP server framework
mcp = FastApiMCP(app, title="EcoScape MCP Server", version="1.0.0")

# 3. Define your AI tool simply using standard decorators
@mcp.tool(name="fetch_cloud_data", description="A tool that returns environmental cloud data.")
async def fetch_cloud_data(query: str) -> str:
    """Processes environmental inquiries or data lookups."""
    # You can customize your internal logic here anytime!
    return f"EcoScapeAI successfully processed your cloud query: '{query}'"

# 4. Mount the endpoints automatically
mcp.mount()

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("server:app", host="0.0.0.0", port=port)
