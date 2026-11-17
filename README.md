# 🌱 Crop Recommendation System (CP462)

ระบบแนะนำพืชจากค่าดินและอากาศ (N, P, K, อุณหภูมิ, ความชื้น, pH, ปริมาณฝน) ด้วยโมเดล **Gaussian Naive Bayes** (เลือกจากการเทียบ Logistic Regression, Naive Bayes, Decision Tree และ baseline ด้วย 5-fold CV)
เทรนบนชุดข้อมูล [Crop Recommendation Dataset (Kaggle)](https://www.kaggle.com/datasets/atharvaingle/crop-recommendation-dataset) — 2,200 แถว, 22 พืช
Test accuracy 99.5% · Macro-F1 0.995

## ไฟล์ในโปรเจค
| ไฟล์ | คืออะไร |
|---|---|
| `notebook/CP462_Crop_Recommendation.ipynb` | notebook ตั้งแต่ EDA → preprocessing → CV/GridSearch → ประเมินผล → เซฟโมเดล |
| `crop_recommender.joblib` | โมเดลที่เทรนแล้ว (Pipeline StandardScaler + Gaussian Naive Bayes, LabelEncoder, รายชื่อ features) |
| `app.py` | หน้าเว็บ GUI (Streamlit) กรอกค่าแปลงแล้วได้พืช 3 อันดับ |
| `crop_icons.py` | ภาพเวกเตอร์ (SVG) ของพืชทั้ง 22 ชนิด |
| `เปิดโปรแกรมแนะนำพืช.command` | macOS: ดับเบิลคลิกเพื่อติดตั้งและเปิด GUI |

## รันบนเครื่อง
```bash
pip install -r requirements.txt
streamlit run app.py
```
macOS ดับเบิลคลิก `เปิดโปรแกรมแนะนำพืช.command` ได้เลย

## ข้อจำกัด
ชุดข้อมูลน่าจะไม่ได้เก็บจากแปลงจริงและไม่ใช่ข้อมูลของไทย โมเดลบอกได้ว่าสภาพแปลง "คล้าย" พืชชนิดใด
ไม่ได้รับประกันผลผลิตหรือกำไร — เป็นต้นแบบ (proof of concept) สำหรับวิชา CP462

## ผู้จัดทำ
- นาย พลภัทร เพ็ชรสินธพ
- นาย อภินัทธ์ ยศวราเลิศ
- นาย ชัยสิทธิ์ ปลื้มสุทธิ์
