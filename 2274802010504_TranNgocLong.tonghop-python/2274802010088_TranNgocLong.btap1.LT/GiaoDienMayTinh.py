import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

win = tk.Tk()
win.title("Giao diện tính toán")
win.geometry("230x70")  
win.resizable(False, False) 

# Các nhãn & ô nhập
# Ô nhập số A
ttk.Label(win, text="Số a: ").grid(column=0, row=0, sticky='w')
so_a = tk.StringVar()
so_a_entered = ttk.Entry(win, width=12, textvariable=so_a)
so_a_entered.grid(column=1, row=0)

# Ô nhập số B
ttk.Label(win, text="Số b: ").grid(column=0, row=1, sticky='w')
so_b = tk.StringVar()
so_b_entered = ttk.Entry(win, width=12, textvariable=so_b)
so_b_entered.grid(column=1, row=1)

# Hiển thị kết quả
ket_qua_label = ttk.Label(win, text="Kết quả: ")
ket_qua_label.grid(column=0, row=2, sticky='w', columnspan=2)

# Hàm kiểm tra kí tự input có phải là số không
def is_number(gia_tri):
    try:
        float(gia_tri)
        return True
    except ValueError:
        return False

# Các hàm phép tính
# Phép cộng
def cong():
    if (is_number(so_a.get()) and is_number(so_b.get())):
        ket_qua_label.configure(text="Kết quả: " + str((float(so_a.get()) + float(so_b.get()))))
    else:
        messagebox.showerror("Lỗi nhập liệu", "Vui lòng chỉ nhập giá trị số")

button_cong = ttk.Button(win, text="+", width=3, command=cong)
button_cong.grid(column=2, row=0)

# Phép trừ
def tru():
    if (is_number(so_a.get()) and is_number(so_b.get())):
        ket_qua_label.configure(text="Kết quả: " + str((float(so_a.get()) - float(so_b.get()))))
    else:
        messagebox.showerror("Lỗi nhập liệu", "Vui lòng chỉ nhập giá trị số")

button_tru = ttk.Button(win, text="-", width=3, command=tru)
button_tru.grid(column=3, row=0)

# Phép nhân
def nhan():
    if (is_number(so_a.get()) and is_number(so_b.get())):
        ket_qua_label.configure(text="Kết quả: " + str((float(so_a.get()) * float(so_b.get()))))
    else:
        messagebox.showerror("Lỗi nhập liệu", "Vui lòng chỉ nhập giá trị số")

button_nhan = ttk.Button(win, text="*", width=3, command=nhan)
button_nhan.grid(column=2, row=1)

# Phép chia
def chia():
    if (is_number(so_a.get()) and is_number(so_b.get())):
        ket_qua_label.configure(text="Kết quả: " + str((float(so_a.get()) / float(so_b.get()))))
    else:
        messagebox.showerror("Lỗi nhập liệu", "Vui lòng chỉ nhập giá trị số")

button_chia = ttk.Button(win, text="/", width=3, command=chia)
button_chia.grid(column=3, row=1)

# Ghi chú để tránh ô nhập bị đẩy
win.grid_columnconfigure(0, weight=1)
win.grid_columnconfigure(1, weight=1)
win.grid_columnconfigure(2, weight=8)
win.grid_columnconfigure(3, weight=0)

win.mainloop()
