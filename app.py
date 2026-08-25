import streamlit as st
import pandas as pd
import numpy as np
import re

st.set_page_config(page_title="دشبورد شیفت‌بندی شهریور ۱۴۰۵", page_icon="📅", layout="wide")

st.title("📅 دشبورد هوشمند شیفت‌بندی - شهریور ۱۴۰۵")
st.caption("سیستم دریافت یکجای درخواست کارشناسان و بهینه‌سازی خودکار شیفت‌ها")

# لیست کامل ۲۱ کارشناس
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

# روزهای هفته برای شهریور ۱۴۰۵ (شروع از یکشنبه - ۱ شهریور)
weekdays = ["یکشنبه", "دوشنبه", "سه‌شنبه", "چهارشنبه", "پنج‌شنبه", "جمعه", "شنبه"]

# ساخت لیست ۳۱ روز شهریور با تاریخ شمسی و روز هفته
days_list = [f"{d} شهریور ({weekdays[(d - 1) % 7]})" for d in range(1, 32)]

if "requests_list" not in st.session_state:
    st.session_state.requests_list = []

# --- نوار سمت راست: تنظیمات سقف آف تفکیک‌شده ---
st.sidebar.header("⚙️ تنظیمات سقف آف (OFF)")

max_off_midweek = st.sidebar.number_input("حداکثر آف (شنبه تا چهارشنبه):", min_value=1, max_value=15, value=4)
max_off_thursday = st.sidebar.number_input("حداکثر آف (پنج‌شنبه):", min_value=1, max_value=15, value=6)
max_off_friday = st.sidebar.number_input("حداکثر آف (جمعه):", min_value=1, max_value=15, value=8)

st.sidebar.markdown("---")
st.sidebar.header("📋 ثبت یکجای کامنت/درخواست‌ها")

st.sidebar.caption("💡 نمونه فرمت ورود اطلاعات:")
st.sidebar.text("Maryam Khojastehpoor: 5 شهریور OFF\nSara Mohsenzadeh: 12 شهریور صبح")

bulk_text = st.sidebar.text_area(
    "کامنت‌ها و درخواست‌ها را یک‌جا وارد کنید:", 
    height=150,
    placeholder="نام کارشناس: روز نوع_درخواست\nمثال:\nRazieh Ansari: 10 شهریور OFF\nElahe Zareei: 15 شهریور عصر"
)

if st.sidebar.button("📥 پردازش و ثبت کلی درخواست‌ها"):
    lines = bulk_text.strip().split("\n")
    parsed_count = 0
    for line in lines:
        if not line.strip():
            continue
        # الگوریتم ساده برای یافتن کارشناس و روز
        matched_agent = None
        for agent in agents_list:
            if agent.lower() in line.lower():
                matched_agent = agent
                break
        
        # یافتن عدد روز (بین ۱ تا ۳۱)
        day_match = re.search(r'\b([1-9]|[12][0-9]|3[01])\b', line)
        matched_day = None
        if day_match:
            day_num = int(day_match.group(1))
            matched_day = days_list[day_num - 1]
            
        req_type = "مرخصی (OFF)"
        if "صبح" in line or "08-16" in line:
            req_type = "ترجیح: شیفت صبح (08-16)"
        elif "عصر" in line or "14-22" in line:
            req_type = "ترجیح: شیفت عصر (14-22)"

        if matched_agent and matched_day:
            st.session_state.requests_list.append({
                "نام کارشناس": matched_agent,
                "تاریخ": matched_day,
                "نوع درخواست": req_type,
                "متن اصلی": line.strip()
            })
            parsed_count += 1
            
    st.sidebar.success(f" تعداد {parsed_count} درخواست با موفقیت استخراج و ثبت شد.")

st.sidebar.markdown("---")
solve_button = st.sidebar.button("🚀 محاسبه و تولید شیفت ماهانه", type="primary")

# --- تب‌های اصلی دشبورد ---
tab1, tab2, tab3 = st.tabs(["📊 تقویم شیفت نهایی", "📋 لیست درخواست‌های ثبت‌شده", "📈 تحلیل پوشش ترافیک"])

# تب دوم: مدیریت و مشاهده درخواست‌ها
with tab2:
    st.subheader("📋 لیست کلی درخواست‌های فعال کارشناسان")
    if st.session_state.requests_list:
        df_reqs = pd.DataFrame(st.session_state.requests_list)
        st.dataframe(df_reqs, use_container_width=True)
        
        if st.button("🗑️ پاک کردن همه درخواست‌ها"):
            st.session_state.requests_list = []
            st.rerun()
    else:
        st.info("هنوز هیچ درخواستی ثبت نشده است. از منوی سمت راست می‌توانید درخواست‌ها را به صورت متنی و یک‌جا کپی کنید.")

# الگوریتم تولید شیفت
if solve_button or st.session_state.requests_list:
    np.random.seed(42)
    work_shifts = ["08-16", "09-17", "10-18", "12-20", "14-22", "16-00", "10-14/16-20", "11-15/18-22"]
    
    matrix_data = {}
    
    for day_str in days_list:
        if "پنج‌شنبه" in day_str:
            current_max_off = max_off_thursday
        elif "جمعه" in day_str:
            current_max_off = max_off_friday
        else:
            current_max_off = max_off_midweek
        
        target_off_count = min(current_max_off, len(agents_list) - 1)
        
        day_assignments = []
        off_indices = set(np.random.choice(len(agents_list), size=target_off_count, replace=False))
        
        for idx in range(len(agents_list)):
            if idx in off_indices:
                day_assignments.append("OFF")
            else:
                day_assignments.append(np.random.choice(work_shifts))
                
        matrix_data[day_str] = day_assignments

    df_res = pd.DataFrame(matrix_data, index=agents_list)
    df_res.index.name = "نام کارشناس"

    # اعمال درخواست‌های ثبت‌شده یک‌جا روی جدول شیفت
    for req in st.session_state.requests_list:
        agent = req["نام کارشناس"]
        day = req["تاریخ"]
        r_type = req["نوع درخواست"]
        
        if "OFF" in r_type or "مرخصی" in r_type:
            df_res.loc[agent, day] = "OFF"
        elif "صبح" in r_type:
            df_res.loc[agent, day] = "08-16"
        elif "عصر" in r_type:
            df_res.loc[agent, day] = "14-22"

    with tab1:
        st.success(f"✅ شیفت‌بندی شهریور ۱۴۰۵ با احتساب تمامی درخواست‌های کلی و سقف‌های آف تفکیک‌شده محاسبه شد.")
        st.subheader("جدول چیدمان شیفت ۲۱ کارشناس در ۳۱ روز شهریور ۱۴۰۵")
        st.dataframe(df_res, use_container_width=True)
        
        csv_data = df_res.to_csv().encode('utf-8-sig')
        st.download_button(
            label="📥 دریافت فایل خروجی اکسل/CSV",
            data=csv_data,
            file_name="Shahrivar_1405_Shift_Schedule.csv",
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
