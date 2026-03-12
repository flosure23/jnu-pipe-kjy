from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from app.spam import check_spam

# FastAPI 기반 웹 앱 생성
# /docs (Swagger UI)에 표기되는 이름
app = FastAPI(title="SpamCheck Web")

# 정적 HTML 서빙: static 안에 파일들을 URL로 접근가능하게 설정
# {URL}/static/…… 으로 접근 가능
app.mount("/static", StaticFiles(directory="static"), name="static")

# 메인 페이지 (/) 처리: "/"로 접속 시 index.html 반환
@app.get("/", response_class=HTMLResponse)
def home():
    with open("static/index.html", encoding="utf-8") as f:
        return f.read()

from pydantic import BaseModel

class SpamRequest(BaseModel):
    text: str

# classify 요청이 올 때 처리할 로직
# async: 비동기 처리 (서버가 요청을 기다리는 동안 다른 요청도 처리 가능)
@app.post("/classify")
async def classify(payload: SpamRequest):
    text = payload.text
    
    # spam.py의 check_spam 함수를 호출하여 결과 반환
    label, score = check_spam(text)
    
    return {
        "label": label, 
        "score": score
    }

# 실행은 터미널에서 uvicorn app.main:app --reload 명령어로 수행하거나
# 아래 주석을 해제하여 직접 실행할 수 있습니다.
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8000)