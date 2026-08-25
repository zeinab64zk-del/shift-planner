import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="داشبورد مدیریت و شیفت‌بندی پرسنل", layout="wide")

st.title("🗓️ سامانه جامع مدیریت و برنامه‌ریزی شیفت‌ها")

# تنظیمات ماه و پرسنل در پنل کناری
st.sidebar.header("⚙️ تنظیمات شیفت‌بندی")
selected_month = st.sidebar.selectbox("انتخاب ماه:", [
    "فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور", 
    "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"
])

num_days = st.sidebar.slider("تعداد روزهای ماه:", min_value=28, max_value=31, value=31)
num_staff = st.sidebar.number_input("تعداد کل کارشناسان:", min_value=1, max_value=50, value=21)

# تولید لیست کارشناسان
staff_list = [f"کارشناس {i+1}" for i in range(num_staff)]

st.subheader(f"📊 برنامه شیفت کاری ماه {selected_month} ({num_staff} نفر - {num_days} روز)")

# ساخت فریم داده‌ها برای روزهای ماه
days_columns = [f"روز {d}" for d in range(1, num_days + 1)]

# تعریف شیفت‌های اولیه
shift_types = ["صبح", "عصر", "شب", "آف"]

# الگوی توزیع شیفت‌ها
np.random.seed(42)
schedule_data = np.random.choice(shift_types, size=(num_staff, num_days))

df = pd.DataFrame(schedule_data, columns=days_columns, index=staff_list)

# نمایش جدول قابل ویرایش تعاملی
edited_df = st.data_editor(df, use_container_width=True)

# خلاصه وضعیت شیفت‌ها
st.markdown("---")
st.subheader("📈 خلاصه وضعیت شیفت‌ها")

col1, col2, col3, col4 = st.columns(4)
col1.metric("کل کارشناسان", len(edited_df))
col2.metric("تعداد شیفت‌های صبح", (edited_df == "صبح").sum().sum())
col3.metric("تعداد شیفت‌های عصر", (edited_df == "عصر").sum().sum())
col4.metric("تعداد شیفت‌های شب", (edited_df == "شب").sum().sum())
