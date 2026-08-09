import os
import sys

# [สำคัญ] บังคับให้ระบบ Windows ใช้ภาษา UTF-8 ป้องกัน Error ภาษาไทย
os.environ["PYTHONUTF8"] = "1"
os.environ["PYTHONIOENCODING"] = "utf-8"

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from google import genai 

# ป้องกัน Terminal แสดงผลภาษาไทยเป็นตัวหนังสือต่างดาว
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

app = FastAPI()

# เปิดทางให้หน้าเว็บคุยกับหลังบ้าน
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
        # เชื่อมต่อสมอง Gemini (อย่าลืมเปลี่ยน API Key ของเจ้านายตรงนี้นะครับ)
        client = genai.Client(api_key="AIzaSyDcVVeVjfVjtjumwgEjZvux2hgUgXyZRQE")
        
        sys_instruct = "You are Jarvis, an advanced voice-enabled AI assistant. You MUST strictly reply in the Thai language, provide direct answers with real-time data when asked, be concise, and always call the user 'เจ้านาย'. Never say you cannot speak; you are fully capable of voice communication."

        # ส่งคำถามไปให้ Gemini ประมวลผล พร้อมเปิดเครื่องมือค้นหา Google Search ในตัว
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_message,
            config=dict(
                system_instruction=sys_instruct,
                tools=[{"google_search": {}}]  # <--- คำสั่งบังคับให้ไปค้นข้อมูลสดๆ จากอินเทอร์เน็ต
            )
        )
        
        reply_message = response.text
        return {"response": reply_message}
        
    except Exception as e:
        print(f"เกิดข้อผิดพลาดในระบบ AI: {e}")
        return {"response": "ขออภัยครับเจ้านาย ระบบประมวลผลหลังบ้านขัดข้องครับ"}

ui_path = "jarvis-ui/dist"
if os.path.exists(ui_path):
    app.mount("/", StaticFiles(directory=ui_path, html=True), name="ui")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)