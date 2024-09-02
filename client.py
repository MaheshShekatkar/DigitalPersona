import os
from langchain_openai import AzureChatOpenAI
from langchain_openai import AzureOpenAI

DEPLOYMENET_NAME = "gpt-4o-mini"

def get_chat_client() -> AzureChatOpenAI:
    return AzureChatOpenAI(
      api_key=os.getenv("OPENAI_API_KEY"),
      api_version="2024-02-01",
      azure_endpoint ="https://digital-ai-assistance.openai.azure.com/",
      deployment_name = DEPLOYMENET_NAME,
      temperature= 0.1
  )
    
def get_client() -> AzureOpenAI:
 return AzureOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    api_version="2024-02-01",
    azure_endpoint ="https://digital-ai-assistance.openai.azure.com/",
    deployment_name = DEPLOYMENET_NAME,
    temperature= 0.9
)
        
    
    