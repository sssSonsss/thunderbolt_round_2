# Fruit Analyzer with Gemini

## Mô tả
Ứng dụng GUI bằng Python giúp nhận diện, đếm số lượng và đánh giá độ chín của các loại hoa quả trên kệ từ ảnh, sử dụng Google Gemini API.

## Tính năng
- Chọn ảnh từ máy tính (hỗ trợ PNG, JPG, JPEG)
- Gửi ảnh lên Gemini API để phân tích
- Hiển thị kết quả JSON: loại quả, số lượng, độ chín (unripe, ripe, overripe)
- Tổng hợp số lượng từng loại quả và từng mức độ chín
- Giao diện đơn giản, dễ sử dụng

## Yêu cầu môi trường
- macOS 12 trở lên
- Đã build sẵn ứng dụng (main.app trong thư mục dist)
- API key Gemini hợp lệ đã được cấu hình trong mã nguồn

## Cài đặt & Sử dụng
1. **Giải nén hoặc copy thư mục project vào máy Mac**
2. **Mở thư mục `dist`**
3. **Nhấp đúp vào biểu tượng `main.app` để chạy ứng dụng**
   - Nếu lần đầu mở bị cảnh báo bảo mật, hãy chuột phải vào `main.app` > chọn `Open` > chọn `Open` tiếp trong popup.
4. Sử dụng giao diện:
   - Nhấn **Select Image** để chọn ảnh (PNG, JPG, JPEG)
   - Nhấn **Analyze Image** để phân tích ảnh
   - Xem kết quả JSON trên giao diện

## Cấu trúc file
- `main.py`: Mã nguồn giao diện và xử lý chính (chỉ dùng khi phát triển)
- `dist/main.app`: Ứng dụng đã build, chỉ cần mở để sử dụng
- `README.md`: Hướng dẫn sử dụng

## Ghi chú
- Đảm bảo API key Gemini còn hiệu lực và có quyền truy cập model Gemini 1.5 Flash.
- Nếu gặp lỗi không mở được app, kiểm tra quyền truy cập hoặc vào System Preferences > Security & Privacy để cho phép mở app.

## Liên hệ
Nếu cần hỗ trợ, vui lòng liên hệ người phát triển project này. 