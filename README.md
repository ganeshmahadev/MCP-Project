# MCP Chatbot

A Streamlit-based chatbot that uses Groq LLMs (via LangChain) to communicate with multiple MCP servers as tools. The agent chooses which MCP server/tool to use based on your input, and displays which servers were used for each response.

## Features
- Chat UI powered by Streamlit
- LLM agent (Groq + LangChain) that routes queries to MCP servers
- Supports both HTTP and command-line MCP servers
- Displays which MCP server/tool was used for each response

## Prerequisites
- Python 3.8+
- [Groq API key](https://console.groq.com/)
- MCP servers (HTTP or command-line) you want to connect to

## Installation

1. **Clone the repository** (if needed):
   ```bash
   git clone <your-repo-url>
   cd MCP\ Project
   ```

2. **Create and activate a virtual environment (recommended):**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your Groq API key:**
   - Create a `.env` file in the project root:
     ```env
     GROQ_API_KEY=your_groq_api_key_here
     ```

5. **Configure MCP servers:**
   - Edit `mcpservers.json` to add your MCP server endpoints (see the provided example in the repo).

## Running the Chatbot

Start your MCP servers (HTTP or command-line) as needed, then run:

```bash
streamlit run chatbot.py
```

Open the provided local URL in your browser to chat!

## MCP Server Configuration Example

```
{
  "mcpServers": {
    "playwright": {
      "url": "http://localhost:8931/mcp"
    },
    "duckduckgo-search": {
      "command": "npx",
      "args": ["-y", "duckduckgo-mcp-server"]
    },
    "airbnb": {
      "command": "npx",
      "args": ["-y", "@openbnb/mcp-server-airbnb"]
    }
  }
}
```

- For HTTP servers, provide a `url`.
- For command-line servers, provide a `command` and `args` array.

## Troubleshooting
- **Connection refused**: Make sure your MCP server is running and accessible at the configured URL/port.
- **Stub responses**: If you see stub messages, the tool is not fully implemented or the server is not running.
- **Groq API errors**: Check your `.env` file and ensure your API key is correct.
- **Agent doesn't use a tool**: The LLM may decide not to use a tool if it doesn't think it's relevant to your query.

## License
MIT 