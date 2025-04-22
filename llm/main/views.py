from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from datetime import datetime
import requests
from langchain_core.messages import HumanMessage, AIMessage
from django.views.decorators.csrf import csrf_exempt
import json
from openai import OpenAI
from django.conf import settings
import os
from langchain_openai import ChatOpenAI  # 최신 LangChain용 OpenAI 연동
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.prompts import ChatPromptTemplate, PromptTemplate, MessagesPlaceholder
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain.docstore.document import Document
from langchain.docstore import InMemoryDocstore
import faiss

# Create your views here.
def chat_view(request):
    return render(request, 'homepage.html')

def calculator_view(request):
    return render(request, 'calculator.html')

def redirect_to_main(request):
    return redirect('/main')

def load_faiss_index():
    # 현재 파일 (views.py) 기준으로 faiss 폴더 경로 계산
    base_dir = os.path.dirname(__file__)              # → main/
    faiss_dir = os.path.join(base_dir, "faiss")       # → main/faiss

    # docs.json 로드
    docs_path = os.path.join(faiss_dir, "docs.json")
    with open(docs_path, "r", encoding="utf-8") as f:
        texts = json.load(f)

    docs = [Document(page_content=text) for text in texts]

    # FAISS index 로드
    index_path = os.path.join(faiss_dir, "my_index.index")
    index = faiss.read_index(index_path)

    # 임베딩 모델
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # LangChain용 docstore 및 mapping
    index_to_docstore_id = {i: str(i) for i in range(len(docs))}
    docstore = InMemoryDocstore({str(i): doc for i, doc in enumerate(docs)})

    return FAISS(embedding_model.embed_query, index, docstore, index_to_docstore_id)

vectorstore = load_faiss_index()


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def chat_api(user_input, chat_history=None):
    if chat_history is None:
        chat_history = []

    # 🔁 OpenAI LLM 설정
    llm = ChatOpenAI(
        model="gpt-4o",  # 또는 gpt-3.5-turbo
        temperature=0.7,
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )

    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    contextualize_q_prompt = PromptTemplate(
        input_variables=["input", "chat_history"],
        template="""
        기존 대화:
        {chat_history}

        질문:
        {input}

        다음 질문을 생성하세요:
        """
    )

    qa_prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 대출 전문가 AI입니다. 주어진 문서를 기반으로 사용자에게 정확한 정보를 제공하세요."),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    ("system", "관련 문서 내용:\n\n{context}")
    ])


    history_aware_retriever = create_history_aware_retriever(llm, retriever, contextualize_q_prompt)
    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

    response = rag_chain.invoke({
        "input": user_input,
        "chat_history": chat_history
    })

    chat_history.extend([
        HumanMessage(content=user_input),
        AIMessage(content=response["answer"])
    ])

    return response["answer"], chat_history


@csrf_exempt
def chat_api_view(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            user_input = body.get('message', '')

            # 세션 기반 대화 이력 불러오기
            raw_history = request.session.get('chat_history', [])
            formatted_history = []
            for i in range(0, len(raw_history), 2):
                formatted_history.append(HumanMessage(content=raw_history[i]))
                if i + 1 < len(raw_history):
                    formatted_history.append(AIMessage(content=raw_history[i+1]))

            # LangChain 기반 답변 생성
            answer, updated_history = chat_api(user_input, formatted_history)

            # 새 히스토리 세션에 저장 (내용만 저장)
            request.session['chat_history'] = [m.content for m in updated_history]

            return JsonResponse({'reply': answer})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid method'}, status=405)

def download_chat_log(request):
    # 세션에서 대화 히스토리 불러오기
    raw_history = request.session.get('chat_history', [])

    # 텍스트 형식으로 변환 (짝수: user, 홀수: AI)
    lines = []
    for i in range(0, len(raw_history), 2):
        user_msg = raw_history[i]
        lines.append(f"사용자: {user_msg}")
        if i + 1 < len(raw_history):
            ai_msg = raw_history[i + 1]
            lines.append(f"AI: {ai_msg}")
        lines.append("")  # 줄바꿈

    chat_text = "\n".join(lines)

    # 파일명 만들기
    filename = f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

    # 응답으로 텍스트 파일 반환
    response = HttpResponse(chat_text, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response






# === runpod api 폐기 ===
# def ask_from_runpod(message, history):
#     response = requests.post(
#         "194.68.245.203:22103/chat",
#         json={
#             "question": message,
#             "history": [msg.dict() for msg in history]  # LangChain message 포맷을 dict로 변환
#         }
#     )
#     print("📡 RunPod 응답 상태코드:", response.status_code)
#     print("📄 RunPod 응답 텍스트:", response.text)
#     data = response.json()
#     print(data)
#     return data["answer"], [HumanMessage(**m) if m["type"] == "human" else AIMessage(**m) for m in data["history"]]



# import traceback

# @csrf_exempt
# def chat_api(request):
#     if request.method == 'POST':
#         try:
#             body = json.loads(request.body)
#             print("받은 메시지:", body)

#             user_input = body.get('message')
#             print("user_input:", user_input)

#             raw_history = request.session.get('chat_history', [])
#             formatted_history = []
#             for i in range(0, len(raw_history), 2):
#                 formatted_history.append(HumanMessage(content=raw_history[i]))
#                 if i + 1 < len(raw_history):
#                     formatted_history.append(AIMessage(content=raw_history[i+1]))

#             answer, updated_history = ask_from_runpod(user_input, formatted_history)
#             request.session['chat_history'] = [msg.content for msg in updated_history]

#             return JsonResponse({'reply': answer})

#         except Exception as e:
#             print("에러 발생:", str(e))
#             traceback.print_exc()  # ✅ 구체적인 에러 트레이스 출력
#             return JsonResponse({'error': str(e)}, status=500)

#     return JsonResponse({'error': 'Invalid method'}, status=405)


