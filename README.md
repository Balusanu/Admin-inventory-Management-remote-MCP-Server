# 📦 Admin Inventory Management – Remote MCP Server

A production-ready **Remote MCP (Model Context Protocol) Server** built using **FastMCP**, enabling Claude Desktop to manage office inventory using natural language.

🌐 **Live Endpoint:**
[https://admin-inventory-management-remote-mcp.onrender.com/](https://admin-inventory-management-remote-mcp.onrender.com/)

---

# 🚀 Project Overview

This project implements an AI-powered **Office Admin Inventory Management System** using the Model Context Protocol (MCP).

It allows Claude Desktop to:

* Add inventory items
* Issue stock
* Check stock availability
* List all items
* Trigger low-stock alerts

All operations are executed via structured tool calls and backed by a persistent database.

---

# 🧠 Architecture

## 🔹 Local Architecture

```
Claude Desktop
      ↓ (stdio MCP)
FastMCP Server
      ↓
SQLite Database
```

## 🔹 Remote Architecture (Production)

```
Claude Desktop
      ↓ (HTTPS MCP Protocol)
Remote FastMCP Server (Render)
      ↓
SQLite Database
```

---

# 🛠️ Tech Stack

* **FastMCP** – MCP server implementation
* **SQLAlchemy** – ORM for database interaction
* **SQLite** – Persistent storage
* **Docker** – Containerization
* **Render** – Cloud deployment
* **Claude Desktop** – LLM client

---

# ⚙️ How It Was Built

## 1️⃣ MCP Tool-Based Server

Inventory operations are exposed as structured tools:

```python
@mcp.tool()
def add_item(name: str, category: str, quantity: int, min_threshold: int):
```

Each tool:

* Validates inputs
* Executes deterministic business logic
* Updates the database
* Returns structured output

---

## 2️⃣ Database Layer

Built using SQLAlchemy ORM.

### Item Model Fields:

* `name`
* `category`
* `quantity`
* `min_threshold`

This ensures persistent and reliable inventory tracking.

---

## 3️⃣ HTTP Transport Mode

Converted from local stdio transport to HTTP transport for remote deployment:

```python
mcp.run(
    transport="http",
    host="0.0.0.0",
    port=port
)
```

This allows Claude to communicate securely over HTTPS.

---

## 4️⃣ Dockerized Deployment

Dockerfile used for containerization:

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "server.py"]
```

Deployed as a Web Service on Render.

---

# 🌐 Live Endpoint Behavior

Opening the URL in a browser may show:

```
Not Found
```

This is expected behavior.

MCP servers expose protocol endpoints — not web UI routes.

---

# 🔗 How to Configure in Claude Desktop

## Step 1: Open Claude Settings

Go to:

```
Settings → Developer → MCP Servers
```

---

## Step 2: Edit Claude Configuration File

### Windows:

```
%APPDATA%\Claude\claude_desktop_config.json
```

### Mac:

```
~/Library/Application Support/Claude/claude_desktop_config.json
```

---

## Step 3: Add Remote MCP Server Configuration

```json
{
  "mcpServers": {
    "admin-inventory-remote": {
      "transport": "http",
      "url": "https://admin-inventory-management-remote-mcp.onrender.com"
    }
  }
}
```

---

## Step 4: Restart Claude Desktop

Claude will automatically:

* Discover available tools
* Enable natural language inventory management

---

# 🧪 Example Usage in Claude

You can now say:

* “Add 200 ball pens in Stationery category with threshold 40.”
* “Issue 30 ball pens.”
* “Check stock of printer paper.”
* “List all items in inventory.”

Claude will:

1. Interpret intent
2. Select appropriate MCP tool
3. Send structured arguments
4. Execute backend logic
5. Return updated inventory status

---

# 🎯 Key Design Principles

## 🔹 Separation of Concerns

* LLM handles reasoning
* MCP handles structured execution
* Database ensures persistence

## 🔹 Deterministic Backend

The LLM does not directly manipulate the database.
All operations pass through validated business logic.

## 🔹 Secure Protocol Communication

Claude communicates with the server using MCP over HTTPS.

