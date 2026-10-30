# 📋 TaskPilot

A conversational AI-powered task management agent built with **LangGraph**, **LangChain**, **Groq**, **SQLite**, and **Streamlit**.

TaskPilot allows users to manage tasks using natural-language conversations. Instead of interacting with traditional forms or CRUD interfaces, users can ask the agent to add, view, search, update, complete, and delete tasks.

The application uses **LLM tool calling**, **LangGraph-based agent orchestration**, **persistent checkpoint memory**, **runtime context injection**, and **user-scoped database operations** to provide persistent conversations and isolated task management for multiple users.

---

## ✨ Features

* 💬 Natural-language task management through a conversational interface
* ➕ Add new tasks with optional descriptions
* 📋 View all tasks belonging to the current user
* 🔎 Search tasks by title or description
* ✏️ Update task titles, descriptions, and status
* ✅ Mark tasks as completed or reopen them
* 🗑️ Delete tasks using task IDs or natural-language references
* 🧠 Persistent conversation memory using LangGraph checkpointing
* 💾 SQLite-backed task and checkpoint persistence
* 🧵 Thread-based conversation isolation
* 👥 User-scoped task isolation
* 🔐 Runtime context injection keeps `user_id` hidden from the LLM tool schema
* 🔧 Multi-step tool execution for requests such as finding a task before updating or deleting it
* 🎨 Streamlit chat interface
* 🖥️ Terminal CLI interface for development and testing
* 🕒 Task timestamps displayed in Indian Standard Time (IST)

---

## 🧠 How It Works

A user sends a natural-language request such as:

> Mark my Docker task as completed.

The request flows through the application as follows:

```text
User
  │
  ▼
Streamlit Chat Interface
  │
  ▼
LangGraph StateGraph
  │
  ▼
Agent Node
  │
  ▼
Groq LLM
(openai/gpt-oss-120b)
  │
  ├──────────── No Tool Call ────────────► Final Response
  │
  ▼
Conditional Routing
  │
  ▼
ToolNode
  │
  ▼
Todo Tools
  │
  ├── Add Task
  ├── View Tasks
  ├── Search Tasks
  ├── Update Task
  └── Delete Task
  │
  ▼
User-Scoped SQLite Database
  │
  ▼
Tool Result
  │
  └──────────────────────────────► Agent Node
                                      │
                                      ▼
                                  Final Response
```

LangGraph persists conversation state through a SQLite-backed checkpointer.

```text
Conversation
     │
     ▼
Thread ID
     │
     ▼
LangGraph SQLite Checkpointer
     │
     ▼
Persistent Conversation State
```

Each application user receives a separate runtime context and conversation thread.

```text
User
 │
 ├── user_id
 │      │
 │      ▼
 │   TodoContext
 │      │
 │      ▼
 │   ToolRuntime
 │      │
 │      ▼
 │   User-Scoped Database Operations
 │
 └── thread_id
        │
        ▼
   LangGraph Checkpointer
        │
        ▼
   Persistent Conversation History
```

This separates **task ownership** from **conversation memory**.

---

## 🛠️ Tech Stack

| Technology                    | Purpose                                                         |
| ----------------------------- | --------------------------------------------------------------- |
| Python                        | Core application language                                       |
| LangGraph                     | Agent workflow orchestration and checkpointing                  |
| LangChain                     | Tool definitions, message abstractions, and runtime integration |
| Groq                          | LLM inference API                                               |
| openai/gpt-oss-120b           | Language model used by the agent                                |
| SQLite                        | Persistent task storage                                         |
| LangGraph SQLite Checkpointer | Persistent conversation state                                   |
| Streamlit                     | Web-based conversational UI                                     |
| python-dotenv                 | Environment variable management                                 |

---

## 🤖 Agent Workflow

The agent uses a cyclic LangGraph workflow:

```text
START
  │
  ▼
AGENT
  │
  ▼
Does the LLM request a tool?
  │
  ├── NO ─────────────► END
  │
  └── YES
        │
        ▼
      TOOLS
        │
        ▼
      AGENT
        │
        └── Repeat until no tool call remains
```

The agent can perform multi-step operations automatically.

For example:

```text
User:
"Mark my Docker task as completed."

Agent:
Search Docker task
      │
      ▼
Receive matching task ID
      │
      ▼
Update task status
      │
      ▼
Generate final response
```

---

## 🔮 Future Improvements

Potential improvements include:

* Real authentication and authorization
* Multiple conversations per user
* New conversation and conversation history management
* Human-in-the-loop confirmation for destructive actions
* Task deadlines and reminders
* Task priorities, tags, and categories
* Structured final responses
* LLM response-length safeguards
* Streaming responses
* Automated unit and integration testing
* LangSmith tracing, observability, and evaluation
* PostgreSQL-backed task persistence
* Production deployment architecture

---