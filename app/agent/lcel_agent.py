# app/agent/lcel_agent.py

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_openai_functions_agent, AgentExecutor
from app.agent.tools.search_for_rooms import search_rooms
from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)

# --- Prompt Template ---
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a helpful hotel assistant. 
        
When users ask about locations, use these guidelines:
- For Carpathians/Carpathian region: use "Carpathian Mountains"
- For Kyiv/Kiev: use "Kyiv" 
- For Odessa: use "Odesa"
- For exact city names, use the exact spelling
- If unsure about exact location name, set location=None and let semantic search handle it

Available locations include: Kyiv, Odesa, Lviv, Kharkiv, Zakarpattia, Dnipro, Berdyansk, Chernivtsi, Carpathian Mountains, Poltava.

Always be helpful and provide detailed information about the rooms found.""",
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)


# --- Agent Builder ---
def build_hotel_agent():
    """Build hotel agent with fresh LLM instance."""
    # Create a fresh LLM instance with current settings
    llm = ChatOpenAI(model=settings.LLM_MODEL, temperature=settings.LLM_TEMPERATURE)

    tools = [search_rooms]
    agent = create_openai_functions_agent(llm=llm, tools=tools, prompt=prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=True)
