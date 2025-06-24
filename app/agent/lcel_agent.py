# app/agent/lcel_agent.py

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain.tools import tool
from app.agent.tools.search_for_rooms import search_rooms
from app.db.session import get_db
from app.core.config import settings
from typing import Optional

# Choose LLM backend dynamically
if settings.LLM_MODEL.startswith("gpt"):
    from langchain_openai import ChatOpenAI

    llm = ChatOpenAI(model=settings.LLM_MODEL, temperature=settings.LLM_TEMPERATURE)
elif settings.LLM_MODEL.startswith("gemini"):
    from langchain_google_genai import ChatGoogleGenerativeAI

    llm = ChatGoogleGenerativeAI(
        model=settings.LLM_MODEL,
        temperature=settings.LLM_TEMPERATURE,
        google_api_key=settings.GOOGLE_API_KEY,
    )
else:
    raise ValueError(f"Unsupported LLM model: {settings.LLM_MODEL}")


# --- Prompt Template ---
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful hotel assistant."),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)


# --- Agent Builder ---
def build_hotel_agent():
    tools = [search_rooms]
    agent = create_openai_functions_agent(llm=llm, tools=tools, prompt=prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=True)
