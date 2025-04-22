import streamlit as st
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools import StructuredTool
from pydantic import BaseModel
import re
import math

# ✅ 숫자 단위 전처리 함수
def convert_korean_numbers(text: str) -> str:
    units = {"천": 1_000, "만": 10_000, "억": 100_000_000}
    pattern = re.compile(r'(\d+)(천|만|억)')
    
    def repl(match):
        return str(int(match.group(1)) * units[match.group(2)])
    
    return pattern.sub(repl, text)

# ✅ 전세대출 한도 계산
def calculate_jeonse_limit(deposit: int, income: int, credit_grade: str) -> str:
    ratio = 0.8 if credit_grade == "상" else 0.6 if credit_grade == "중" else 0.4
    limit = int(min(deposit * ratio, income * 4))
    return f"당신의 전세대출 한도는 약 {limit:,}원입니다."

# ✅ 월 상환금 계산
def calculate_monthly_payment(loan_amount: int, annual_interest_rate: float, years: int) -> str:
    r = annual_interest_rate / 100 / 12
    n = years * 12
    monthly = loan_amount * r / (1 - (1 + r) ** -n)
    return f"{loan_amount:,}원을 연 {annual_interest_rate}%의 이자로 {years}년간 갚을 경우, 매월 약 {int(monthly):,}원을 상환하셔야 합니다."

# ✅ 스키마 정의
class JeonseLimitInput(BaseModel):
    deposit: int
    income: int
    credit_grade: str

class MonthlyPaymentInput(BaseModel):
    loan_amount: int
    annual_interest_rate: float
    years: int

# ✅ 도구 등록
tools = [
    StructuredTool.from_function(
        name="jeonse_limit_calc",
        description="전세대출 한도 계산기",
        args_schema=JeonseLimitInput,
        func=calculate_jeonse_limit
    ),
    StructuredTool.from_function(
        name="monthly_payment_calc",
        description="월 상환금 계산기",
        args_schema=MonthlyPaymentInput,
        func=calculate_monthly_payment
    )
]

# ✅ LLM 및 메모리 초기화
llm = ChatOpenAI(model_name="gpt-4", temperature=0)
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# ✅ 프롬프트 설정
prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 금융 상담 전문가입니다."),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}")
])

# ✅ Agent 생성
agent = create_openai_functions_agent(llm=llm, tools=tools, prompt=prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, memory=memory, verbose=True)

# ✅ Streamlit UI
st.title("💰 금융 상담 챗봇")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("질문을 입력하세요:")

if user_input:
    processed_input = convert_korean_numbers(user_input)
    response = agent_executor.run({"input": processed_input})
    st.session_state.chat_history.append(("user", user_input))
    st.session_state.chat_history.append(("bot", response))

for role, msg in st.session_state.chat_history:
    st.chat_message(role).write(msg)
