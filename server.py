import os
from fastapi import FastAPI
from fastapi_mcp import FastApiMCP

# Initialize standard FastAPI app
app = FastAPI()

# Clean initialization 
mcp = FastApiMCP(app)

# Fixed decorator attribute name from tool to tools
@mcp.tools(name="fetch_cloud_data", description="A tool that returns environmental cloud data.")
async def fetch_cloud_data(query: str) -> str:
    """Processes environmental inquiries or data lookups."""
    return f"EcoScapeAI successfully processed your cloud query: '{query}'"

# Mount the MCP endpoints onto FastAPI automatically
mcp.mount()

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("server:app", host="0.0.0.0", port=port)
