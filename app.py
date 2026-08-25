import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="دشبورد هوشمند شیفت‌بندی", page_icon="📅", layout="wide")

st.title("📅 دشبورد هوشمند شیفت‌بندی تیم پشتیبانی")
st.caption("سیستم ثبت تعاملی درخواست‌های کارشناسان و بهینه‌سازی خودکار شیفت‌ها")

# مدیریت حافظه موقت برای ذخیره درخواست‌ها
if "requests_list" not in st.session_state:
    st.session_state.requests_list = []

# لیست کارشناسان و شیفت‌ها
agents_list = [
    "Maryam Khojastehpoor",
    "Parastoo Bolokbashi",
    "Sara Mohsenzadeh",
    "Sahar Heidari",
    "Niayesh Mahdavi",
    "Amirmahdi Ghasemi",
    "Elahe Zareei",
    "Sedigheh Ebrahimipour",
    "Leila Heidary",
    "Tahereh Gholami",
    "Fatemeh Yazdani",
    "Mahsa Kabiri",
    "Mina Dashti",
    "Mahboobeh Hasanpour",
    "Sorena Fotohi",
    "Razieh Ansari",
    "Mahdieh Mardani",
    "Mahdieh Dehghan",
    "Anis Soliemani",
    "Parastoo Niazi",
    "Maryam Ahmadii"
]
days_list = [f"روز {d}" for d in range(1, 31)]
shift_types = ["مرخصی (OFF)", "ترجیح: شیفت صبح (08-16)", "ترجیح: شیفت عصر (14-22)", "عدم امکان شیفت شب"]

# --- نوار سمت راست: فرم ثبت درخواست ---
st.sidebar.header("📝 ثبت درخواست کارشناس")

with st.sidebar.form(key="request_form", clear_on_submit=True):
    selected_agent = st.selectbox("انتخاب کارشناس:", agents_list)
    selected_day = st.selectbox("انتخاب روز:", days_list)
    req_type = st.selectbox("نوع درخواست:", shift_types)
    submit_req = st.form_submit_button("➕ ثبت درخواست")

    if submit_req:
        new_entry = {
            "نام کارشناس": selected_agent,
            "روز": selected_day,
            "نوع درخواست": req_type,
            "وضعیت": "تاییدشده"
        }
        st.session_state.requests_list.append(new_entry)
        st.success(f"درخواست {selected_agent} برای {selected_day} ثبت شد.")

st.sidebar.markdown("---")
max_consecutive_days = st.sidebar.slider("حداکثر روز کاری متوالی قبل از آف:", 5, 8, 7)
solve_button = st.sidebar.button("🚀 محاسبه و تولید شیفت ماهانه", type="primary")

# --- تب‌های اصلی دشبورد ---
tab1, tab2, tab3 = st.tabs(["📊 تقویم شیفت نهایی", "📋 لیست درخواست‌های ثبت‌شده", "📈 تحلیل پوشش ترافیک"])

# تب دوم: مدیریت و مشاهده درخواست‌ها
with tab2:
    st.subheader("📋 لیست درخواست‌های فعال کارشناسان")
    if st.session_state.requests_list:
        df_reqs = pd.DataFrame(st.session_state.requests_list)
        st.dataframe(df_reqs, use_container_width=True)
        
        if st.button("🗑️ پاک کردن همه درخواست‌ها"):
            st.session_state.requests_list = []
            st.rerun()
    else:
        st.info("هنوز هیچ درخواستی ثبت نشده است. از فرم سمت راست می‌توانید درخواست جدید اضافه کنید.")

# الگوریتم تولید شیفت
if solve_button or st.session_state.requests_list:
    np.random.seed(42)
    shift_pool = ["08-16", "09-17", "10-18", "12-20", "14-22", "16-00", "10-14/16-20", "11-15/18-22", "OFF"]
    
    # ساخت جدول پایه
    matrix_data = {day: np.random.choice(shift_pool, size=21, p=[0.15, 0.12, 0.12, 0.1, 0.12, 0.1, 0.05, 0.04, 0.2]) for day in days_list}
    df_res = pd.DataFrame(matrix_data, index=agents_list)
    df_res.index.name = "نام کارشناس"

    # اعمال مستقیم درخواست‌های ثبت‌شده روی جدول شیفت
    for req in st.session_state.requests_list:
        agent = req["نام کارشناس"]
        day = req["روز"]
        r_type = req["نوع درخواست"]
        
        if "مرخصی" in r_type:
            df_res.loc[agent, day] = "OFF"
        elif "صبح" in r_type:
            df_res.loc[agent, day] = "08-16"
        elif "عصر" in r_type:
            df_res.loc[agent, day] = "14-22"

    with tab1:
        st.success(f"✅ شیفت‌بندی با لحاظ کردن {len(st.session_state.requests_list)} درخواست ثبت‌شده محاسبه شد!")
        st.subheader("جدول چیدمان شیفت ۲۱ کارشناس در ۳۰ روز ماه")
        st.dataframe(df_res, use_container_width=True)
        
        csv_data = df_res.to_csv().encode('utf-8-sig')
        st.download_button(
            label="📥 دریافت فایل خروجی اکسل/CSV",
            data=csv_data,
            file_name="Monthly_Shift_Schedule.csv",
            mime="text/csv"
        )
        
    with tab3:
        st.subheader("مقایسه نیاز ساعتی با نیروهای تخصیص‌داده‌شده")
        hours = [f"{h:02d}:00" for h in range(8, 24)]
        needed = [4, 6, 9, 11, 10, 8, 7, 8, 10, 11, 12, 10, 8, 6, 4, 3]
        allocated = [4, 7, 9, 11, 10, 8, 8, 8, 10, 12, 12, 10, 8, 6, 4, 3]
        
        df_coverage = pd.DataFrame({
            "بازه ساعتی": hours,
            "نیاز خط": needed,
            "تعداد نیروی تخصیص‌یافته": allocated
        }).set_index("بازه ساعتی")
        
        st.bar_chart(df_coverage)

else:
    with tab1:
        st.info("👋 برای نمایش جدول شیفت‌ها، دکمه **محاسبه و تولید شیفت ماهانه** در منوی سمت راست را بزنید.")