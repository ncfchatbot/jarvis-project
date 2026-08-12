import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai
from google.genai import types

app = FastAPI()

# ตั้งค่า CORS อนุญาตให้หน้าเว็บติดต่อเข้ามาได้
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
    print(f"เจ้านายสั่งว่า: {user_message}")

    try:
        # ดึง API Key
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            return {"response": "Error: ไม่พบ API Key ในระบบหลังบ้านของ Render ครับ"}

        # เชื่อมต่อด้วยไลบรารีตัวใหม่
        client = genai.Client(api_key=api_key)
        
        # ตั้งค่าคำสั่งและการค้นหา Google
        config = types.GenerateContentConfig(
            system_instruction="You are Jarvis, an advanced AI assistant. You MUST strictly reply in Thai.",
            tools=[{"google_search": {}}]
        )

        # เรียกใช้งานโมเดลรุ่นเสถียรที่สุด
        response = client.models.generate_content(
            model='gemini-1.5-flash-latest',
            contents=user_message,
            config=config
        )

        return {"response": response.text}

    except Exception as e:
        # ถ้าพัง จะส่งข้อความ Error ของระบบไปแสดงที่หน้าจอให้เห็นกันชัดๆ เลย
        error_msg = str(e)
        print(f"Error: {error_msg}")
        return {"response": f"ระบบขัดข้องครับเจ้านาย สาเหตุคือ: {error_msg}"}

@app.get("/")
async def root():
    return {"status": "Jarvis Backend is running online!"}