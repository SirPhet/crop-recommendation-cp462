"""
Crop Recommendation System — GUI (CP462 Part 2)

รันบนเครื่อง:   pip install -r requirements.txt  แล้ว  streamlit run app.py
ต้องมี crop_recommender.joblib (ดาวน์โหลดจาก Colab) อยู่โฟลเดอร์เดียวกับไฟล์นี้
"""
from pathlib import Path

import joblib
import pandas as pd
import streamlit as st

from crop_icons import CROP_SVG, CROP_TH

MODEL_PATH = Path(__file__).parent / "crop_recommender.joblib"

# (ชื่อไทย, หน่วย, min, max, ค่าเริ่มต้น, step) — ช่วงตามชุดข้อมูล
FEATURES = {
    "N":           ("ไนโตรเจน (N)",    "",   0.0, 140.0, 90.0, 1.0),
    "P":           ("ฟอสฟอรัส (P)",    "",   5.0, 145.0, 42.0, 1.0),
    "K":           ("โพแทสเซียม (K)",  "",   5.0, 205.0, 43.0, 1.0),
    "temperature": ("อุณหภูมิ",        "°C", 8.8, 43.7, 20.9, 0.1),
    "humidity":    ("ความชื้น",        "%",  14.3, 100.0, 82.0, 0.1),
    "ph":          ("ค่า pH ดิน",      "",   3.5, 9.9, 6.5, 0.1),
    "rainfall":    ("ปริมาณฝน",        "mm", 20.2, 298.6, 202.9, 0.1),
}

