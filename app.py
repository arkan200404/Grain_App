import streamlit as st
import pandas as pd
from datetime import datetime
import os
from streamlit_js_eval import get_geolocation

# ڕێکخستنی لاپەڕە
st.set_page_config(page_title="سیستەمی وەسڵی هەردی", layout="wide")

# ناوی فایلی پاشەکەوتکردن
SAVE_FILE = "all_sales.csv"

# دروستکردنی میمۆری بۆ ژمارەی ڕیزەکان
if 'num_rows' not in st.session_state:
    st.session_state.num_rows = 15

# وەرگرتنی لۆکەیشن
loc = get_geolocation()

st.markdown("""
    <style>
    .stApp { background-color: #f4f4f4; }
    .receipt-container {
        background-color: white; border: 4px solid #000; width: 100%;
        max-width: 1000px; margin: auto; padding: 30px; direction: rtl; color: black !important;
    }
    .stTextInput input { background-color: white !important; color: black !important; border: 2px solid #333 !important; font-weight: bold !important; }
    .stNumberInput input { background-color: #e9ecef !important; color: black !important; border: 2px solid #333 !important; font-weight: bold !important; }
    .header-text { color: white; background-color: #000080; padding: 10px; text-align: center; font-weight: bold; }
    .total-box { margin-top: 20px; border: 4px solid #000; padding: 20px; background-color: #ffcc00; font-size: 35px; font-weight: bold; text-align: left; color: black; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="receipt-container">', unsafe_allow_html=True)

# بەشی سەرەوە
col_h1, col_h2 = st.columns(2)
with col_h1:
    market_name = st.text_input("👤 بەڕێز (ناوی کڕیار):", key="market")
with col_h2:
    today_date = st.text_input("📅 بەروار:", value=datetime.now().strftime("%Y / %m / %d"))

st.markdown("<hr style='border: 2px solid black;'>", unsafe_allow_html=True)

# ناونیشانی ستوونەکان
h1, h2, h3, h4 = st.columns([1.5, 3, 1, 1.5])
h1.markdown('<div class="header-text">بڕی پارە</div>', unsafe_allow_html=True)
h2.markdown('<div class="header-text">جۆری بابەت</div>', unsafe_allow_html=True)
h3.markdown('<div class="header-text">ژمارە</div>', unsafe_allow_html=True)
h4.markdown('<div class="header-text">نرخ</div>', unsafe_allow_html=True)

items_to_save = []
grand_total = 0

# دروستکردنی ڕیزەکان بەپێی ئەو ژمارەیەی لە میمۆری دایە
for i in range(st.session_state.num_rows):
    c1, c2, c3, c4 = st.columns([1.5, 3, 1, 1.5])
    with c4: rate = st.number_input(f"r{i}", min_value=0, step=250, label_visibility="collapsed")
    with c3: qty = st.number_input(f"q{i}", min_value=0, step=1, label_visibility="collapsed")
    with c2: item = st.text_input(f"i{i}", label_visibility="collapsed", placeholder="ناو بنووسە...")
    
    subtotal = qty * rate
    grand_total += subtotal
    with c1: st.markdown(f"<div style='text-align:center; padding-top:10px; font-size:18px; font-weight:bold; color:red; border: 1px solid #ccc; height: 45px; background: #fff;'>{subtotal:,}</div>", unsafe_allow_html=True)
    
    if item and qty > 0:
        items_to_save.append(f"{item}({qty}x{rate})")

# کۆی گشتی
st.markdown(f'<div class="total-box"><span style="float:right;">کۆی گشتی:</span><span>{grand_total:,} دینار</span></div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# دوگمەکانی خوارەوە (دەرەوەی وەسڵەکە)
col_b1, col_b2, col_b3 = st.columns(3)

with col_b1:
    if st.button("➕ زیادکردنی ڕیزی تر"):
        st.session_state.num_rows += 5
        st.rerun()

with col_b2:
    if st.button("💾 تۆمارکردن و سەیڤکردن"):
        if market_name and items_to_save:
            # ئامادەکردنی داتا بۆ سەیڤکردن
            new_data = {
                "ڕێکەوت": today_date,
                "کڕیار": market_name,
                "بابەتەکان": ", ".join(items_to_save),
                "کۆی گشتی": grand_total,
                "لۆکەیشن": f"{loc['coords']['latitude']},{loc['coords']['longitude']}" if loc else "نەزانراو"
            }
            df = pd.DataFrame([new_data])
            # سەیڤکردن لە فایلی CSV (Append)
            if not os.path.isfile(SAVE_FILE):
                df.to_csv(SAVE_FILE, index=False, encoding='utf-8-sig')
            else:
                df.to_csv(SAVE_FILE, mode='a', header=False, index=False, encoding='utf-8-sig')
            st.success("✅ وەسڵەکە سەیڤ کرا لە فۆڵدەری Grain_App")
        else:
            st.error("❌ تکایە ناوی کڕیار و بابەتەکان پڕ بکەرەوە")

with col_b3:
    if os.path.isfile(SAVE_FILE):
        st.download_button("📥 دابەزاندنی هەموو فرۆشەکان (Excel)", data=pd.read_csv(SAVE_FILE).to_csv(index=False).encode('utf-8-sig'), file_name="sales_report.csv")

# پیشاندانی ئەرشیف لە کۆتایی لاپەڕەکە
st.divider()
st.subheader("📊 ئەرشیفی وەسڵە سەیڤکراوەکان")
if os.path.isfile(SAVE_FILE):
    st.dataframe(pd.read_csv(SAVE_FILE).tail(5))