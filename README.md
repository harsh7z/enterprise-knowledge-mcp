# Enterprise Knowledge Assistant MCP Server

A Python-based Model Context Protocol (MCP) server using **FastMCP** that connects an internal knowledge base to Claude or other MCP-capable LLMs. This allows employees or internal tools to search, retrieve, and ask questions about internal documents in a structured and auditable manner.

---

## Features

* **Search documents**: Search internal knowledge base by keywords or questions.
* **Retrieve document content**: Get the full content of a document by ID.
* **Ask knowledge assistant**: Ask questions to an internal QA endpoint, with a fallback to search results.
* **Async HTTP calls**: Uses `httpx` for non-blocking requests.
* **FastMCP tool decorators**: Each function is a separate MCP tool available to LLMs.

---

### Example Tool Calls

* **Search documents**:

```python
search_documents("expense reimbursement policy")
```

* **Retrieve document content**:

```python
get_document_content("HR-00123")
```

* **Ask knowledge assistant**:

```python
ask_knowledge_base("How do I request vacation days?")
```

Each tool is decorated with `@mcp.tool()` and is directly callable by the connected model.

---

