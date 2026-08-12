import os
import json
import urllib.request
import urllib.error
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# อนุญาตให้หน้าเว็บสีฟ้าเชื่อมต่อเข้ามา
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

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return {"response": "Error: ไม่พบ API Key ในระบบหลังบ้านครับ"}

    # ลับเฉพาะ: ยิงคำสั่งตรงเข้าเซิร์ฟเวอร์ AI ของ Google โดยไม่ใช้ SDK
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    
    # จัดเตรียมข้อมูลคำสั่ง
    payload = {
        "systemInstruction": {
            "parts": [{"text": "You are Jarvis, an advanced AI assistant. You MUST strictly reply in Thai."}]
        },
        "contents": [
            {"role": "user", "parts": [{"text": user_message}]}
        ]
    }
    
    # แปลงข้อมูลเป็นรูปแบบที่เซิร์ฟเวอร์เข้าใจ
    data = json.dumps(payload).encode('utf-8')
    headers = {'Content-Type': 'application/json'}
    req = urllib.request.Request(url, data=data, headers=headers)

    try:
        # ส่งคำสั่งและรอรับข้อความตอบกลับ
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            text_response = result['candidates'][0]['content']['parts'][0]['text']
            return {"response": text_response}
            
    except urllib.error.HTTPError as e:
        # ถ้าพัง คราวนี้จะฟ้อง Error ตรงๆ จากฝั่ง Google 
        error_body = e.read().decode('utf-8')
        return {"response": f"เซิร์ฟเวอร์ Google ปฏิเสธครับ: {e.code} - {error_body}"}
    except Exception as e:
        return {"response": f"ระบบขัดข้องภายในครับ: {str(e)}"}

@app.get("/")
async def root():
    return {"status": "Jarvis Direct API Backend is running online!"}