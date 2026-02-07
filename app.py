import streamlit as st
import pandas as pd
from datetime import datetime
import os
from streamlit_js_eval import get_geolocation

# ڕێکخستنی لاپەڕە
st.set_page_config(page_title="سیستەمی هەردی", layout="wide")

# ناوی فایلی پاشەکەوتکردن
SAVE_FILE = "all_sales.csv"

if 'num_rows' not in st.session_state:
    st.session_state.num_rows = 15

loc = get_geolocation()

# CSS بۆ ناچارکردنی مۆبایل کە ستوونەکان تێکنەدا و ڕێک وەک کۆمپیوتەر بێت
st.markdown("""
    <style>
    /* ناچارکردنی ستوونەکان کە لە تەنیشت یەک بمێننەوە لەسەر مۆبایل */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        align-items: center !important;
        gap: 5px !important;
    }
    [data-testid="column"] {
        min-width: 0px !important;
        flex: 1 1 auto !important;
    }
    
    .stApp { background-color: #f4f4f4; }
    .receipt-container {
        background-color: white; border: 3px solid #000; width: 100%;
        max-width: 900px; margin: auto; padding: 10px; direction: rtl; color: black !important;
    }
    
    /* بچووککردنەوەی فۆنت بۆ ئەوەی لەسەر مۆبایل جێگەی ببێتەوە */
    .stTextInput input, .stNumberInput input {
        font-size: 14px !important;
        padding: 5px !important;
        background-color: white !important;
        color: black !important;
        border: 1px solid #333 !important;
    }
    
    .header-text {
        color: white; background-color: #000080; padding: 5px;
        text-align: center; font-weight: bold; font-size: 12px;
    }
    
    .total-box {
        margin-top: 15px; border: 3px solid #000; padding: 10px;
        background-color: #ffcc00; font-size: 20px; font-weight: bold;
        text-align: left; color: black;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="receipt-container">', unsafe_allow_html=True)

# بەشی سەرەوە
col_h1, col_h2 = st.columns(2)
with col_h1: market_name = st.text_input("👤 بەڕێز:", key="market")
with col_h2: today_date = st.text_input("📅 بەروار:", value=datetime.now().strftime("%Y/%m/%d"))

st.markdown("<hr style='border: 1px solid black; margin: 10px 0;'>", unsafe_allow_html=True)

# ناونیشانی ستوونەکان (بە ڕیز و بە تەنیشت یەک)
h1, h2, h3, h4 = st.columns([1.2, 2.5, 0.8, 1.2])
h1.markdown('<div class="header-text">بڕ</div>', unsafe_allow_html=True)
h2.markdown('<div class="header-text">بابەت</div>', unsafe_allow_html=True)
h3.markdown('<div class="header-text">ژمارە</div>', unsafe_allow_html=True)
h4.markdown('<div class="header-text">نرخ</div>', unsafe_allow_html=True)

items_to_save = []
grand_total = 0

# دروستکردنی ڕیزەکان
for i in range(st.session_state.num_rows):
    c1, c2, c3, c4 = st.columns([1.2, 2.5, 0.8, 1.2])
    with c4: rate = st.number_input(f"r{i}", min_value=0, step=250, label_visibility="collapsed")
    with c3: qty = st.number_input(f"q{i}", min_value=0, step=1, label_visibility="collapsed")
    with c2: item = st.text_input(f"i{i}", label_visibility="collapsed", placeholder="ناو...")
    
    subtotal = qty * rate
    grand_total += subtotal
    with c1: st.markdown(f"<div style='text-align:center; font-size:12px; font-weight:bold; color:red; border: 1px solid #ccc; background: #fff;'>{subtotal:,}</div>", unsafe_allow_html=True)
    
    if item and qty > 0:
        items_to_save.append(f"{item}({qty}x{rate})")

# کۆی گشتی
st.markdown(f'<div class="total-box">کۆی گشتی: {grand_total:,} دینار</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# دوگمەکانی خوارەوە
col_b1, col_b2 = st.columns(2)
with col_b1:
    if st.button("➕ ڕیزی تر"):
        st.session_state.num_rows += 5
        st.rerun()
with col_b2:
    if st.button("💾 سەیڤکردن"):
        if market_name and items_to_save:
            new_data = {"Date": today_date, "Market": market_name, "Items": ", ".join(items_to_save), "Total": grand_total}
            st.success("وەسڵەکە تۆمار کرا!")
        else:
            st.error("تکایە ناوی کڕیار بنووسە")
