from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("enterprise_knowledge")

# Constants
KB_API_BASE = "https://your-knowledge-api.company.com/v1"
USER_AGENT = "enterprise-assistant/1.0"

# Utility: Request wrapper
async def make_kb_request(endpoint: str, params: dict[str, Any] | None = None) -> dict[str, Any] | None:
    """Make a request to the enterprise knowledge API with error handling."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{KB_API_BASE}/{endpoint}", params=params, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Request failed: {e}")
            return None


# Tool: Search documents 
@mcp.tool()
async def search_documents(query: str, limit: int = 5) -> str:
    """Search internal documents related to the query.

    Args:
        query: Search term or question to find in internal docs.
        limit: Max number of results to return.
    """
    data = await make_kb_request("search", {"q": query, "limit": limit})

    if not data or "results" not in data:
        return "No relevant documents found or unable to reach the knowledge API."

    docs = []
    for doc in data["results"]:
        docs.append(f"""
Title: {doc.get('title', 'Untitled')}
Source: {doc.get('source', 'Unknown')}
Summary: {doc.get('snippet', 'No summary available')}
URL: {doc.get('url', 'N/A')}
        """)
    return "\n---\n".join(docs)


# Tool: Retrieve full document
@mcp.tool()
async def get_document_content(doc_id: str) -> str:
    """Retrieve the full text of a document by ID.

    Args:
        doc_id: Unique document identifier.
    """
    data = await make_kb_request(f"documents/{doc_id}")

    if not data or "content" not in data:
        return "Document not found or unavailable."

    title = data.get("title", "Untitled")
    author = data.get("author", "Unknown")
    updated = data.get("updated_at", "Unknown")
    content = data.get("content", "")

    return f"""
Title: {title}
Author: {author}
Last Updated: {updated}

Content:
{content[:2000]}...
    """


# Tool: Ask knowledge assistant
@mcp.tool()
async def ask_knowledge_base(question: str) -> str:
    """Ask the internal knowledge assistant a question.

    This uses a company-internal QA API or search fallback.
    """
    data = await make_kb_request("ask", {"q": question})

    if data and "answer" in data:
        return f"Answer: {data['answer']}"
    else:
        # fallback to search
        docs = await search_documents(question)
        return f"No direct answer found. Here are related documents:\n{docs}"


# Run server
def main():
    mcp.run(transport='stdio')


if __name__ == "__main__":
    main()
