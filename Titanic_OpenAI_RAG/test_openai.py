
import os
from dotenv import load_dotenv
from openai import OpenAI

# .env 파일에서 API 키 읽기
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError(".env 파일에 OPENAI_API_KEY가 없습니다.")

# OpenAI 연결
client = OpenAI(api_key=api_key)

# 간단한 연결 테스트
response = client.responses.create(
    model="gpt-6-luna",
        reasoning={"effort": "none"},
    input="연결 테스트입니다. 'OpenAI API 연결 성공'이라고 답해주세요.",
    max_output_tokens=100
)

print(response.output_text)
