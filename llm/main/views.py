from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from datetime import datetime
import requests
from langchain_core.messages import HumanMessage, AIMessage

# Create your views here.
def chat_view(request):
    return render(request, 'homepage.html')

def calculator_view(request):
    return render(request, 'calculator.html')

def redirect_to_main(request):
    return redirect('/main')




def ask_from_runpod(message, history):
    response = requests.post(
        "http://<runpod_ip>:8000/chat",
        json={
            "question": message,
            "history": [msg.dict() for msg in history]  # LangChain message 포맷을 dict로 변환
        }
    )
    data = response.json()
    return data["answer"], [HumanMessage(**m) if m["type"] == "human" else AIMessage(**m) for m in data["history"]]



def chat_api(request):
    if request.method == 'POST':
        user_input = request.POST.get('message')

        # 세션에서 이전 히스토리 로딩 (내용만 저장되어 있음)
        raw_history = request.session.get('chat_history', [])
        # LangChain 메시지 포맷으로 변환
        formatted_history = []
        for i in range(0, len(raw_history), 2):
            formatted_history.append(HumanMessage(content=raw_history[i]))
            if i + 1 < len(raw_history):
                formatted_history.append(AIMessage(content=raw_history[i+1]))

        # 모델 호출 + 업데이트된 히스토리 받기
        answer, updated_history = ask_from_runpod(user_input, formatted_history)

        # 세션에 새 히스토리 저장 (텍스트만 저장)
        request.session['chat_history'] = [msg.content for msg in updated_history]

        return JsonResponse({'reply': answer})


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
