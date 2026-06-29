"""
BÁO CÁO PHÂN TÍCH
1. Input của bài toán là gì?
   - keyword (string, không bắt buộc): từ khóa tìm kiếm theo tên sản phẩm,
     truyền qua Query Parameter, ví dụ: /products?keyword=mouse
   - max_price (float, không bắt buộc): mức giá tối đa để lọc sản phẩm,
     truyền qua Query Parameter, ví dụ: /products?max_price=300000
   - Hai tham số trên có thể được truyền độc lập, kết hợp cùng nhau,
     hoặc không truyền tham số nào.

2. Output mong muốn là gì?
   - Nếu không truyền tham số nào: trả về toàn bộ danh sách sản phẩm.
   - Nếu chỉ truyền keyword: trả về sản phẩm có tên chứa từ khóa đó
     (không phân biệt chữ hoa/chữ thường).
   - Nếu chỉ truyền max_price: trả về sản phẩm có price <= max_price.
   - Nếu truyền cả hai: trả về sản phẩm thỏa mãn đồng thời cả hai điều kiện.
   - Nếu max_price < 0: trả về lỗi rõ ràng dạng
     {"detail": "max_price không được âm"}.

3. Đề xuất giải pháp xử lý bài toán
   - Sử dụng FastAPI Query Parameters cho "keyword" và "max_price",
     cả hai đều là tham số không bắt buộc (Optional, giá trị mặc định None).
   - Trước khi lọc dữ liệu, kiểm tra ràng buộc: nếu max_price được truyền
     và nhỏ hơn 0 thì trả lỗi ngay bằng HTTPException (status 400).
   - Áp dụng lọc tuần tự trên danh sách products:
     bước lọc theo keyword (nếu có) -> bước lọc theo max_price (nếu có).
   - Vì hai điều kiện độc lập và có thể kết hợp, dùng cách lọc tuần tự
     (filter từng bước) sẽ tự nhiên đáp ứng được yêu cầu "thỏa mãn cả hai".

4. Thiết kế các bước xử lý bài toán
   Bước 1: Nhận keyword và max_price từ Query Parameters.
   Bước 2: Kiểm tra max_price, nếu < 0 thì raise HTTPException với
           detail "max_price không được âm".
   Bước 3: Khởi tạo result = toàn bộ danh sách products.
   Bước 4: Nếu có keyword, lọc result theo điều kiện
           keyword.lower() nằm trong name.lower().
   Bước 5: Nếu có max_price, lọc result theo điều kiện price <= max_price.
   Bước 6: Trả về result.
"""

from typing import Optional

from fastapi import FastAPI, HTTPException, Query

app = FastAPI()

products = [
    {"id": 1, "name": "Laptop", "price": 15000000},
    {"id": 2, "name": "Mouse", "price": 200000},
    {"id": 3, "name": "Keyboard", "price": 500000},
    {"id": 4, "name": "Monitor", "price": 3000000},
]


@app.get("/products")
def get_products(
    keyword: Optional[str] = Query(default=None),
    max_price: Optional[float] = Query(default=None),
):
    if max_price is not None and max_price < 0:
        raise HTTPException(status_code=400, detail="max_price không được âm")

    result = products

    if keyword is not None:
        result = [p for p in result if keyword.lower() in p["name"].lower()]

    if max_price is not None:
        result = [p for p in result if p["price"] <= max_price]

    return result