import os
import streamlit as st
import openai
from openai import OpenAI
import time

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

# thread id를 하나로 관리하기 위함
if 'thread_id_2' not in st.session_state:
    thread = client.beta.threads.create()
    st.session_state.thread_id_2 = thread.id  # thread.id만 저장

# thread_id, assistant_id 설정
thread_id_2 = st.session_state.thread_id_2
assistant_id = "asst_I1cokkUAGv3SMqt9XrcPmw8X"

# 메세지 모두 불러오기
thread_messages = client.beta.threads.messages.list(thread_id_2, order="asc")

# 페이지 제목
st.header("AIDI와 관련하여 사회정서학습(SEL) 연결을 도와주는 챗봇")
st.header('AIDT를 사용하는 학생의 상황+바라는 AIDT를 활용한 수업형태를 물어보세요', divider='rainbow')
st.markdown('''
    :red[만든이] :orange[울산] :green[호계초] :blue[신재광]''')
st.markdown('''
    :red[도와준이] :orange[울산] :green[화진초] :blue[석희철]''')

    
# 메세지 가져와서 UI에 뿌려주기
for msg in thread_messages.data:
    with st.chat_message(msg.role):
        st.write(msg.content[0].text.value)  # content를 정확히 참조
    
# 입력창에 입력을 받아서 입력된 내용으로 메세지 생성
prompt = st.chat_input("물어보고 싶은 것을 입력하세요!")
if prompt:
    message = client.beta.threads.messages.create(
        thread_id=thread_id_2,  # 'thread_id'를 변수로 사용
        role="user",
        content=prompt
        # content={"text": {"value": prompt}}  # 올바른 형식의 content 제공
    )

    # 입력한 메시지 UI에 표시
    with st.chat_message(message.role):
        st.write(message.content[0].text.value)
    
    # RUN을 돌리는 과정
    run = client.beta.threads.runs.create(
        thread_id=thread_id_2,
        assistant_id=assistant_id,
    )

    # RUN이 completed 되었나 1초마다 체크
    while run.status != "completed":
        print("status 확인중", run.status)
        time.sleep(1)
        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id_2,
            run_id=run.id,
        )
    
    # while문을 빠져나왔다는 것은 완료됐다는 것이니 메세지 불러오기
    messages = client.beta.threads.messages.list(
        thread_id=thread_id_2
    )
    # 마지막 메세지 UI에 표시하기
    with st.chat_message(messages.data[0].role):
        st.write(messages.data[0].content[0].text.value)

    # st.write(f"User has sent the following prompt: {prompt}")
