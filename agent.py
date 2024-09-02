from langchain.agents import Tool
from langchain.memory import ConversationBufferMemory
import client
from typing import Any
import json
from langchain.agents import create_tool_calling_agent, tool, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate

def run_agent(user_input: str):
    memory = ConversationBufferMemory(memory_key="chat_history",return_messages=True)
    agent = get_agent(memory)
    currency= "GBP"
    try:
       print(f"Input to agent ===========> {user_input}")
      #  response = agent.invoke({"input":f"Fetch asset in Indian rupee and use the exchange rate one pound equals to 110.26 Indian rupees to convert asset value in given {currency}."
      #                           "Don't show the calculation."})
       response = agent.invoke({"input":"NV"})
       print(f"Tool response ===========> {response}")
    except json.JSONDecodeError as e:
      print(f"JSON decoding error encountered: {e}")
    except ValueError as e: 
      print(f"ValueError encountered: {e}")

    return response

def get_agent(memory:ConversationBufferMemory):
    llm=client.get_chat_client()
    tools = [get_asset_value,get_exhange_rate]
    llm_with_tools = llm.bind_tools(tools)
    prompt = ChatPromptTemplate.from_messages([
      ("system", "you're a helpful assistant."), 
      ("human", "{input}"), 
      ("placeholder", "{agent_scratchpad}")])

    agent = create_tool_calling_agent(llm=llm_with_tools, tools=tools, prompt=prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True,memory=memory)
    return agent_executor

def get_asset_tool() -> Tool:
    return Tool(
    name="asset value Tool",
    func=get_asset_value,
    description="Get the current asset value.")
    
@tool
def get_asset_value() -> str:
    """Applies a asset value function to an input."""
    return "{'asset':'1448.14159'}"    
  
@tool
def get_exhange_rate() -> str:
    """Applies a exhange rate function to an input."""
    return "{'rate':'one pound equals to 110.26 Indian rupees'}"          
