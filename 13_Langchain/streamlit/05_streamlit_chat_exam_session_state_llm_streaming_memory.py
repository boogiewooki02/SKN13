##################################################################
#  streamlit/05_streamlit_chat_exam_session_state_llm_streaming_memory.py
##################################################################

import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser

# 프롬프트 -> LLM 요청 -> 응답 -> chat_message container에 출력

# LLM 모델 생성
@st.cache_resource
def get_llm_model():
    load_dotenv()
    model = ChatOpenAI(model='gpt-4o-mini')
    prompt_template = ChatPromptTemplate(
        messages = [
            MessagesPlaceholder(variable_name="history", optional=True),
            ("user", "{query}") # 사용자 질문
        ]
    )
    return prompt_template | model | StrOutputParser()

model = get_llm_model()


st.title("Chatbot+session state 위젯 튜토리얼")

# Session State를 생성
## session_state: dictionary 구현체. 시작 ~ 종료할 때까지 사용자별로 유지되야 하는 값들을 저장하는 곳

# 0. 대화 내역을 session_state의 "messages":list로 저장
# 1. session state에 "messages" key가 있는지 조회
if "messages" not in st.session_state:
    st.session_state["messages"] = [] # 대화 내용들 저장 용도

##############################
# 기존 대화 이력을 출력
##############################
message_list = st.session_state['messages']
history_message_list = [(msg_dict['role'], msg_dict['content']) for msg_dict in message_list]

for message in st.session_state['messages']:
    with st.chat_message(message['role']):
        st.write(message['content'])



# 사용자의 프롬프트(질문)을 입력받는 위젯
prompt = st.chat_input("User Prompt") # 사용자가 입력한 문자열을 반환
# print(prompt)

## 대화 작업
if prompt is not None:
    # session_state의 messages에 대화 내역을 저장
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    
    with st.chat_message("ai"):
        message_placeholder = st.empty() # update가 가능한 컨테이너
        full_message = "" # LLM이 응답하는 토큰들을 저장할 문자열 변수
        for token in model.stream({"query": prompt, "history": history_message_list}):
            full_message += token
            message_placeholder.write(full_message) # 기존 내용을 full_message로 사용
            # print(full_message)
            # print("--------------------------")

        st.session_state['messages'].append({"role": "ai", "content": full_message})

