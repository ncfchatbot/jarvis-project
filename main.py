import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai
from google.genai import types

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    text: str

@app.post("/chat")
async def chat_with_jarvis(request: ChatRequest):
    user_message = request.text
    
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return {"response": "Error: ไม่พบ API Key ในระบบหลังบ้านครับ"}

    try:
        # ใช้ไลบรารีทางการของ Google มันจะจัดการเชื่อมต่อเข้า Interactions API ให้เองโดยอัตโนมัติ
        client = genai.Client(api_key=api_key)
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_message,
            config=types.GenerateContentConfig(
                system_instruction="You are Jarvis, an advanced AI assistant. You MUST strictly reply in Thai."
            )
        )
        return {"response": response.text}
        
    except Exception as e:
        return {"response": f"ระบบขัดข้องครับเจ้านาย: {str(e)}"}

@app.get("/")
async def root():
    return {"status": "Jarvis Interactions API is running!"}