st.set_page_config(page_title="แนะนำพืช · Crop Recommendation", page_icon="🌱", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Kanit:wght@400;500;600&family=IBM+Plex+Sans+Thai:wght@400;600&display=swap');
html, body, [class*="css"], .stMarkdown, .stNumberInput label, button { font-family: 'IBM Plex Sans Thai', sans-serif; }
.stApp { background: #F8F5EE; }
.block-container { padding-top: 2rem; max-width: 1200px; }
h1, h2, h3, .hero h1 { font-family: 'Kanit', sans-serif !important; }
.hero { background: #16261C; color: #F8F5EE; border-radius: 24px; padding: 28px 32px; margin-bottom: 24px; }
.hero h1 { color: #F8F5EE; margin: 0; font-size: 2.1rem; font-weight: 600; }
.hero p { color: #C9D6C3; margin: 6px 0 0; }
.panel-title { font-family: 'Kanit', sans-serif; font-size: 1.25rem; font-weight: 500; color: #16261C; margin: 0 0 8px; }
.best { background: #fff; border: 2px solid #5E8A50; border-radius: 24px; padding: 24px; display: flex; gap: 24px; align-items: center; }
.best .icon { width: 150px; height: 150px; flex: none; background: #EEF4E8; border-radius: 28px; padding: 16px; box-sizing: border-box; }
.best .rank { font-size: .85rem; letter-spacing: .1em; color: #5E8A50; font-weight: 600; }
.best .th { font-family: 'Kanit', sans-serif; font-size: 2.4rem; font-weight: 600; color: #16261C; line-height: 1.1; }
.best .en { color: #6B7A6E; font-size: 1.05rem; }
.bar { height: 12px; background: #E6E2D6; border-radius: 99px; overflow: hidden; margin-top: 12px; }
.bar > div { height: 100%; background: #5E8A50; border-radius: 99px; }
.pct { font-family: 'Kanit', sans-serif; font-size: 1.3rem; color: #16261C; margin-top: 6px; }
.runner { background: #fff; border: 1px solid #E6E2D6; border-radius: 20px; padding: 16px; display: flex; gap: 16px; align-items: center; margin-top: 14px; }
.runner .icon { width: 72px; height: 72px; flex: none; background: #F3F1EA; border-radius: 16px; padding: 8px; box-sizing: border-box; }
.runner .th { font-family: 'Kanit', sans-serif; font-size: 1.3rem; color: #16261C; }
.runner .en { color: #6B7A6E; font-size: .9rem; }
.runner .bar > div { background: #A9C49A; }
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(104px, 1fr)); gap: 12px; }
.tile { background: #fff; border: 1px solid #E6E2D6; border-radius: 16px; padding: 10px 6px; text-align: center; opacity: .55; }
.tile.on { opacity: 1; border: 2px solid #5E8A50; background: #F1F7EC; }
.tile svg { width: 56px; height: 56px; }
.tile .th { font-size: .9rem; color: #16261C; margin-top: 4px; }
.tile .p { font-size: .75rem; color: #5E8A50; font-weight: 600; }
.note { color: #6B7A6E; font-size: .85rem; margin-top: 18px; }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_model():
    saved = joblib.load(MODEL_PATH)  # {"model": Pipeline, "label_encoder": ..., "features": [...]}
    return saved["model"], saved["label_encoder"], saved["features"]


def html(s: str) -> None:
    """แสดง HTML (ตัดช่องว่างหน้าบรรทัด กัน markdown ตีความเป็น code block)"""
    st.markdown("\n".join(line.strip() for line in s.splitlines()), unsafe_allow_html=True)


def predict_proba(values: dict) -> pd.Series:
    model, label_encoder, features = load_model()
    X = pd.DataFrame([[values[f] for f in features]], columns=features)
    proba = model.predict_proba(X)[0] * 100
    return pd.Series(proba, index=label_encoder.classes_).sort_values(ascending=False)


html("""
<div class="hero">
  <h1>🌱 ระบบแนะนำพืชจากค่าดินและอากาศ</h1>
  <p>กรอกผลตรวจดินและสภาพอากาศของแปลง → โมเดล Random Forest แนะนำพืช 3 อันดับ (Test accuracy 99.5%) · CP462 Part 2</p>
</div>
""")

if not MODEL_PATH.exists():
    st.error(f"ไม่พบไฟล์โมเดล `{MODEL_PATH.name}` — ดาวน์โหลดจาก Colab แล้ววางไว้โฟลเดอร์เดียวกับ app.py")
    st.stop()

left, right = st.columns([1, 1.6], gap="large")

with left:
    st.markdown('<p class="panel-title">ข้อมูลแปลง</p>', unsafe_allow_html=True)
    values = {}
    st.caption("ธาตุอาหารในดิน")
    for f in ["N", "P", "K"]:
        label, unit, lo, hi, default, step = FEATURES[f]
        values[f] = st.slider(label, lo, hi, default, step, key=f)
    st.caption("สภาพอากาศและดิน")
    for f in ["temperature", "humidity", "ph", "rainfall"]:
        label, unit, lo, hi, default, step = FEATURES[f]
        values[f] = st.slider(f"{label} ({unit})" if unit else label, lo, hi, default, step, key=f)

proba = predict_proba(values)
top3 = proba.head(3)

with right:
    st.markdown('<p class="panel-title">พืชที่แนะนำ</p>', unsafe_allow_html=True)
    best_name, best_p = top3.index[0], top3.iloc[0]
    html(f"""
<div class="best">
  <div class="icon">{CROP_SVG[best_name]}</div>
  <div style="flex:1">
    <div class="rank">อันดับ 1</div>
    <div class="th">{CROP_TH[best_name]}</div>
    <div class="en">{best_name}</div>
    <div class="bar"><div style="width:{best_p:.0f}%"></div></div>
    <div class="pct">ความมั่นใจ {best_p:.1f}%</div>
  </div>
</div>""")

    cols = st.columns(2)
    for i, (name, p) in enumerate(top3.iloc[1:].items()):
        with cols[i]:
            html(f"""
<div class="runner">
  <div class="icon">{CROP_SVG[name]}</div>
  <div style="flex:1">
    <div class="en">อันดับ {i + 2}</div>
    <div class="th">{CROP_TH[name]} <span class="en">{name}</span></div>
    <div class="bar"><div style="width:{max(p, 1):.0f}%"></div></div>
    <div class="en">{p:.1f}%</div>
  </div>
</div>""")

    if best_p < 50:
        st.warning("ความมั่นใจต่ำกว่า 50% — ค่าที่กรอกอาจไม่ตรงกับสภาพที่พืชชนิดใดในระบบชอบ ควรใช้ผลนี้อย่างระมัดระวัง")

st.markdown('<p class="panel-title" style="margin-top:28px">พืชทั้ง 22 ชนิดในระบบ</p>', unsafe_allow_html=True)
tiles = "".join(
    f'<div class="tile{" on" if name in top3.index else ""}">{CROP_SVG[name]}'
    f'<div class="th">{CROP_TH[name]}</div><div class="p">{proba[name]:.0f}%</div></div>'
    for name in sorted(CROP_SVG, key=lambda n: -proba[n])
)
st.markdown(f'<div class="grid">{tiles}</div>', unsafe_allow_html=True)

st.markdown('<p class="note">หมายเหตุ: โมเดลบอกว่าสภาพแปลง “คล้าย” พืชชนิดใดในชุดข้อมูล 22 ชนิด '
            'ไม่ได้รับประกันผลผลิตหรือกำไร — ใช้ประกอบการตัดสินใจเท่านั้น · ภาพพืชเป็นภาพเวกเตอร์วาดประกอบ</p>',
            unsafe_allow_html=True)
