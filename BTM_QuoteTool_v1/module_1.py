import pandas as pd
import re

# Hàm tách thông số sản phẩm từ cột VN_Description
def tach_thong_so_san_pham(thong_so, tu_khoa_list):
    if isinstance(thong_so, str):  # Kiểm tra nếu thong_so là chuỗi
        # Tách chuỗi thành các phần nhỏ dựa trên dấu phẩy hoặc dấu gạch ngang
        phan_tu = re.split(r'[,-]', thong_so)

        # Gộp phần trước và sau dấu phẩy cuối cùng vào cột Product Size
        product_size = phan_tu[-1].strip() if len(phan_tu) > 1 else ''
        product_description = ', '.join(phan_tu[:-1]).strip() if len(phan_tu) > 1 else ''

        # Lấy Name Tag là từ viết hoa trong mô tả, loại trừ từ đầu tiên
        name_tag = ' '.join([word for word in product_description.split()[1:] if word[0].isupper()])

        # Lấy Product Family từ từ khóa nếu có trong mô tả
        product_family = ''
        first_word = product_description.split()[0] if product_description.split() else ''
        
        # Kiểm tra nếu từ đầu trùng với một trong các từ khóa
        for tu_khoa in tu_khoa_list:
            if first_word.lower() == tu_khoa.lower():
                product_family = first_word
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
    tu_khoa = input("Nhập từ khóa cho Product Family (cách nhau bằng dấu phẩy): ")
    tu_khoa_list = [word.strip() for word in tu_khoa.split(',')]  # Chia nhỏ và lưu vào danh sách
    
    # Đọc và xử lý file Excel
    df = doc_va_xu_ly_excel(file_path, tu_khoa_list)

    # Lọc các sản phẩm có sự trùng khớp với từ khóa
    df_ket_qua = df[df['Product Family'].isin(tu_khoa_list)]
    
    # In kết quả
    print("\nKết quả sản phẩm có sự trùng khớp:")
    print(df_ket_qua)

    # Kiểm tra nếu có sản phẩm nào để chọn
    if df_ket_qua.empty:
        print("Không có sản phẩm nào trùng khớp với từ khóa.")
        return
    
    # Người dùng chọn sản phẩm để lưu
    print("\nChọn sản phẩm để lưu (nhập số dòng, cách nhau bằng dấu phẩy): ")
    for index, row in df_ket_qua.iterrows():
        print(f"{index}: {row['VN_Description']}")

    selected_indices = input("Nhập số dòng mà bạn muốn lưu: ")
    selected_indices_list = [int(idx.strip()) for idx in selected_indices.split(',') if idx.strip().isdigit()]
    
    # Lưu các sản phẩm đã chọn vào DataFrame mới
    df_selected = df_ket_qua.loc[selected_indices_list]

    # Xuất kết quả ra file Excel mới
    xuat_file_excel(df_selected, 'ket_qua_tim_kiem.xlsx')
    print("Kết quả đã được xuất ra file 'ket_qua_tim_kiem.xlsx'.")

# Ví dụ gọi hàm chính với file Excel
file_path = 'duong_dan_den_file_excel.xlsx'  # Thay đổi đường dẫn đến file của bạn
xu_ly_file_va_tim_kiem(file_path)
