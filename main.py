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

    # ใช้ Endpoint ใหม่ล่าสุด และโมเดล 2.0-flash ที่รองรับ API Key ใหม่ 100%
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
    
    # โครงสร้าง JSON ตามมาตรฐานใหม่ของ Google
    payload = {
        "system_instruction": {
            "parts": [{"text": "You are Jarvis, an advanced AI assistant. You MUST strictly reply in Thai."}]
        },
        "contents": [
            {"role": "user", "parts": [{"text": user_message}]}
        ]
    }
    
    data = json.dumps(payload).encode('utf-8')
    headers = {'Content-Type': 'application/json'}
    req = urllib.request.Request(url, data=data, headers=headers)

    try:
        # ยิงคำสั่งเข้าเซิร์ฟเวอร์
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            text_response = result['candidates'][0]['content']['parts'][0]['text']
            return {"response": text_response}
            
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        return {"response": f"เซิร์ฟเวอร์ Google ปฏิเสธครับ: {e.code} - {error_body}"}
    except Exception as e:
        return {"response": f"ระบบขัดข้องภายในครับ: {str(e)}"}

@app.get("/")
async def root():
    return {"status": "Jarvis New API Backend is running online!"}