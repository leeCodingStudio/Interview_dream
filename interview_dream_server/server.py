import fastapi
from fastapi import Request
from model import generate_question
from fastapi.middleware.cors import CORSMiddleware

app = fastapi.FastAPI()
# 모든 주소(*)를 허용
# CORSMiddleware를 등록합니다.
origins = ["https://kdt-team-2.github.io"]  # 클라이언트 도메인 추가 필요
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.post("/test")
async def test(request: Request):
    split_text_list = []
    input_data = await request.json()
    print(input_data)
    # 텍스트만 파싱
    context = input_data["context"]
    # 전체 내용을 한 번에 처리
    result = generate_question(context)
    split_text_list.append(result)
    # 문장을 마침표를 기준으로 문단으로 나누기
    sentences = context.split('.')
    sentences = sentences[:-1]
    paragraphs = []
    paragraph = ""
    for sentence in sentences:
        paragraph += sentence.strip() + ". "
        if len(paragraph) > 30:
            paragraphs.append(paragraph)
            paragraph = ""
    # 마지막 문단 처리
    if paragraph.strip():
        paragraphs.append(paragraph)
    # 문단씩 짤라서 처리 range뒤에 숫자만 원하는 문단으로 짜르면 됩니다.
    for i in range(0, len(paragraphs), 3):
        combined_paragraph = ""
        for j in range(3):
            if i + j < len(paragraphs):
                combined_paragraph += paragraphs[i + j]
        result = generate_question(combined_paragraph)
        split_text_list.append(result)
    new_list = []
    for s in split_text_list:
        for s2 in s:
            s3_list = []
            # split 함수의 결과에 구분자를 추가
            for end in ['요.', '?']:
                substrings = s2.split(end)
                for i, s3 in enumerate(substrings):
                    s3 = s3.replace("*", "")
                    s3 = s3.replace("-", "")
                    s3 = s3.replace('"', "")
                    s3 = s3.replace(")", "")
                    s3 = s3.replace("(", "")
                    if i < len(substrings) - 1:
                        if s3.endswith('요.') or s3.endswith('?'):
                            s3_list.append(s3 + end)
                    elif s3:
                        if s3.endswith('요.') or s3.endswith('?'):
                            s3_list.append(s3)
            new_list += s3_list
    print(new_list)
    return new_list


@app.post("/chat")
async def test(request: Request):
    input_data = await request.json()
    # 텍스트만 파싱
    context = input_data["context"]
    text_list = generate_question(context)
    new_list = []
    s3_list = []
    for s in text_list:
        # split 함수의 결과에 구분자를 추가
        for end in ['요.', '?']:
            substrings = s.split(end)
            for i, s3 in enumerate(substrings):
                s3 = s3.replace("*", "")
                s3 = s3.replace("-", "")
                s3 = s3.replace('"', "")
                s3 = s3.replace(")", "")
                s3 = s3.replace("(", "")
                if i < len(substrings) - 1:
                    if s3.endswith('요.') or s3.endswith('?'):
                        s3_list.append(s3 + end)
                elif s3:
                    if s3.endswith('요.') or s3.endswith('?'):
                        s3_list.append(s3)
    new_list += s3_list
    if len(new_list) == 0:
        return ['Nan']
    elif type(new_list) == list:
        return [new_list[0]]
    else:
        return new_list





