import json
import os
import re

FILE_NAME = "students.json"

# ------------------ Predefined Departments ------------------
DEPARTMENTS = ["Computer Science", "Mathematics", "Physics", "Chemistry", "Biology", "Economics", "History"]

# ------------------ File Handling ------------------

def load_data():
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            return {}  # Return empty dict if file is empty or corrupted
    return {}

def save_data(data):
    with open(FILE_NAME, "w") as file:
        json.dump(data, file, indent=4)

# ------------------ Validations ------------------

def valid_student_id(sid):
    """
    Validates student ID format: CU-0000-YYYY
    - CU can be uppercase or lowercase
    - Roll number: 4 digits
    - Year: any 4-digit number
    """
    pattern = r"^(CU)-(\d{4})-(\d{4})$"
    match = re.match(pattern, sid, re.IGNORECASE)
    return bool(match)

def normalize_student_id(sid):
    """Normalize CU to uppercase for consistency"""
    parts = sid.split('-')
    return f"CU-{parts[1]}-{parts[2]}"

def valid_name(name):
    """Name must contain alphabets only (spaces allowed)"""
    return name.replace(" ", "").isalpha()

def valid_age(age):
    """Age must be numeric and between 5 and 100"""
    return age.isdigit() and 5 <= int(age) <= 100

# ------------------ CRUD Operations ------------------

def add_student():
    data = load_data()

    while True:
        sid_input = input("Enter Student ID (CU-0000-YYYY): ").strip()
        if not valid_student_id(sid_input):
            print("❌ Invalid ID! Must be like 'CU-0001-2026', CU/cu accepted.")
            continue

        sid = normalize_student_id(sid_input)

        if sid in data:
            print("❌ Student ID already exists!")
        else:
            break

    # Name input
    while True:
        name = input("Enter Name: ").strip()
        if valid_name(name):
            break
        print("❌ Invalid name! Only alphabets allowed.")

    # Age input
    while True:
        age_input = input("Enter Age: ").strip()
        if valid_age(age_input):
            age = int(age_input)
            break
        print("❌ Invalid age! Enter digits only between 5–100.")

    # Department selection
    print("\nSelect Department:")
    for i, dept in enumerate(DEPARTMENTS, 1):
        print(f"{i}. {dept}")

    while True:
        dept_choice = input("Enter choice number: ").strip()
        if dept_choice.isdigit() and 1 <= int(dept_choice) <= len(DEPARTMENTS):
            department = DEPARTMENTS[int(dept_choice)-1]
            break
        print("❌ Invalid choice! Enter a number corresponding to a department.")

    # Save student
    data[sid] = {
        "Name": name,
        "Age": age,
        "Department": department
    }

    save_data(data)
    print(f"✅ Student added successfully! Student ID: {sid}")

def view_students():
    data = load_data()
    if not data:
        print("No student records found.")
        return

    for sid, info in data.items():
        print("\n----------------------")
        print(f"Student ID: {sid}")
        print(f"Name: {info['Name']}")
        print(f"Age: {info['Age']}")
        print(f"Department: {info['Department']}")

# ------------------ Search, Update, Delete ------------------

def search_student():
    data = load_data()
    sid_input = input("Enter Student ID to search: ").strip()

    if not valid_student_id(sid_input):
        print("❌ Invalid ID format! Must be like CU-0000-YYYY")
        return

    sid = normalize_student_id(sid_input)

    if sid in data:
        print("\nStudent Found:")
        print(f"Student ID: {sid}")
        for key, value in data[sid].items():
            print(f"{key}: {value}")
    else:
        print("❌ Student not found!")

def update_student():
    data = load_data()
    sid_input = input("Enter Student ID to update: ").strip()

    if not valid_student_id(sid_input):
        print("❌ Invalid ID format! Must be like CU-0000-YYYY")
        return

    sid = normalize_student_id(sid_input)

    if sid not in data:
        print("❌ Student not found!")
        return

    while True:
        # Show current student details
        print("\nStudent Found:")
        print(f"Student ID: {sid}")
        for key, value in data[sid].items():
            print(f"{key}: {value}")

        # Update menu
        print("\nWhich field do you want to update?")
        print("1. Name")
        print("2. Age")
        print("3. Department")
        print("4. Student ID")
        print("5. Cancel")

        choice = input("Enter your choice (1-5): ").strip()
        if not choice.isdigit() or int(choice) < 1 or int(choice) > 5:
            print("❌ Invalid choice! Update cancelled.")
            return

        choice = int(choice)

        if choice == 1:
            new_name = input("Enter new Name: ").strip()
            if not valid_name(new_name):
                print("❌ Invalid name! Only alphabets allowed. Update cancelled.")
                return
            data[sid]["Name"] = new_name
        elif choice == 2:
            new_age = input("Enter new Age: ").strip()
            if not valid_age(new_age):
                print("❌ Invalid age! Must be a number between 5-100. Update cancelled.")
                return
            data[sid]["Age"] = int(new_age)
        elif choice == 3:
            print("\nSelect new Department:")
            for i, dept in enumerate(DEPARTMENTS, 1):
                print(f"{i}. {dept}")
            while True:
                dept_choice = input("Enter choice number: ").strip()
                if dept_choice.isdigit() and 1 <= int(dept_choice) <= len(DEPARTMENTS):
                    data[sid]["Department"] = DEPARTMENTS[int(dept_choice)-1]
                    break
                print("❌ Invalid choice! Enter a number corresponding to a department.")
        elif choice == 4:
            new_sid_input = input("Enter new Student ID (CU-0000-YYYY): ").strip()
            if not valid_student_id(new_sid_input):
                print("❌ Invalid ID format! Update cancelled.")
                return
            new_sid = normalize_student_id(new_sid_input)
            if new_sid in data:
                print("❌ Student ID already exists. Update cancelled.")
                return
            data[new_sid] = data.pop(sid)
            sid = new_sid
        elif choice == 5:
            print("Update cancelled.")
            return

        save_data(data)
        print("✅ Student record updated successfully!")

        another = input("\nDo you want to update another field for this student? (y/n): ").strip().lower()
        if another != "y":
            break

def delete_student():
    data = load_data()
    sid_input = input("Enter Student ID to delete: ").strip()

    if not valid_student_id(sid_input):
        print("❌ Invalid ID format! Must be like CU-0000-YYYY")
        return

    sid = normalize_student_id(sid_input)

    if sid in data:
        del data[sid]
        save_data(data)
        print("✅ Student deleted successfully!")
    else:
        print("❌ Student not found!")

# ------------------ Main Menu ------------------

def main():
    while True:
        print("\n====== Student Management System ======")
        print("1. Add Student")
        print("2. View All Students")
        print("3. Search Student")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ").strip()
        if not choice.isdigit() or int(choice) < 1 or int(choice) > 6:
            print("❌ Invalid choice! Enter a number between 1-6.")
            continue

        choice = int(choice)

        if choice == 1:
            add_student()
        elif choice == 2:
            view_students()
        elif choice == 3:
            search_student()
        elif choice == 4:
            update_student()
        elif choice == 5:
            delete_student()
        elif choice == 6:
            print("Exiting program...")
            break

# ------------------ Run Program ------------------

if __name__ == "__main__":
    main()
