import os
from bs4 import BeautifulSoup
import pandas as pd

HTML_FILE = "MyActivity.html"
CSV_FILE = "jarvis_memory.csv"

def process_memory():
    if not os.path.exists(HTML_FILE):
        print(f"❌ หาไฟล์ {HTML_FILE} ไม่เจอครับ! ก๊อปปี้มาไว้โฟลเดอร์เดียวกันหรือยังเอ่ย?")
        return

    print("⏳ กำลังอ่านไฟล์ความทรงจำ... อาจใช้เวลาแป๊บนึงนะครับ")
    
    with open(HTML_FILE, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    # ค้นหาข้อความทั้งหมดในไฟล์
    # ปกติ Google Takeout จะเก็บใน div class="content-cell"
    cells = soup.find_all('div')
    
    memories = []
    for cell in cells:
        text = cell.get_text(separator=" ", strip=True)
        # คัดกรองเอาเฉพาะข้อความยาวๆ ที่น่าจะเป็นความรู้ หรือ Prompt ที่พิมพ์
        if len(text) > 50 and "http" not in text and "Activity" not in text:
            if text not in memories: # ป้องกันข้อมูลซ้ำ
                memories.append(text)

    if not memories:
        print("⚠️ ดึงข้อความไม่ได้เลย โครงสร้างไฟล์อาจแปลกไป ลองเปิดไฟล์ MyActivity.html ดูด้วยตาเปล่าก่อนครับ")
        return

    df = pd.DataFrame({'memory_text': memories})
    df.to_csv(CSV_FILE, index=False, encoding='utf-8')
    
    print(f"✅ สกัดความทรงจำสำเร็จ! ได้มาทั้งหมด {len(memories)} รายการ")
    print(f"💾 บันทึกไฟล์ความทรงจำลงใน {CSV_FILE} เรียบร้อย พร้อมเอาไปทำ Vector Database แล้ว!")

if __name__ == '__main__':
    process_memory()