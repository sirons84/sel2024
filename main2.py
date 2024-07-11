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
st.header("AIDT와 관련하여 사회정서학습(SEL) 연결을 도와주는 챗봇")
st.write('학생 맥락과 AIDT 기능, 그리고 AI 기반 지원 방안을 단계적으로 입력해주세요.', divider='rainbow')

# Step 1: 학생 맥락 입력
st.subheader("STEP 1. 학생 맥락")
student_context = st.text_area("이 학생의 맥락을 자세히 작성해주세요.")

# Step 2: AIDT 기능 선택
st.subheader("STEP 2. AIDT 기능 선택")
aidt_functions = {
    "학습진단": ["성취수준 진단", "학습현황 분석"],
    "학습추천": ["학습경로 추천", "학습 처방"],
    "맞춤형 콘텐츠": ["다양한 콘텐츠 제공", "학습처방 콘텐츠 제공", "피드백 및 도움말 제공"],
    "대시보드": ["학습 참여도 정보 제공", "학습 이력 정보 제공", "학습 분석 정보 제공"],
    "AI튜터": ["질의응답", "추가학습자료 제공", "학습 전략 제안", "학습진도 모니터링", "피드백 및 성취도 평가", "오답노트 제공"],
    "AI 보조교사": ["수업설계 지원", "피드백 설계 지원", "평가 지원", "학생 모니터링 지원"],
    "교사 재구성 기능": ["학습 활동 재구성 대시보드 구성", "학습 관리", "학습자 관리"]
}

selected_aidt_functions = st.multiselect("AIDT 기능을 2개 선택해주세요.", list(aidt_functions.keys()))

# Step 3: AI 기반 지원 방안 입력
st.subheader("STEP 3. AI 기반 지원 방안")
cognitive_emotional_support = st.text_area("이 학생에게는 어떤 인지적 및 정서적 지원이 필요할까요?")
customized_support = st.text_area("이 학생에게 필요한 맞춤형 지원은 또 무엇이 있을까요?")
data_needed = st.text_area("이 학생의 배움 상황을 평가하고 개선하기 위해 어떤 데이터가 필요할까요?")

# 프롬프트 생성
full_prompt = f"""
학생 맥락:
{student_context}

AIDT 기능:
{', '.join(selected_aidt_functions)}

인지적 및 정서적 지원:
{cognitive_emotional_support}

맞춤형 지원:
{customized_support}

필요한 데이터:
{data_needed}
"""

# 프롬프트 실행 및 결과 출력
message = client.beta.threads.messages.create(
    thread_id=thread_id_2,
    role="user",
    content=full_prompt
)

with st.chat_message(message.role):
    st.write(message.content[0].text.value)

run = client.beta.threads.runs.create(
    thread_id=thread_id_2,
    assistant_id=assistant_id,
)

while run.status != "completed":
    time.sleep(1)
    run = client.beta.threads.runs.retrieve(
        thread_id=thread_id_2,
        run_id=run.id,
    )

messages = client.beta.threads.messages.list(
    thread_id=thread_id_2
)

with st.chat_message(messages.data[0].role):
    st.write(messages.data[0].content[0].text.value)