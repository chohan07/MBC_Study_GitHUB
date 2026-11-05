
import streamlit as st
from rag_chatbot import ask_rag
from main import search_fact

st.set_page_config(
    page_title="타이타닉 AI 팩트체킹",
    page_icon="🚢",
    layout="centered"
)

st.title("🚢 타이타닉 AI 팩트체킹 챗봇")
st.caption("OpenAI + RAG | 타이타닉 실습 데이터 156명 기준")

st.info(
    "이 챗봇은 타이타닉 실습 데이터의 사실표 F-1~F-4를 "
    "근거로 답변합니다. 근거가 없으면 '확인 불가'라고 답합니다."
)

# 질문 입력
question = st.text_input(
    "질문을 입력하세요",
    placeholder="예: 여성 생존율은?"
)

if st.button("질문하기"):
    if not question.strip():
        st.warning("질문을 입력해주세요.")
    else:
        with st.spinner("근거를 검색하고 답변을 생성하는 중..."):
            answer = ask_rag(question)
            fact_id, fact = search_fact(question)

        st.subheader("🤖 챗봇 답변")
        st.write(answer)

        if fact is not None:
            st.success(f"근거: {fact_id} | {fact['주제']}")
            with st.expander("검색된 원본 근거 보기"):
                st.write(fact["근거"])
        else:
            st.warning("사실표에 해당 질문의 근거가 없습니다.")

st.divider()
st.caption("출처: 타이타닉 실습 데이터(titanic_data.pkl)")
