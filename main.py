# pip freeze > requirements.txt
# pip install -r requirements.txt
# streamlit run main.py
from langchain_community.chains import PebbloRetrievalQA 
from langchain.memory import ConversationBufferMemory 
from langchain.chains import ConversationalRetrievalChain
import client 
import store
import streamlit as st
import streamlit_chat as message
import agent
from langchain.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables import ConfigurableFieldSpec
from langchain_community.chat_message_histories import SQLChatMessageHistory

def main():
    # store keywork in the vector database.
  vectorstore = store.store()
  st.title("AI assistant for digital application")
  st.header("Ask anything about your application... 🤖")
  
  if 'generated' not in st.session_state:
    st.session_state['generated']  = []
    
  if 'past' not in st.session_state:
    st.session_state['past'] = []  
    
  if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []
   
    
  system_prompt = (
    "You are an assistant for question-answering tasks. "
    "Use the following pieces of retrieved context to answer "
    "the question. If you don't know the answer, say that you "
    "don't know. return only the a word "
    "answer concise."
    "\n\n"
    "{context}"
  )  
  
  human_prompt = (
  """
    You are an assistant that helps users with investment bank realted queries.
    You can fetch the answer from the agent tool.
    If you don't know the answer in agent, say that you don't know.

    User: {input}"""
  )  
    
  prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
         MessagesPlaceholder("chat_history"),
        ("human", human_prompt),
    ]
  )
  
  chatclient = client.get_chat_client()
  
  question_answer_chain = create_stuff_documents_chain(chatclient, prompt=prompt)
  qa_chain = create_retrieval_chain(vectorstore.as_retriever(), 
                                    question_answer_chain)
  
  conversational_rag_chain = RunnableWithMessageHistory(
    qa_chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history",
    output_messages_key="answer",
    history_factory_config=[
        ConfigurableFieldSpec(
            id="user_id",
            annotation=str,
            name="User ID",
            description="Unique identifier for the user.",
            default="",
            is_shared=True,
        ),
        ConfigurableFieldSpec(
            id="conversation_id",
            annotation=str,
            name="Conversation ID",
            description="Unique identifier for the conversation.",
            default="",
            is_shared=True,
        ),
    ],
  )
  
  # get the user input
  user_input = get_query()
  if user_input:
    # Similarity or Semantic search
    result = conversational_rag_chain.invoke({'input': user_input},
                                              config={"configurable": {"user_id": "123", "conversation_id": "1"}})
    st.session_state.chat_history.append((user_input,result['answer']))
    st.session_state.past.append(user_input)
    print(f"retrival chain ====> {result['context']}")
    st.session_state.generated.append(result['answer'])

    if st.session_state['generated']:
      for i in range(len(st.session_state['generated'])):
        message.message(st.session_state['past'][i], is_user=True, key=str(i)+ '_user')  
        #message.message(st.session_state['generated'][i],key=str(i))
      # provide the serach result to agent which intern call API 
        response =agent.run_agent(st.session_state['generated'][i])
        message.message(response['output'],key=str(i))
      # display the final result on the screen
      # If input is audio and video convert into repective 
    
def get_query():
  input_text = st.chat_input("Ask anything about your application...")
  return input_text

def get_session_history(user_id: str, conversation_id: str):
    return SQLChatMessageHistory(f"{user_id}--{conversation_id}", "sqlite:///memory.db") 

if __name__ == '__main__':
  main()