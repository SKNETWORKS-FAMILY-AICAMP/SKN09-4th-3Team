from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from peft import PeftModel
import json
import faiss
from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.docstore import InMemoryDocstore
from langchain_community.llms import HuggingFacePipeline
from langchain_core.outputs import Generation, LLMResult
from langchain_core.messages import BaseMessage
from typing import List
from transformers import pipeline
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_core.messages import HumanMessage, AIMessage
import os
from sentence_transformers import SentenceTransformer
from langchain.prompts import PromptTemplate

HF_TOKEN = os.getenv("HF_TOKEN")

# 메인 모델
tokenizer = AutoTokenizer.from_pretrained("beomi/KoAlpaca-Polyglot-5.8B", token=HF_TOKEN)
base_model = AutoModelForCausalLM.from_pretrained("beomi/KoAlpaca-Polyglot-5.8B", token=HF_TOKEN)

# LoRA 어댑터
model = PeftModel.from_pretrained(base_model, "monka/koalpaca_finetune", token=HF_TOKEN)

# 임베딩
embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", token=HF_TOKEN)



print("🔥 모델 로딩 중...")
tokenizer = AutoTokenizer.from_pretrained("beomi/KoAlpaca-Polyglot-5.8B")
base_model = AutoModelForCausalLM.from_pretrained("beomi/KoAlpaca-Polyglot-5.8B")
model = PeftModel.from_pretrained(base_model, "monka/koalpaca_finetune")
generator = pipeline("text-generation", model=model, tokenizer=tokenizer)

print("📦 FAISS 인덱스 로딩 중...")
def load_faiss_index(faiss_dir="faiss"):
    with open(f"{faiss_dir}/docs.json", "r", encoding="utf-8") as f:
        texts = json.load(f)
    docs = [Document(page_content=text) for text in texts]
    index = faiss.read_index(f"{faiss_dir}/my_index.index")
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    index_to_docstore_id = {i: str(i) for i in range(len(docs))}
    docstore = InMemoryDocstore({str(i): doc for i, doc in enumerate(docs)})
    return FAISS(embedding_model.embed_query, index, docstore, index_to_docstore_id)

vectorstore = load_faiss_index()




def ask_question(user_input, chat_history=None):
    if chat_history is None:
        chat_history = []

    # HuggingFace 기반 LangChain LLM 생성
    llm = HuggingFacePipeline(pipeline=generator)

    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    contextualize_q_prompt = PromptTemplate(
    input_variables=["input", "chat_history"],
    template="""
    기존 대화:
    {chat_history}

    질문:
    {input}

    다음 질문을 생성하세요:
    """)

    qa_prompt = ChatPromptTemplate.from_messages([
        ("system", "당신은 대출 전문가 AI입니다. 주어진 문서를 기반으로 사용자에게 정확한 정보를 제공하세요."),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}")
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
