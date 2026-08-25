import streamlit as st
import pandas as pd

st.set_page_config(page_title="مدیریت شیفت‌های چت و تماس", layout="wide")

st.title("📋 سامانه شیفت‌بندی کارشناسان چت و تماس")

# لیست کامل ۲۱ کارشناس
all_staff = [
    "Maryam Khojastehpoor", "Parastoo Bolokbashi", "Sara Mohsenzadeh", 
    "Sahar Heidari", "Niayesh Mahdavi", "Amirmahdi Ghasemi", "Elahe Zareei",
    "Sedigheh Ebrahimipour", "Leila Heidary", "Tahereh Gholami", 
    "Fatemeh Yazdani", "Mahsa Kabiri", "Mina Dashti", "Mahboobeh Hasanpour", 
    "Sorena Fotohi", "Razieh Ansari", "Mahdieh Mardani", "Mahdieh Dehghan", 
    "Anis Soliemani", "Parastoo Niazi", "Maryam Ahmadii"
]

# اعضای اولیه چت
default_chat = [
    "Maryam Khojastehpoor", "Parastoo Bolokbashi", "Sara Mohsenzadeh", 
    "Sahar Heidari", "Niayesh Mahdavi", "Amirmahdi Ghasemi", "Elahe Zareei"
]

# تنظیمات ماه و انتخاب اعضا در پنل کناری
st.sidebar.header("⚙️ تنظیمات ماه و جابه‌جایی افراد")
selected_month = st.sidebar.selectbox("انتخاب ماه:", [
    "فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور", 
    "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"
])

# قابلیت تغییر و جابه‌جایی افراد چت (افراد باقیمانده خودکار به تماس منتقل می‌شوند)
selected_chat = st.sidebar.multiselect(
    "کارشناسان بخش چت را انتخاب کنید:", 
    options=all_staff, 
    default=default_chat
)

selected_call = [person for person in all_staff if person not in selected_chat]

# نمایش لیست جدید تیم‌ها برای ماه انتخاب‌شده
st.subheader(f"👥 ترکیب تیم‌ها - ماه {selected_month}")
col1, col2 = st.columns(2)

with col1:
    st.success(f"**بخش چت ({len(selected_chat)} نفر)**")
    st.table(pd.DataFrame({"نام کارشناس": selected_chat}))

with col2:
    st.info(f"**بخش تماس ({len(selected_call)} نفر)**")
    st.table(pd.DataFrame({"نام کارشناس": selected_call}))

st.markdown("---")
st.subheader("📅 جدول شیفت‌ها (بر اساس شیفت‌های قبلی)")

# جدول شیفت‌های قبلی بدون دستکاری ساعات
shifts_data = {
    "کانال": ["چت", "تماس"],
    "تعداد نفرات ماه جاری": [len(selected_chat), len(selected_call)],
    "وضعیت شیفت‌بندی": ["شیفت‌های قبلی چت برقرار است", "شیفت‌های قبلی تماس برقرار است"]
}

st.dataframe(pd.DataFrame(shifts_data), use_container_width=True)
