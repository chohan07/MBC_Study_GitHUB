
import os
from dotenv import load_dotenv
from openai import OpenAI

# 기존 main.py의 검색 기능 가져오기
from main import search_fact

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def ask_rag(question):
    # 1. 관련 사실 검색
    fact_id, fact = search_fact(question)

    # 2. 근거가 없으면 답변하지 않음
    if fact is None:
        return "확인 불가"

    # 3. 검색된 사실만 AI에 전달
    evidence = fact["근거"]

    response = client.responses.create(
        model="gpt-4.1-mini",
        instructions=(
            "당신은 타이타닉 데이터 팩트체킹 챗봇입니다. "
            "제공된 근거에 있는 내용으로만 답변하세요. "
            "근거에 없는 정보는 추측하지 말고 '확인 불가'라고 답하세요. "
            "답변은 한국어로 간결하게 작성하세요. "
            f"답변 마지막에 반드시 사실ID [{fact_id}]를 표시하세요."
        ),
        input=(
            f"질문: {question}\n"
            f"근거: {evidence}"
        ),
        max_output_tokens=200
    )

    return response.output_text




# 이 파일을 직접 실행할 때만 테스트
if __name__ == "__main__":
    questions = [
        "전체 생존율은?",
        "여성 생존율은?",
        "2등석 생존율은?",
        "승객들의 국적은?"
    ]

    print("\n===== 타이타닉 RAG 챗봇 =====")

    for question in questions:
        print(f"\n질문: {question}")
        print(f"챗봇 답변: {ask_rag(question)}")
