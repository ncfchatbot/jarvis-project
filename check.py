import requests

# วาง API KEY ของคุณตรงนี้
API_KEY = "AIzaSyDcVVeVjfVjtjumwgEjZvux2hgUgXyZRQE"

url = f"https://generativelanguage.googleapis.com/v1beta/models?key={API_KEY.strip()}"
try:
    response = requests.get(url).json()
    print("🎯 รายชื่อโมเดลทั้งหมดที่คุณสามารถใช้งานได้:")
    print("-" * 50)
    
    found = False
    for m in response.get('models', []):
        # คัดมาเฉพาะโมเดลที่ใช้คุยตอบโต้ (generateContent) ได้
        if 'generateContent' in m.get('supportedGenerationMethods', []):
            print(f"👉 {m['name']}")
            found = True
            
    if not found:
        print("❌ ไม่พบโมเดลที่รองรับการสนทนาเลย (สิทธิ์ API Key อาจมีปัญหา)")
except Exception as e:
    print(f"❌ เกิดข้อผิดพลาดในการเชื่อมต่อ: {e}")