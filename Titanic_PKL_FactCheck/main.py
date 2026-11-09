
import pandas as pd
from pathlib import Path

# 1. PKL 파일 불러오기
BASE_DIR = Path(__file__).resolve().parent
df = pd.read_pickle(BASE_DIR / "titanic_data.pkl")

# 2. 기본 통계 계산
total = len(df)
survived = int(df["Survived"].sum())

gender = df.groupby("Sex")["Survived"].agg(
    ["count", "sum", "mean"]
)

classes = df.groupby("Pclass")["Survived"].agg(
    ["count", "sum", "mean"]
)

# 3. 팩트체킹용 사실표 생성
facts = {
    "F-1": {
        "주제": "전체 생존율",
        "근거": (
            f"전체 {total}명 중 {survived}명 생존, "
            f"생존율 {survived / total * 100:.1f}%"
        )
    },
    "F-2": {
        "주제": "성별 생존율",
        "근거": (
            f"여성 {gender.loc['female', 'mean'] * 100:.1f}%, "
            f"남성 {gender.loc['male', 'mean'] * 100:.1f}%"
        )
    },
    "F-3": {
        "주제": "객실 등급별 승객 수",
        "근거": ", ".join(
            f"{i}등석 {int(classes.loc[i, 'count'])}명"
            for i in [1, 2, 3]
        )
    },
    "F-4": {
        "주제": "객실 등급별 생존율",
        "근거": ", ".join(
            f"{i}등석 {classes.loc[i, 'mean'] * 100:.1f}%"
            for i in [1, 2, 3]
        )
    }
}

# 4. 결과 확인
print("===== 타이타닉 PKL 사실표 =====")

for fact_id, fact in facts.items():
    print(f"{fact_id} | {fact['주제']} | {fact['근거']}")


# 5. 질문에 맞는 사실 검색 및 답변

def ask_question(question):
    q = question.lower().replace(" ", "")

    # 객실 등급별 생존율
    if ("등석" in q or "객실" in q) and "생존" in q:
        fact_id = "F-4"

    # 객실 등급별 승객 수
    elif "등석" in q or "객실" in q:
        fact_id = "F-3"

    # 성별 생존율
    elif any(word in q for word in ["여성", "남성", "성별"]):
        fact_id = "F-2"

    # 전체 생존율
    elif "전체" in q and "생존" in q:
        fact_id = "F-1"

    # 사실표에 없는 질문
    else:
        return "확인 불가", None

    fact = facts[fact_id]
    answer = fact["근거"] + f" [{fact_id}]"

    return answer, fact_id


# 6. 챗봇 질문 테스트
questions = [
    "전체 생존율은?",
    "여성 생존율은?",
    "3등석 승객은 몇 명인가?",
    "2등석 생존율은?",
    "승객들의 국적은?"
]

print("\n===== PKL 팩트체킹 챗봇 테스트 =====")

for question in questions:
    answer, fact_id = ask_question(question)

    print(f"\n질문: {question}")
    print(f"답변: {answer}")
