#!/bin/bash
# ดับเบิลคลิกไฟล์นี้เพื่อเปิด GUI แนะนำพืช (ครั้งแรกจะติดตั้งไลบรารีให้อัตโนมัติ ใช้เวลา 1-3 นาที)
cd "$(dirname "$0")" || exit 1

if [ ! -f crop_recommender.joblib ]; then
  echo "❌ ไม่พบไฟล์ crop_recommender.joblib — ดาวน์โหลดจาก Colab แล้ววางไว้โฟลเดอร์เดียวกับไฟล์นี้"
  read -n 1 -s -r -p "กดปุ่มใดก็ได้เพื่อปิด..."; exit 1
fi

if [ ! -x .venv/bin/streamlit ]; then
  echo "⏳ ครั้งแรก: กำลังติดตั้งไลบรารี (ต้องต่ออินเทอร์เน็ต)..."
  python3 -m venv .venv || { echo "❌ สร้าง venv ไม่สำเร็จ — ต้องมี Python 3"; read -n 1 -s -r; exit 1; }
  .venv/bin/pip install -q --upgrade pip
  .venv/bin/pip install -q -r requirements.txt || { echo "❌ ติดตั้งไลบรารีไม่สำเร็จ"; read -n 1 -s -r; exit 1; }
fi

# ข้ามหน้าถามอีเมลของ Streamlit ที่ขึ้นตอนรันครั้งแรก
if [ ! -f "$HOME/.streamlit/credentials.toml" ]; then
  mkdir -p "$HOME/.streamlit"
  printf '[general]\nemail = ""\n' > "$HOME/.streamlit/credentials.toml"
fi

echo "🌱 กำลังเปิดโปรแกรม... (เบราว์เซอร์จะเปิดเอง ถ้าไม่เปิดให้ไปที่ http://localhost:8501)"
echo "   ปิดโปรแกรม: กด Ctrl+C ในหน้าต่างนี้ หรือปิดหน้าต่าง Terminal"
.venv/bin/streamlit run app.py --browser.gatherUsageStats false
