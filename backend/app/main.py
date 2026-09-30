from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "LegalEase AI is running"}

@app.get("/health")
def health():
    return {"status": "healthy"}
@app.get("/health")
def health():
    return {"status": "healthy"}
from pydantic import BaseModel

class GenerateRequest(BaseModel):
    data: dict = {}

@app.post("/generate")
def generate_document(request: GenerateRequest):
    return {
        "content": "Legal document generated successfully."
    }