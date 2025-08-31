import uvicorn
from fastapi import FastAPI
from paths.answers import router as answers_router
from paths.questions import router as questions_router

app = FastAPI()

app.include_router(answers_router)
app.include_router(questions_router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)