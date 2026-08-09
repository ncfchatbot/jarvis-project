import pandas as pd
import chromadb
import os

CSV_FILE = "jarvis_memory.csv"
DB_DIR = "jarvis_brain_db" # ชื่อโฟลเดอร์ที่จะเก็บสมองของ Jarvis

def build_vector_db():
    if not os.path.exists(CSV_FILE):
        print(f"❌ ไม่พบไฟล์ {CSV_FILE}")
        return

    print("🧠 กำลังเตรียมสร้างโครงสร้างสมองให้ Jarvis...")
    
    # อ่านข้อมูล 54 รายการที่เราสกัดมา
    df = pd.read_csv(CSV_FILE)
    memories = df['memory_text'].tolist()
    
    # สร้างฐานข้อมูล Vector (บันทึกลงในคอมพิวเตอร์ของคุณ)
    client = chromadb.PersistentClient(path=DB_DIR)
    
    # สร้าง Collection (เปรียบเสมือนแฟ้มเก็บความทรงจำ)
    # ถ้ามีแฟ้มเดิมอยู่แล้ว ระบบจะลบของเก่าทิ้งเพื่ออัปเดตของใหม่
    try:
        client.delete_collection(name="personal_memory")
    except Exception:
        pass # ถ้ายังไม่มีแฟ้มก็ปล่อยผ่าน
        
    collection = client.create_collection(name="personal_memory")
    
    # เตรียมรหัส ID ให้แต่ละความทรงจำ
    ids = [str(i) for i in range(len(memories))]
    
    print(f"🔄 กำลังแปลงข้อความ {len(memories)} รายการเป็นเส้นประสาทความทรงจำ (Vectors)...")
    print("⏳ ขั้นตอนนี้อาจใช้เวลาสักครู่ (ถ้าเป็นการรันครั้งแรก ระบบอาจมีโหลดโมเดลเล็กๆ เพิ่มเติมอัตโนมัติ)")
    
    # นำข้อมูลเข้าสู่สมอง (ChromaDB จะแปลงข้อความให้อัตโนมัติ)
    collection.add(
        documents=memories,
        ids=ids
    )
    
    print("✅ สร้างสมองเสร็จสมบูรณ์! ตอนนี้ Jarvis พร้อมดึงความทรงจำไปใช้งานแล้ว")

if __name__ == '__main__':
    build_vector_db()