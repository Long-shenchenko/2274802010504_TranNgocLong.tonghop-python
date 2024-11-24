import tkinter as tk
from tkinter import ttk
import psycopg2

cua_so = tk.Tk()
cua_so.title("Quản lý Sinh Viên")

tk.Label(cua_so, text="Tên:").grid(row=0, column=0)
nhap_ten = tk.Entry(cua_so)
nhap_ten.grid(row=0, column=1)

tk.Label(cua_so, text="Tuổi:").grid(row=0, column=2)
nhap_tuoi = tk.Entry(cua_so)
nhap_tuoi.grid(row=0, column=3)

tk.Label(cua_so, text="Giới tính:").grid(row=1, column=0)
nhap_gioi_tinh = tk.Entry(cua_so)
nhap_gioi_tinh.grid(row=1, column=1)

tk.Label(cua_so, text="Ngành học:").grid(row=1, column=2)
nhap_nganh_hoc = tk.Entry(cua_so)
nhap_nganh_hoc.grid(row=1, column=3)

cot = ('ID', 'Tên', 'Tuổi', 'Giới tính', 'Ngành')
bang = ttk.Treeview(cua_so, columns=cot, show='headings')

for cot_ten in cot:
    bang.heading(cot_ten, text=cot_ten)

bang.grid(row=2, column=0, columnspan=4)

nut_them = tk.Button(cua_so, text="Thêm sinh viên")
nut_them.grid(row=3, column=0)

nut_cap_nhat = tk.Button(cua_so, text="Cập nhật thông tin")
nut_cap_nhat.grid(row=3, column=1)

nut_xoa = tk.Button(cua_so, text="Xóa sinh viên")
nut_xoa.grid(row=3, column=2)

nut_tai_lai = tk.Button(cua_so, text="Tải lại danh sách")
nut_tai_lai.grid(row=3, column=3)

def ket_noi_csdl():
    try:
        ket_noi = psycopg2.connect(
            dbname="book",
            user="postgres",
            password="ngoclong",
            host="localhost",
            port="5432"
        )
        return ket_noi
    except Exception as e:
        print(f"Không thể kết nối cơ sở dữ liệu: {e}")
        return None
    
def them_sinh_vien():
    ket_noi = ket_noi_csdl()
    con_tro = ket_noi.cursor()

    ten = nhap_ten.get()
    tuoi = int(nhap_tuoi.get())
    gioi_tinh = nhap_gioi_tinh.get()
    nganh = nhap_nganh_hoc.get()

    cau_lenh = "INSERT INTO students (name, age, gender, major) VALUES (%s, %s, %s, %s)"
    con_tro.execute(cau_lenh, (ten, tuoi, gioi_tinh, nganh))

    ket_noi.commit()
    ket_noi.close()

nut_them.config(command=them_sinh_vien)

def cap_nhat_sinh_vien():
    ket_noi = ket_noi_csdl()
    con_tro = ket_noi.cursor()

    sinh_vien_chon = bang.selection()[0]
    sinh_vien_id = bang.item(sinh_vien_chon, 'values')[0]

    ten = nhap_ten.get()
    tuoi = int(nhap_tuoi.get())
    gioi_tinh = nhap_gioi_tinh.get()
    nganh = nhap_nganh_hoc.get()

    cau_lenh = "UPDATE students SET name=%s, age=%s, gender=%s, major=%s WHERE id=%s"
    con_tro.execute(cau_lenh, (ten, tuoi, gioi_tinh, nganh, sinh_vien_id))

    ket_noi.commit()
    ket_noi.close()

nut_cap_nhat.config(command=cap_nhat_sinh_vien)

def xoa_sinh_vien():
    ket_noi = ket_noi_csdl()
    con_tro = ket_noi.cursor()

    sinh_vien_chon = bang.selection()[0]
    sinh_vien_id = bang.item(sinh_vien_chon, 'values')[0]

    cau_lenh = "DELETE FROM students WHERE id=%s"
    con_tro.execute(cau_lenh, (sinh_vien_id,))

    ket_noi.commit()
    ket_noi.close()

nut_xoa.config(command=xoa_sinh_vien)

def tai_lai_danh_sach():
    for item in bang.get_children():
        bang.delete(item)

    ket_noi = ket_noi_csdl()
    con_tro = ket_noi.cursor()

    con_tro.execute("SELECT * FROM students")
    hang = con_tro.fetchall()

    for du_lieu in hang:
        bang.insert('', tk.END, values=du_lieu)

    ket_noi.close()

nut_tai_lai.config(command=tai_lai_danh_sach)

cua_so.mainloop()
