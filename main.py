import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai

app = FastAPI()

# ตั้งค่า CORS อนุญาตให้หน้าเว็บทุกโดเมนติดต่อเข้ามาได้
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
        # ดึง API Key จากระบบ Environment Variable ที่ตั้งค่าไว้ใน Render
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise HTTPException(status_code=500, detail="API Key not found in environment variables")

        # เชื่อมต่อสมอง Gemini ด้วยคีย์ที่ถูกต้อง
        client = genai.Client(api_key=api_key)
        
        sys_instruct = "You are Jarvis, an advanced voice-enabled AI assistant. You MUST strictly reply in Thai."

        # ส่งคำถามไปให้ Gemini ประมวลผล พร้อมเปิดเครื่องมือค้นหา Google Search ในตัว
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_message,
            config=dict(
                system_instruction=sys_instruct,
                tools=[{"google_search": {} }]
            )
        )

        return {"response": response.text}

    except Exception as e:
        print(f"เกิดข้อผิดพลาดในระบบ AI: {str(e)}")
        return {"response": "ขออภัยครับเจ้านาย ระบบประมวลผลหลังบ้านขัดข้องครับ"}

@app.get("/")
async def root():
    return {"status": "Jarvis Backend is running online!"}