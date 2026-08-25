import streamlit as st
import random
import pandas as pd

st.title("سیستم چینش خودکار شیفت‌ها")

# ۱. دریافت ورودی تعداد نفرات هر شیفت
st.sidebar.header("تنظیمات تعداد نفرات شیفت")
morning_req = st.sidebar.number_input("تعداد نفرات شیفت صبح", min_value=1, value=4)
evening_req = st.sidebar.number_input("تعداد نفرات شیفت عصر", min_value=1, value=3)
night_req = st.sidebar.number_input("تعداد نفرات شیفت شب", min_value=1, value=2)

# ۲. مشخصات اعضا و روزها
team_members = [f"کارشناس {i}" for i in range(1, 22)]  # ۲۱ نفر
days_in_month = 31

if st.button("چینش خودکار شیفت‌ها"):
    # ساختار ذخیره شیفت‌ها
    schedule = {day: {} for day in range(1, days_in_month + 1)}
    member_shift_count = {member: 0 for member in team_members}

    for day in range(1, days_in_month + 1):
        # اولویت‌دهی به افرادی که شیفت کمتری داشته‌اند
        available_members = sorted(team_members, key=lambda m: member_shift_count[m])
        
        # انتخاب نفرات برای شیفت صبح
        morning_staff = available_members[:morning_req]
        for m in morning_staff:
            member_shift_count[m] += 1
        
        # انتخاب نفرات برای شیفت عصر
        remaining_members = [m for m in available_members if m not in morning_staff]
        evening_staff = remaining_members[:evening_req]
        for m in evening_staff:
            member_shift_count[m] += 1
            
        # انتخاب نفرات برای شیفت شب
        remaining_members = [m for m in remaining_members if m not in evening_staff]
        night_staff = remaining_members[:night_req]
        for m in night_staff:
            member_shift_count[m] += 1
            
        schedule[day] = {
            "صبح": ", ".join(morning_staff),
            "عصر": ", ".join(evening_staff),
            "شب": ", ".join(night_staff)
        }

    df_schedule = pd.DataFrame(schedule).T
    st.write("### جدول شیفت‌بندی پیشنهادی")
    st.dataframe(df_schedule)
