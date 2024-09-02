import os
from langchain_openai import AzureOpenAI
from langchain_openai import AzureChatOpenAI
from langchain_openai import AzureOpenAIEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.docstore.document import Document

DEPLOYMENET_NAME = "textEmbedding3Large"

chatClient = AzureChatOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    api_version="2024-02-01",
    azure_endpoint ="https://digital-ai-assistance.openai.azure.com/",
    deployment_name = DEPLOYMENET_NAME,
    temperature= 0.1
)

def store():
    with open(".\data\keywords.txt") as paper:
        keywords = paper.read()
      
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=10,
        chunk_overlap= 2,
        length_function= len,
        add_start_index = True
    )

    splits = text_splitter.split_text(keywords)

    emdeddings = AzureOpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"),
                                    azure_endpoint="https://digital-ai-assistance.openai.azure.com/",
                                    api_version="2024-02-01",
                                    azure_deployment=DEPLOYMENET_NAME)

    persist_directory = ".\data\db\chroma"
    vectorstore = Chroma.from_texts(
        texts=splits,
        embedding=emdeddings,
        persist_directory=persist_directory
    )
    return vectorstore
