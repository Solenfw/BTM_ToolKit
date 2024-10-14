import pandas as pd
import re

# Hàm tách chuỗi dựa trên dấu phẩy nhưng không tách nếu đó là số thập phân
def tach_chuoi_voi_dau_phay(thong_so):
    if isinstance(thong_so, str):
        # Sử dụng biểu thức chính quy để tìm tất cả số thập phân và lưu trữ chúng
        decimal_numbers = re.findall(r'\d+,\d+', thong_so)

        # Thay thế các số thập phân bằng một ký hiệu đặc biệt tạm thời (VD: "{DECIMAL}")
        temp_string = re.sub(r'\d+,\d+', '{DECIMAL}', thong_so)

        # Tách chuỗi dựa trên dấu phẩy thông thường (không bao gồm số thập phân)
        parts = [part.strip() for part in temp_string.split(',')]

        # Đưa lại các số thập phân vào vị trí ban đầu
        for i, part in enumerate(parts):
            if '{DECIMAL}' in part:
                parts[i] = part.replace('{DECIMAL}', decimal_numbers.pop(0))

        return parts
    return []

# Hàm tách thông số sản phẩm từ cột VN_Description
def tach_thong_so_san_pham(thong_so, tu_khoa_list):
    if isinstance(thong_so, str):
        # Tách chuỗi bằng cách sử dụng hàm tach_chuoi_voi_dau_phay
        phan_tu = tach_chuoi_voi_dau_phay(thong_so)

        # Gộp phần trước và sau dấu phẩy cuối cùng vào cột Product Size
        product_size = phan_tu[-1].strip() if len(phan_tu) > 1 else ''
        product_description = ', '.join(phan_tu[:-1]).strip() if len(phan_tu) > 1 else ''

        # Lấy Name Tag là từ viết hoa trong mô tả, loại trừ từ đầu tiên
        name_tag = ' '.join([word for word in product_description.split()[1:] if word[0].isupper()])

        # Loại bỏ phần trùng lặp trong Product Description nếu Product Size đã tồn tại
        if product_size in product_description:
            product_description = product_description.replace(product_size, '').strip()

        # Lấy Product Family từ từ khóa nếu có trong mô tả
        product_family = ''
        
        # Kiểm tra từng từ trong từ khóa, nếu khớp với mô tả, sẽ thêm vào Product Family
        for tu_khoa in tu_khoa_list:
            if tu_khoa.lower() in thong_so.lower():
                # Ghép từ khóa vào Product Family
                product_family = tu_khoa
                break

        return {
            'Product Family': product_family,
            'Product Description': product_description,
            'Product Size': product_size,
            'Name Tag': name_tag
        }
    else:
        return {
            'Product Family': '',
            'Product Description': '',
            'Product Size': '',
            'Name Tag': ''
        }

# Hàm đọc file Excel và tách dữ liệu trong cột VN_Description
def doc_va_xu_ly_excel(file_path, tu_khoa_list):
    # Đọc dữ liệu từ file Excel
    df = pd.read_excel(file_path)
    
    # Kiểm tra cột VN_Description và cột Code
    if 'VN_Description' not in df.columns or 'Code' not in df.columns:
        raise ValueError("File Excel phải chứa cả cột 'VN_Description' và 'Code'!")
    
    # Áp dụng hàm tách thông số cho từng dòng trong cột VN_Description
    df['Product Family'] = df['VN_Description'].apply(lambda x: tach_thong_so_san_pham(x, tu_khoa_list)['Product Family'])
    df['Product Description'] = df['VN_Description'].apply(lambda x: tach_thong_so_san_pham(x, tu_khoa_list)['Product Description'])
    df['Product Size'] = df['VN_Description'].apply(lambda x: tach_thong_so_san_pham(x, tu_khoa_list)['Product Size'])
    df['Name Tag'] = df['VN_Description'].apply(lambda x: tach_thong_so_san_pham(x, tu_khoa_list)['Name Tag'])
    
    return df

# Hàm xuất dữ liệu ra file Excel
def xuat_file_excel(df, file_name):
    # Xuất dữ liệu ra file Excel
    df.to_excel(file_name, index=False)

# Hàm chính để thực hiện quy trình
def xu_ly_file_va_tim_kiem(file_path):
    # Người dùng nhập nhiều từ khóa cho Product Family (cách nhau bằng dấu phẩy)
    while True:
        tu_khoa = input("Nhập từ khóa cho Product Family (cách nhau bằng dấu phẩy): ")
        tu_khoa_list = [word.strip() for word in tu_khoa.split(',')]  # Chia nhỏ và lưu vào danh sách
        
        # Đọc và xử lý file Excel
        df = doc_va_xu_ly_excel(file_path, tu_khoa_list)

        # Lọc các sản phẩm có sự trùng khớp với từ khóa
        df_ket_qua = df[df['Product Family'] != '']  # Chỉ chọn các dòng có từ khóa tìm được
        
        # Kiểm tra nếu có sản phẩm nào để lưu
        if df_ket_qua.empty:
            print("Không có sản phẩm nào trùng khớp với từ khóa. Vui lòng nhập lại.")
        else:
            break  # Dừng khi tìm thấy sản phẩm khớp
    
    # Xuất kết quả ra file Excel mới
    xuat_file_excel(df_ket_qua, 'ket_qua_tim_kiem1dao.xlsx')
    print("Kết quả đã được xuất ra file 'ket_qua_tim_kiem.xlsx'.")

# Ví dụ gọi hàm chính với file Excel
file_path = r'D:\Work\Code\BTM_code\Excel\FIle test.xlsx'  # Thay đổi đường dẫn đến file của bạn
xu_ly_file_va_tim_kiem(file_path)
