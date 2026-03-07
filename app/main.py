from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def welcome():
    return {"message": "Welcome to PAI"}

@app.get("/health")
def health():
    return { "status": "healthy", "message": "service is running"}   