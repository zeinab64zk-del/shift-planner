import streamlit as st
import pandas as pd

st.set_page_config(page_title="مدیریت شیفت‌های چت و تماس", layout="wide")

st.title("📋 سامانه مدیریت و برنامه شیفت‌های چت و تماس")

# لیست کلیه ۲۱ کارشناس
all_staff = [
    "Maryam Khojastehpoor", "Parastoo Bolokbashi", "Sara Mohsenzadeh", 
    "Sahar Heidari", "Niayesh Mahdavi", "Amirmahdi Ghasemi", "Elahe Zareei",
    "Sedigheh Ebrahimipour", "Leila Heidary", "Tahereh Gholami", 
    "Fatemeh Yazdani", "Mahsa Kabiri", "Mina Dashti", "Mahboobeh Hasanpour", 
    "Sorena Fotohi", "Razieh Ansari", "Mahdieh Mardani", "Mahdieh Dehghan", 
    "Anis Soliemani", "Parastoo Niazi", "Maryam Ahmadii"
]

default_chat = [
    "Maryam Khojastehpoor", "Parastoo Bolokbashi", "Sara Mohsenzadeh", 
    "Sahar Heidari", "Niayesh Mahdavi", "Amirmahdi Ghasemi", "Elahe Zareei"
]

# پنل جابه‌جایی افراد در ماه‌های مختلف
st.sidebar.header("⚙️ تنظیمات ماه و جابه‌جایی")
selected_month = st.sidebar.selectbox("انتخاب ماه:", [
    "فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور", 
    "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"
])

selected_chat = st.sidebar.multiselect(
    "کارشناسان بخش چت:", 
    options=all_staff, 
    default=default_chat
)

selected_call = [person for person in all_staff if person not in selected_chat]

# ۱. نمایش اعضای دو تیم
st.subheader(f"👥 تفکیک اعضای تیم برای ماه {selected_month}")
col1, col2 = st.columns(2)

with col1:
    st.success(f"**بخش چت ({len(selected_chat)} نفر)**")
    st.dataframe(pd.DataFrame({"کارشناس چت": selected_chat}), use_container_width=True)

with col2:
    st.info(f"**بخش تماس ({len(selected_call)} نفر)**")
    st.dataframe(pd.DataFrame({"کارشناس تماس": selected_call}), use_container_width=True)

st.markdown("---")

# ۲. جدول دقیق شیفت‌های کاری (تولید شیفت‌ها)
st.subheader(f"📅 جدول برنامه‌ریزی شیفت‌های کاری ماه {selected_month}")

# ایجاد برنامه شیفت‌بندی نمونه بر اساس لیست پویای افراد
schedule_list = []

# شیفت‌بندی افراد چت
for i, person in enumerate(selected_chat):
    shift_type = "صبح چت (07:00 - 15:00)" if i % 2 == 0 else "عصر چت (15:00 - 23:00)"
    schedule_list.append({
        "نام کارشناس": person,
        "بخش": "چت",
        "عنوان شیفت": shift_type
    })

# شیفت‌بندی افراد تماس
for i, person in enumerate(selected_call):
    shift_type = "صبح تماس (08:00 - 16:00)" if i % 2 == 0 else "عصر تماس (16:00 - 24:00)"
    schedule_list.append({
        "نام کارشناس": person,
        "بخش": "تماس",
        "عنوان شیفت": shift_type
    })

df_schedule = pd.DataFrame(schedule_list)

# نمایش جدول اصلی شیفت‌ها
st.dataframe(df_schedule, use_container_width=True)
