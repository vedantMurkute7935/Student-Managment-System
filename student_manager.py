import csv
import os

# file where all data is saved
filename = "students.csv"

# creating the file if it doesnt exist
def create_file():
    if not os.path.exists(filename):
        f = open(filename, "w", newline="")
        writer = csv.writer(f)
        writer.writerow(["ID", "Name", "Age", "Marks", "Subject"])
        f.close()

# read all students from csv
def read_students():
    create_file()
    f = open(filename, "r", newline="")
    reader = csv.DictReader(f)
    data = list(reader)
    f.close()
    return data

# save all students back to csv
def save_students(students):
    f = open(filename, "w", newline="")
    writer = csv.DictWriter(f, fieldnames=["ID", "Name", "Age", "Marks", "Subject"])
    writer.writeheader()
    writer.writerows(students)
    f.close()

# make new id like S001 S002 etc
def make_id(students):
    if len(students) == 0:
        return "S001"
    last = max(int(s["ID"][1:]) for s in students)
    return "S" + str(last + 1).zfill(3)

# add new student
def add_student():
    print("\n-- Add New Student --")
    students = read_students()

    name = input("Enter name: ").strip()
    if name == "":
        print("Name cant be empty!")
        return

    # checking age is valid number
    try:
        age = int(input("Enter age: "))
    except ValueError:
        print("Age should be a number!")
        return

    # marks between 0 and 100
    try:
        marks = float(input("Enter marks (out of 100): "))
        if marks < 0 or marks > 100:
            print("Marks should be between 0 and 100")
            return
    except ValueError:
        print("Marks should be a number!")
        return

    subject = input("Enter subject: ").strip()
    if subject == "":
        print("Subject cant be empty!")
        return

    new_student = {
        "ID": make_id(students),
        "Name": name,
        "Age": age,
        "Marks": marks,
        "Subject": subject
    }

    students.append(new_student)
    save_students(students)
    print("Student added! ID is:", new_student["ID"])

# show all students
def view_students():
    students = read_students()
    print("\n-- All Students --")

    if len(students) == 0:
        print("No students found.")
        return

    # print header
    print(f"{'ID':<6} {'Name':<18} {'Age':<5} {'Marks':<8} {'Subject'}")
    print("-" * 50)

    for s in students:
        print(f"{s['ID']:<6} {s['Name']:<18} {s['Age']:<5} {s['Marks']:<8} {s['Subject']}")

    print("\nTotal:", len(students))

# search student by name or id
def search_student():
    print("\n-- Search Student --")
    search = input("Enter name or ID to search: ").strip().lower()
    students = read_students()

    found = []
    for s in students:
        if search in s["Name"].lower() or search in s["ID"].lower():
            found.append(s)

    if len(found) == 0:
        print("No student found with that name or ID")
    else:
        for s in found:
            print("\nID:", s["ID"])
            print("Name:", s["Name"])
            print("Age:", s["Age"])
            print("Marks:", s["Marks"])
            print("Subject:", s["Subject"])

# edit existing student
def edit_student():
    view_students()
    students = read_students()

    if len(students) == 0:
        return

    sid = input("\nEnter student ID to edit: ").strip().upper()

    found = False
    for s in students:
        if s["ID"] == sid:
            found = True
            print("Leave blank if you dont want to change that field")

            new_name = input("New name [" + s["Name"] + "]: ").strip()
            if new_name != "":
                s["Name"] = new_name

            new_age = input("New age [" + s["Age"] + "]: ").strip()
            if new_age != "":
                try:
                    s["Age"] = int(new_age)
                except:
                    print("Invalid age, keeping old value")

            new_marks = input("New marks [" + s["Marks"] + "]: ").strip()
            if new_marks != "":
                try:
                    s["Marks"] = float(new_marks)
                except:
                    print("Invalid marks, keeping old value")

            new_sub = input("New subject [" + s["Subject"] + "]: ").strip()
            if new_sub != "":
                s["Subject"] = new_sub

            save_students(students)
            print("Updated successfully!")
            break

    if not found:
        print("Student not found with ID:", sid)

# delete a student
def delete_student():
    view_students()
    students = read_students()

    if len(students) == 0:
        return

    sid = input("\nEnter student ID to delete: ").strip().upper()

    for s in students:
        if s["ID"] == sid:
            confirm = input("Are you sure you want to delete " + s["Name"] + "? (yes/no): ")
            if confirm.lower() == "yes":
                students.remove(s)
                save_students(students)
                print("Deleted successfully!")
            else:
                print("Cancelled.")
            return

    print("Student not found")

# show some basic stats
def show_stats():
    students = read_students()
    print("\n-- Stats --")

    if len(students) == 0:
        print("No data to show")
        return

    all_marks = []
    for s in students:
        all_marks.append(float(s["Marks"]))

    avg = sum(all_marks) / len(all_marks)
    print("Total students:", len(students))
    print("Average marks:", round(avg, 2))
    print("Highest marks:", max(all_marks))
    print("Lowest marks:", min(all_marks))

# main menu
def menu():
    create_file()
    while True:
        print("\n=============================")
        print("  Student Management System")
        print("=============================")
        print("1. Add student")
        print("2. View all students")
        print("3. Search student")
        print("4. Edit student")
        print("5. Delete student")
        print("6. Stats")
        print("7. Exit")
        print("=============================")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            add_student()
        elif choice == "2":
            view_students()
        elif choice == "3":
            search_student()
        elif choice == "4":
            edit_student()
        elif choice == "5":
            delete_student()
        elif choice == "6":
            show_stats()
        elif choice == "7":
            print("Bye!")
            break
        else:
            print("Wrong choice, enter 1 to 7")

        input("\nPress enter to continue...")

# run the program
if __name__ == "__main__":
    menu()
