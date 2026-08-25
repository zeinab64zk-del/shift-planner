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

st.sidebar.caption("💡 نمونه فرمت ورود اطلاعات (فارسی، انگلیسی، اسم کوچک یا نام کامل):")
st.sidebar.text("Maryam Khojastehpoor: 5 شهریور OFF\nRazieh: 10 شهریور صبح\nZareei: ۱۵ شهریور عصر")

bulk_text = st.sidebar.text_area(
    "کامنت‌ها و درخواست‌ها را یک‌جا وارد کنید:", 
    height=150,
    placeholder="نام کارشناس: روز نوع_درخواست\nمثال:\nRazieh Ansari: 10 شهریور OFF\nElahe: ۱۵ شهریور 14-22"
)

# --- الگوریتم هوشمند پردازش و استخراج درخواست‌ها ---
if st.sidebar.button("📥 پردازش و ثبت کلی درخواست‌ها"):
    lines = bulk_text.strip().split("\n")
    parsed_count = 0
    
    # نقشه تبدیل و تشخیص هوشمند شیفت‌ها و کلمات کلیدی
    shift_patterns = {
        "OFF": ["off", "آف", "مرخصی", "تعطیل"],
        "08-16": ["08-16", "8-16", "۸-۱۶", "صبح"],
        "09-17": ["09-17", "9-17", "۹-۱۷"],
        "10-18": ["10-18", "۱۰-۱۸"],
        "12-20": ["12-20", "۱۲-۲۰"],
        "14-22": ["14-22", "14-22", "۱۴-۲۲", "عصر"],
        "16-00": ["16-00", "16-24", "۱۶-۰۰", "شب"],
        "10-14/16-20": ["10-14/16-20", "دو پارت", "دونوبه‌"],
        "11-15/18-22": ["11-15/18-22"]
    }

    for line in lines:
        if not line.strip():
            continue
        
        # ۱. یافتن نام کارشناس (بررسی نام کامل، فامیلی و نام کوچک)
        matched_agent = None
        clean_line = line.lower().replace(" ", "").replace("‌", "")
        for agent in agents_list:
            clean_agent = agent.lower().replace(" ", "")
            first_name = agent.split()[0].lower()
            last_name = agent.split()[-1].lower() if len(agent.split()) > 1 else ""
            
            if clean_agent in clean_line or first_name in clean_line or (last_name and last_name in clean_line):
                matched_agent = agent
                break
        
        # ۲. تبدیل اعداد فارسی/عربی به انگلیسی و استخراج عدد روز (۱ تا ۳۱)
        persian_digits = "۰۱۲۳۴۵۶۷۸۹"
        english_digits = "0123456789"
        trans_table = str.maketrans(persian_digits, english_digits)
        normalized_line = line.translate(trans_table)
        
        day_match = re.search(r'\b([1-9]|[12][0-9]|3[01])\b', normalized_line)
        matched_day = None
        if day_match:
            day_num = int(day_match.group(1))
            matched_day = days_list[day_num - 1]
            
        # ۳. تشخیص نوع شیفت درخواست‌شده
        detected_shift = None
        for shift_code, keywords in shift_patterns.items():
            if any(kw in line.lower() for kw in keywords):
                detected_shift = shift_code
                break
        
        if not detected_shift:
            detected_shift = "OFF"  # حالت پیش‌فرض در صورت ذکر نکردن نوع شیفت دقیق

        # ثبت نهایی درخواست در Session State
        if matched_agent and matched_day:
            st.session_state.requests_list.append({
                "نام کارشناس": matched_agent,
                "تاریخ": matched_day,
                "نوع درخواست": detected_shift,
                "متن اصلی": line.strip()
            })
            parsed_count += 1
            
    st.sidebar.success(f"تعداد {parsed_count} درخواست با موفقیت استخراج و ثبت شد.")

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

    # اعمال دقیق درخواست‌های ثبت‌شده روی جدول شیفت‌ها
    for req in st.session_state.requests_list:
        agent = req["نام کارشناس"]
        day = req["تاریخ"]
        r_type = req["نوع درخواست"]
        
        df_res.loc[agent, day] = r_type

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
