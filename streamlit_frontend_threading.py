import streamlit as st
from langgraph_backend import chatbot
from langchain_core.messages import HumanMessage
import uuid

# *********************** utility function **************** 
def generate_thread_id():
    thread_id = uuid.uuid4()
    return thread_id

def reset_chat():
    thread_id=generate_thread_id()
    st.session_state['thread_id']=thread_id
    add_thread(st.session_state['thread_id'])    
    st.session_state['message_history']=[]


def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_thread'].append(thread_id)



# *********************** Session Setup ********************

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()    

# CONFIG ko ab session state initialize hone ke baad define kiya hai
CONFIG = {'configurable': {'thread_id': st.session_state['thread_id']}}

if 'chat_threads' not in st.session_state():
    st.session_state['chat_threads']=[]

add_thread(st.session_state['thread_id'])    


# *********************** Sidebar UI ***********************
st.sidebar.title('LangGraph Chatbot')

if st.sidebar.button('New Chat'):
    reset_chat()
    st.rerun()

st.sidebar.header('My Conversatio')

st.sidebar.text(st.session_state['thread_id'])

# *********************** Main UI ***************************

# Loading the conversation history
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])   

user_input = st.chat_input('Type here')

if user_input:
    # 1. User message ko history me add karein aur display karein
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    
    with st.chat_message('user'):
        st.text(user_input)

    ## first add the message to message_history
    with st.chat_message('assistant'):

        ai_message = st.write_stream(
            message_chunk.content for message_chunk, metadata in chatbot.stream(
                {'messages': [HumanMessage(content=user_input)]},
                    config=CONFIG,
                    stream_mode='messages'
            )
        )
        
    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})