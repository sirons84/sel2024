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

# 페이지 제목
st.header("AIDI와 관련하여 사회정서학습(SEL) 연결을 도와주는 챗봇")
st.write('학생 페르소나+사회정서학습 프레임워크 를 선택한 후 "위 조건을 이용한 AIDT를 활용한 사회정서학습 아이디어를 알려줘"', divider='rainbow')
st.markdown('''
    :문서출처: (1) 디지털 기반 사회정서학습(SEL) 활용 사례 및 모델탐색 - 김현구, 2023, KERIS ''')
st.markdown('''
    :문서출처: (2) 사회·정서적 학습(SEL), 학생-학부모-교사 모두에게 도입해야! - 이찬승, 2023, 교육을 바꾸는 사람들 ''')
st.markdown('''
    :red[만든이] :orange[울산] :green[호계초] :blue[신재광]''')
st.markdown('''
    :red[도와준이] :orange[울산] :green[화진초] :blue[석희철]''')

# 학생 페르소나 선택
persona_options = [
    "학습 성적 높지만 디지털 역량이 낮은 학생",
    "학습 성적 낮고 디지털 역량도 낮은 학생",
    "학습 성적 높고 디지털 역량도 높은 학생",
    "학습 성적 낮지만 디지털 역량은 높은 학생",
    "직접 쓰기"
]
framework_options = [
    "자기인식(self-awareness)",
    "자기 관리(self-management)",
    "사회적 인식(social awareness)",
    "대인 관계 기술(relationship skills)",
    "책임 있는 결정(making responsible decisions)",
    "직접 쓰기"
]

# 드롭다운 메뉴 한 줄에 2개로 구성
col1, col2 = st.columns(2)
with col1:
    persona = st.selectbox("학생 페르소나를 선택하세요", persona_options)

with col2:
    framework = st.selectbox("사회정서학습 프레임워크를 선택하세요", framework_options)

# 사용자가 직접 쓰기를 선택한 경우
if persona == "직접 쓰기":
    persona = st.text_input("학생 페르소나를 직접 입력하세요")

if framework == "직접 쓰기":
    framework = st.text_input("사회정서학습 프레임워크를 직접 입력하세요")

# 선택된 옵션을 표시
if persona and framework:
    st.write(f"선택된 학생 페르소나: {persona}")
    st.write(f"선택된 사회정서학습 프레임워크: {framework}")

# 메세지 모두 불러오기
thread_messages = client.beta.threads.messages.list(thread_id_2, order="asc")

# 메세지 가져와서 UI에 뿌려주기
for msg in thread_messages.data:
    with st.chat_message(msg.role):
        st.write(msg.content[0].text.value)  # content를 정확히 참조

# 입력창에 입력을 받아서 입력된 내용으로 메세지 생성
prompt = st.chat_input("물어보고 싶은 것을 입력하세요!")
if prompt:
    # 사용자가 선택한 페르소나와 프레임워크를 포함하여 프롬프트 구성
    full_prompt = f"학생 페르소나: {persona}\n사회정서학습 프레임워크: {framework}\n질문: {prompt}"

    message = client.beta.threads.messages.create(
        thread_id=thread_id_2,  # 'thread_id'를 변수로 사용
        role="user",
        content=full_prompt  # 선택된 페르소나와 프레임워크를 포함한 프롬프트
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
