import streamlit as st
from datetime import datetime

# Cấu hình trang
st.set_page_config(
    page_title="Phần mềm tính tiền gửi tiết kiệm - TS. Vũ Đức Bình",
    layout="wide"
)

# Ảnh banner đầu trang (Hình 1)
# Bạn có thể thay liên kết ảnh bên dưới bằng URL ảnh Kế toán ngân hàng của bạn
st.image("https://images.unsplash.com/photo-1554224155-8d04cb21cd6c", use_container_width=True)

# Tiêu đề chính
st.title("💰 PHẦN MỀM TÍNH TIỀN GỬI TIẾT KIỆM - TS. VŨ ĐỨC BÌNH")
st.caption("Ngày gửi được tính lãi | Ngày rút không tính lãi | Lãi suất năm chia 365 ngày | Lãi suất tháng chia 30 ngày")

st.markdown("---")

# 1. Thông tin khoản tiền gửi
st.header("1️⃣ Thông tin khoản tiền gửi")
col1, col2 = st.columns(2)

with col1:
    so_tien_gui = st.number_input("💵 Số tiền gửi (VNĐ)", min_value=0, value=100000000, step=1000000)
    lai_suat_co_ky_han = st.number_input("📈 Lãi suất có kỳ hạn", value=6.00, step=0.1, format="%.2f")
    don_vi_ls_co_kh = st.selectbox("Đơn vị lãi suất có kỳ hạn", ["Theo năm (%/năm)", "Theo tháng (%/tháng)"])

with col2:
    lai_suat_khong_ky_han = st.number_input("📉 Lãi suất không kỳ hạn", value=0.50, step=0.1, format="%.2f")
    don_vi_ls_khong_kh = st.selectbox("Đơn vị lãi suất không kỳ hạn", ["Theo năm (%/năm)", "Theo tháng (%/tháng)"])
    ky_han_gui = st.number_input("📅 Kỳ hạn gửi (tháng)", min_value=1, value=12, step=1)

# 2. Hình thức nhận lãi
st.header("2️⃣ Hình thức nhận lãi")
hinh_thuc_nhan_lai = st.selectbox("💳 Hình thức nhận lãi", ["Cuối kỳ", "Hàng tháng", "Đầu kỳ"])
phuong_phap_tinh_lai = st.radio("Phương pháp tính lãi trong kỳ", ["Lãi đơn", "Lãi kép"], horizontal=True)

# 3. Thời gian gửi tiền
st.header("3️⃣ Thời gian gửi tiền")
col_guitien1, col_guitien2 = st.columns(2)

with col_guitien1:
    ngay_gui = st.date_input("📅 Ngày khách hàng gửi tiền", datetime.now())

with col_guitien2:
    ngay_rut = st.date_input("📅 Ngày khách hàng rút tiền", datetime.now().replace(year=datetime.now().year + 1))

# Tính toán các thông tin kỳ hạn
so_ngay_thuc_te = (ngay_rut - ngay_gui).days
# Giả định ngày đáo hạn kỳ đầu là cộng theo số tháng kỳ hạn
try:
    ngay_dao_han_dau = ngay_gui.replace(year=ngay_gui.year + (ngay_gui.month + ky_han_gui - 1) // 12, 
                                        month=(ngay_gui.month + ky_han_gui - 1) % 12 + 1)
except Exception:
    ngay_dao_han_dau = ngay_gui

# 4. Thông tin kỳ hạn
st.header("4️⃣ Thông tin kỳ hạn")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Ngày gửi", ngay_gui.strftime("%d/%m/%Y"))
c2.metric("Ngày đáo hạn kỳ đầu", ngay_dao_han_dau.strftime("%d/%m/%Y"))
c3.metric("Ngày rút", ngay_rut.strftime("%d/%m/%Y"))
c4.metric("Số ngày thực tế", f"{so_ngay_thuc_te} ngày")

if ngay_rut == ngay_dao_han_dau:
    st.success("✅ Rút đúng ngày đáo hạn kỳ đầu. Khách hàng được hưởng lãi suất có kỳ hạn.")
elif ngay_rut < ngay_dao_han_dau:
    st.warning("⚠️ Rút trước hạn. Toàn bộ tiền gửi sẽ tính theo lãi suất không kỳ hạn.")
else:
    st.info("ℹ️ Rút sau hạn. Phần quá hạn sẽ áp dụng lãi suất không kỳ hạn.")

# 5. Lãi suất áp dụng
st.header("5️⃣ Lãi suất áp dụng")
ls1, ls2, ls3 = st.columns(3)
ls1.metric("Lãi suất có kỳ hạn", f"{lai_suat_co_ky_han:.2f}%/năm")
ls2.metric("Lãi suất không kỳ hạn", f"{lai_suat_khong_ky_han:.2f}%/năm")

lai_thuc_te = lai_suat_co_ky_han if ngay_rut >= ngay_dao_han_dau else lai_suat_khong_ky_han
ls3.metric("Lãi suất thực tế", f"{lai_thuc_te:.2f}%/năm")

st.info(f"Đang áp dụng: **Lãi suất {'có kỳ hạn' if ngay_rut >= ngay_dao_han_dau else 'không kỳ hạn'} — {lai_thuc_te:.2f}%/năm**. Mẫu số tính lãi: **365 ngày**.")

st.markdown("---")

# Nút tính tiền lãi
if st.button("🧮 TÍNH TIỀN LÃI", use_container_width=True, type="primary"):
    # Công thức tính lãi đơn cuối kỳ đơn giản
    tien_lai = so_tien_gui * (lai_thuc_te / 100) * (so_ngay_thuc_te / 365)
    tong_tien = so_tien_gui + tien_lai
    
    st.balloons()
    st.subheader("📊 KẾT QUẢ TÍNH LÃI")
    res_col1, res_col2 = st.columns(2)
    res_col1.metric("💰 Tiền lãi thu được", f"{tien_lai:,.0f} VNĐ")
    res_col2.metric("🏦 Tổng số tiền nhận được", f"{tong_tien:,.0f} VNĐ")

st.caption("🪵 Ứng dụng tính lãi tiền gửi tiết kiệm | Lãi suất năm chia 365 ngày, lãi suất tháng chia 30 ngày | Ngày gửi tính lãi, ngày rút không tính lãi")
