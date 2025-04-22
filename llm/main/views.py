from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from datetime import datetime
from langchain_core.messages import HumanMessage, AIMessage
import openai
import os

def chat_view(request):
    return render(request, 'homepage.html')

def calculator_view(request):
    return render(request, 'calculator.html')

def redirect_to_main(request):
    return redirect('/main')

def ask_openai(message, history):
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=history + [{"role": "user", "content": message}]
        )
        answer = response.choices[0].message.content.strip()
        new_history = history + [{"role": "user", "content": message}, {"role": "assistant", "content": answer}]
        return answer, new_history
    except Exception as e:
        return f"에러 발생: {str(e)}", history
    
def chat_api(request):
    if request.method == 'POST':
        user_input = request.POST.get('message')
        raw_history = request.session.get('chat_history', [])
        formatted_history = []
        for i in range(0, len(raw_history), 2):
            formatted_history.append(HumanMessage(content=raw_history[i]))
            if i + 1 < len(raw_history):
                formatted_history.append(AIMessage(content=raw_history[i+1]))
        answer, updated_history = ask_from_openai(user_input, formatted_history)
        request.session['chat_history'] = [msg.content for msg in updated_history]
        return JsonResponse({'reply': answer})

def download_chat_log(request):
    raw_history = request.session.get('chat_history', [])
    lines = []
    for i in range(0, len(raw_history), 2):
        lines.append(f"사용자: {raw_history[i]}")
        if i + 1 < len(raw_history):
            lines.append(f"AI: {raw_history[i + 1]}")
        lines.append("")
    chat_text = "\n".join(lines)
    filename = f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    response = HttpResponse(chat_text, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename=\"{filename}\"'
    return response
