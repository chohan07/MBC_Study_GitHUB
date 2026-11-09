
import streamlit as st
from main import ask_question, facts

st.set_page_config(
    page_title="타이타닉 PKL 팩트체킹",
    page_icon="🚢",
    layout="centered"
)

st.title("🚢 타이타닉 PKL 팩트체킹 챗봇")
st.caption("Python + Pandas + PKL | OpenAI API 사용 안 함")

st.info(
    "타이타닉 실습 데이터 156명을 기준으로 "
    "사실표 F-1~F-4에서 근거를 검색합니다."
)

question = st.text_input(
    "질문을 입력하세요",
    placeholder="예: 여성 생존율은?"
)

if st.button("질문하기"):
    if not question.strip():
        st.warning("질문을 입력해 주세요.")
    else:
        answer, fact_id = ask_question(question)

        st.subheader("챗봇 답변")
        st.write(answer)

        if fact_id is not None:
            st.success(
                f"근거: {fact_id} | {facts[fact_id]['주제']}"
            )
            with st.expander("원본 근거 확인"):
                st.write(facts[fact_id]["근거"])
        else:
            st.warning("사실표에 해당 질문의 근거가 없습니다.")

st.divider()
st.caption("출처: 타이타닉 실습 데이터 (titanic_data.pkl)")
