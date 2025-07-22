import streamlit as st
import json
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool
from dotenv import load_dotenv
import os
import requests
import subprocess
load_dotenv()

# Load MCP server config
def load_mcp_config(path='mcpservers.json'):
    with open(path, 'r') as f:
        return json.load(f)

# Wrap each MCP server as a LangChain Tool
def make_mcp_tools(config):
    tools = []
    servers = config.get('mcpServers', {})
    for name, info in servers.items():
        if 'url' in info:
            def make_tool(url, name):
                def _call(input):
                    try:
                        resp = requests.post(url, json={"input": input})
                        return resp.json().get("output", str(resp.text))
                    except Exception as e:
                        return f"Error calling {name}: {e}"
                return Tool(
                    name=name,
                    func=_call,
                    description=f"Call the {name} MCP server at {url}"
                )
            tools.append(make_tool(info['url'], name))
        elif 'command' in info and 'args' in info:
            def make_cmd_tool(cmd, args, name):
                def _call(input):
                    try:
                        # Pass input as last arg or via stdin
                        full_cmd = [cmd] + args + [input]
                        result = subprocess.run(full_cmd, capture_output=True, text=True, input=input)
                        return result.stdout.strip() or result.stderr.strip()
                    except Exception as e:
                        return f"Error calling {name}: {e}"
                return Tool(
                    name=name,
                    func=_call,
                    description=f"Call the {name} MCP server via command: {cmd} {' '.join(args)}"
                )
            tools.append(make_cmd_tool(info['command'], info['args'], name))
        else:
            def _call(input, name=name):
                return f"Stub: would call {name} with input: {input}"
            tools.append(Tool(
                name=name,
                func=_call,
                description=f"Stub for {name} MCP server"
            ))
    return tools

# Set up Groq LLM (load from .env)
openai_api_key = os.getenv('OPENAI_API_KEY', 'OPENAI_API_KEY')
llm = ChatOpenAI(api_key=openai_api_key, model_name="gpt-4o")

# Streamlit UI
st.title("MCP Chatbot (Agent Mode)")

mcp_config = load_mcp_config()
tools = make_mcp_tools(mcp_config)

if not tools:
    st.warning("No MCP servers configured.")

if 'history' not in st.session_state:
    st.session_state['history'] = []

user_input = st.text_input("You:", "")

# Set up LangChain agent
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True
)

if st.button("Send") and user_input:
    # Run agent and capture tool usage
    try:
        response = agent.run(user_input)
        # Try to extract tool usage from agent's intermediate steps (if available)
        used_tools = [tool.name for tool in tools if tool.name.lower() in response.lower()]
    except Exception as e:
        response = f"Agent error: {e}"
        used_tools = []
    st.session_state['history'].append((user_input, response, used_tools))

# Display chat history
for user_msg, mcp_msg, used_tools in st.session_state['history']:
    st.markdown(f"**You:** {user_msg}")
    st.markdown(f"**MCP:** {mcp_msg}")
    st.markdown(f"_MCP servers used: {', '.join(used_tools) if used_tools else 'None'}_") 