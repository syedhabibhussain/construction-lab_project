import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
import re

# --- BACKEND LOGIC ---
FILE_NAME = "students.json"
DEPARTMENTS = ["Computer Science", "Mathematics", "Physics", "Chemistry", "Biology", "Economics", "History"]

def load_data():
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r") as file:
                return json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}
    return {}

def save_data(data):
    try:
        with open(FILE_NAME, "w") as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        print(f"Error saving file: {e}")

def valid_student_id(sid):
    pattern = r"^(CU)-(\d{4})-(\d{4})$"
    return bool(re.match(pattern, sid, re.IGNORECASE))

def normalize_student_id(sid):
    parts = sid.split('-')
    return f"CU-{parts[1]}-{parts[2]}".upper()

# --- FRONTEND GUI ---
class SMSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Management System")
        self.root.geometry("900x600")
        self.root.configure(bg="#f0f0f0")

        # Title
        tk.Label(root, text="Student Management System", font=("Helvetica", 22, "bold"), 
                 fg="#2c3e50", bg="#f0f0f0").pack(pady=20)

        # --- Input Section ---
        input_frame = tk.LabelFrame(root, text=" Register New Student ", font=("Arial", 10, "bold"), 
                                   padx=15, pady=15, bg="#f0f0f0")
        input_frame.pack(padx=20, fill="x")

        tk.Label(input_frame, text="ID (CU-0000-2026):", bg="#f0f0f0").grid(row=0, column=0, sticky="e")
        self.ent_id = tk.Entry(input_frame, font=("Arial", 10))
        self.ent_id.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(input_frame, text="Full Name:", bg="#f0f0f0").grid(row=0, column=2, sticky="e")
        self.ent_name = tk.Entry(input_frame, font=("Arial", 10))
        self.ent_name.grid(row=0, column=3, padx=10, pady=5)

        tk.Label(input_frame, text="Age:", bg="#f0f0f0").grid(row=1, column=0, sticky="e")
        self.ent_age = tk.Entry(input_frame, font=("Arial", 10))
        self.ent_age.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(input_frame, text="Department:", bg="#f0f0f0").grid(row=1, column=2, sticky="e")
        self.combo_dept = ttk.Combobox(input_frame, values=DEPARTMENTS, state="readonly", font=("Arial", 10))
        self.combo_dept.set("Select Department") 
        self.combo_dept.grid(row=1, column=3, padx=10, pady=5)

        # --- Button Section ---
        btn_frame = tk.Frame(root, bg="#f0f0f0")
        btn_frame.pack(pady=15)

        tk.Button(btn_frame, text="✚ Add Student", command=self.add_student, bg="#27ae60", fg="white", 
                  font=("Arial", 10, "bold"), width=15).grid(row=0, column=0, padx=8)
        
        tk.Button(btn_frame, text="🗑 Delete Selected", command=self.delete_student, bg="#c0392b", fg="white", 
                  font=("Arial", 10, "bold"), width=15).grid(row=0, column=1, padx=8)
        
        tk.Button(btn_frame, text="⟳ Clear Fields", command=self.clear_fields, bg="#7f8c8d", fg="white", 
                  font=("Arial", 10, "bold"), width=15).grid(row=0, column=2, padx=8)

        # --- View Table ---
        table_frame = tk.Frame(root)
        table_frame.pack(padx=20, pady=10, fill="both", expand=True)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", rowheight=30)
        style.map("Treeview", background=[('selected', '#3498db')])

        self.tree = ttk.Treeview(table_frame, columns=("ID", "Name", "Age", "Dept"), show='headings')
        self.tree.heading("ID", text="STUDENT ID")
        self.tree.heading("Name", text="FULL NAME")
        self.tree.heading("Age", text="AGE")
        self.tree.heading("Dept", text="DEPARTMENT")
        self.tree.column("ID", width=150, anchor="center")
        self.tree.column("Age", width=80, anchor="center")

        self.tree.pack(fill="both", expand=True)

        self.tree.tag_configure('oddrow', background="#ffffff")
        self.tree.tag_configure('evenrow', background="#f2f2f2")

        self.refresh_table()

    def refresh_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        data = load_data()
        for i, (sid, info) in enumerate(data.items()):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            self.tree.insert("", "end", values=(sid, info['Name'], info['Age'], info['Department']), tags=(tag,))

    def add_student(self):
        sid_raw = self.ent_id.get().strip()
        name = self.ent_name.get().strip()
        age = self.ent_age.get().strip()
        dept = self.combo_dept.get()

        if not valid_student_id(sid_raw):
            messagebox.showerror("Error", "ID must follow format: CU-0000-2026")
            return
        
        sid = normalize_student_id(sid_raw)
        data = load_data()

        if sid in data:
            messagebox.showerror("Error", f"ID {sid} already exists!")
            return

        if not name or not age or dept == "Select Department":
            messagebox.showerror("Error", "Please fill all fields!")
            return

        data[sid] = {"Name": name, "Age": age, "Department": dept}
        save_data(data)
        self.refresh_table()
        self.clear_fields()
        messagebox.showinfo("Success", "Student Added!")

    def delete_student(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a row first!")
            return
        
        sid = self.tree.item(selected)['values'][0]
        if messagebox.askyesno("Confirm", f"Delete {sid}?"):
            data = load_data()
            if sid in data:
                del data[sid]
                save_data(data)
                self.refresh_table()

    def clear_fields(self):
        self.ent_id.delete(0, tk.END)
        self.ent_name.delete(0, tk.END)
        self.ent_age.delete(0, tk.END)
        self.combo_dept.set('Select Department')

# --- THE START COMMAND ---
if __name__ == "__main__":
    root = tk.Tk()
    app = SMSApp(root)
    root.mainloop() # This line MUST be present to show the window