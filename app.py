import datetime
import pandas as pd
import streamlit as st

# 1. ตั้งค่าหัวข้อเว็บและคำทักทาย
st.title("แอปพลิเคชันทำนายดวงชะตาจากปีเกิด 🔮")
st.write("สวัสดีครับ! ยินดีต้อนรับสู่โปรแกรมดูดวงประจำปีนี้")

# ฟังก์ชันสำหรับโหลดข้อมูลจาก Excel พร้อมทำ Caching เพื่อไม่ให้โหลดใหม่ทุกครั้งที่กดปุ่ม
@st.cache_data
def load_data():
    # หากไฟล์ database.xlsx อยู่ใน GitHub โฟลเดอร์เดียวกับโค้ดตอน Deploy สามารถเรียกชื่อไฟล์ตรงๆ ได้เลย
    file_path = "database.xlsx"
    
    # หมายเหตุ: หากต้องการดึงข้าม Repository สามารถเปลี่ยน file_path เป็น URL แบบ Raw ได้ เช่น:
    # file_path = "https://raw.githubusercontent.com/USERNAME/REPO_NAME/main/database.xlsx"
    
    df = pd.read_excel(file_path)
    return df

try:
    df_fortune = load_data()
    data_loaded = True
except Exception as e:
    st.error(f"ไม่สามารถโหลดไฟล์ database.xlsx ได้ กรุณาตรวจสอบการวางไฟล์บน GitHub: {e}")
    data_loaded = False

if data_loaded:
    # 2. สร้างช่องกรอกข้อมูล (อายุ วันเดือนปีเกิด)
    st.subheader("กรอกข้อมูลของคุณเพื่อเริ่มทำนาย")

    age = st.number_input("อายุปัจจุบัน (ปี)", min_value=1, max_value=120, value=25)

    # กำหนดช่วงวันที่ให้เลือกเฉพาะปี 1950 ถึง 2017 ตามที่ต้องการ
    min_date = datetime.date(1950, 1, 1)
    max_date = datetime.date(2017, 12, 31)
    default_date = datetime.date(1995, 1, 1)

    birth_date = st.date_input(
        "วัน เดือน ปีเกิดของคุณ",
        value=default_date,
        min_value=min_date,
        max_value=max_date
    )

    # ดึงค่า "ปี ค.ศ." ออกมาจากวันที่ผู้ใช้เลือก เพื่อนำไปเทียบกับคอลัมน์ years
    selected_year = birth_date.year

    # 3. สร้างปุ่มกดทำนายดวง
    if st.button("🔮 กดเพื่อทำนายดวงปีนี้"):
        with st.spinner("กำลังค้นหาคำทำนายจากปีเกิดของคุณ..."):
            # ค้นหาแถวใน DataFrame ที่คอลัมน์ 'years' ตรงกับปีที่เลือก
            matched_row = df_fortune[df_fortune['years'] == selected_year]
            
            if not matched_row.empty:
                # ดึงข้อความคำทำนายจากคอลัมน์ที่ 2 (สมมติว่าชื่อคอลัมน์ 'fortune' หรือดึงจากคอลัมน์ที่ index=1)
                # .iloc[0, 1] หมายถึง แถวแรกที่เจอ และคอลัมน์ที่ 2
                my_fortune = matched_row.iloc[0, 1]
                
                st.success("✨ ผลการทำนายดวงของคุณปีนี้ ✨")
                st.info(f"ผู้ใช้งานอายุ {age} ปี (เกิดปี ค.ศ. {selected_year})")
                st.markdown(f"### > **คำทำนาย:** {my_fortune}")
            else:
                st.warning(f"ไม่พบข้อมูลคำทำนายสำหรับปี ค.ศ. {selected_year} ในระบบ")
