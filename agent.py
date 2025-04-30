from langchain.chat_models import AzureChatOpenAI
from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType
from tools import order_food_p

# Azure GPT-4 setup
llm = AzureChatOpenAI(
    deployment_name="gpt-4.1",
    openai_api_version="2024-12-01-preview",
    openai_api_key="",
    azure_endpoint="https://joshi-ma20px8d-eastus2.cognitiveservices.azure.com/",
)

# Agent tools (add more later if needed)
tools = [order_food_p]

# Initialize the agent
agent_executor = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=True,
)
