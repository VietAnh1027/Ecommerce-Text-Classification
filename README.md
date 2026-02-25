# API Phân loại hàng hóa dựa trên mô tả

Dự án này sử dụng mô hình BERT đã được fine-tune để phân loại hàng hóa dựa trên mô tả, được triển khai dưới dạng gọi API để sử dụng

## Hướng dẫn cài đặt và sử dụng

**Bước 1**: Clone repository

Mở cmd, di chuyển đến thư mục muốn chứa repo và thực thi lệnh sau
```bash
git clone https://github.com/VietAnh1027/Ecommerce-Text-Classification.git
cd Ecommerce-Text-Classification
```

**Bước 2**: Cài đặt thư viện cần thiết
```bash
pip install -r requirements.txt
```

**Bước 3**: Chạy server

Lần đầu chạy ứng dụng sẽ hơi lâu do phải cài đặt model từ hugging face hub, những lần chạy sau sẽ không cần cài đặt thư mục model nữa
```bash
uvicorn app:app --reload
```
