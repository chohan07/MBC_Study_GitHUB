
import pandas as pd
from pathlib import Path

# 현재 Python 파일이 있는 폴더
BASE_DIR = Path(__file__).resolve().parent

# PKL 파일 경로
file_path = BASE_DIR / "titanic_data.pkl"

# 타이타닉 데이터 불러오기
titanic_df = pd.read_pickle(file_path)

# 데이터 확인
print("타이타닉 데이터 불러오기 성공!")
print("행·열 개수:", titanic_df.shape)
print("전체 승객:", len(titanic_df), "명")
print("생존자:", int(titanic_df["Survived"].sum()), "명")
print("전체 생존율:", round(titanic_df["Survived"].mean() * 100, 1), "%")


# 4단계: 타이타닉 사실표 자동 생성

gender = titanic_df.groupby("Sex")["Survived"].agg(
    ["count", "sum", "mean"]
)

classes = titanic_df.groupby("Pclass")["Survived"].agg(
    ["count", "sum", "mean"]
)

facts = {
    "F-1": {
        "주제": "전체 생존율",
        "근거": (
            f"전체 {len(titanic_df)}명 중 "
            f"{int(titanic_df['Survived'].sum())}명 생존, "
            f"생존율 {titanic_df['Survived'].mean() * 100:.1f}%"
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

print("\n===== 타이타닉 사실표 =====")

for fact_id, fact in facts.items():
    print(f"{fact_id} | {fact['주제']} | {fact['근거']}")


# 5단계: 질문에 맞는 사실 검색

def search_fact(question):
    question = question.lower().replace(" ", "")

    # 객실 등급별 생존율
    if ("등석" in question or "객실" in question) and "생존" in question:
        return "F-4", facts["F-4"]

    # 객실 등급별 승객 수
    elif "등석" in question or "객실" in question:
        return "F-3", facts["F-3"]

    # 성별 생존율
    elif "여성" in question or "남성" in question or "성별" in question:
        return "F-2", facts["F-2"]

    # 전체 생존율
    elif "전체" in question and "생존" in question:
        return "F-1", facts["F-1"]

    # 근거가 없는 질문
    else:
        return None, None


# 검색 테스트
questions = [
    "전체 생존율은?",
    "여성 생존율은?",
    "3등석 승객은 몇 명인가?",
    "2등석 생존율은?",
    "승객들의 국적은?"
]

print("\n===== RAG 근거 검색 테스트 =====")

for question in questions:
    fact_id, fact = search_fact(question)

    print(f"\n질문: {question}")

    if fact:
        print(f"검색된 근거: {fact['근거']}")
        print(f"사실ID: {fact_id}")
    else:
        print("확인 불가")
