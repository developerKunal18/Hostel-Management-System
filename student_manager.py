from config import STUDENTS_FILE, ROOMS_FILE
from storage import read_data, write_data
from utils import input_required, input_positive_int, today
from room_manager import allocate_room


def add_student():
    students = read_data(STUDENTS_FILE)

    name = input_required("Enter student name: ")
    phone = input_required("Enter phone number: ")

    if not phone.isdigit() or not 7 <= len(phone) <= 15:
        print("Enter a valid phone number containing 7 to 15 digits.")
        return

    if any(s["phone"] == phone and s["active"] for s in students):
        print("An active student already uses this phone number.")
        return

    room_id = input_positive_int("Enter room ID for allocation: ")

    rooms = read_data(ROOMS_FILE)
    room = next((r for r in rooms if r["id"] == room_id), None)

    if not room:
        print("Room not found. Add the room before registering the student.")
        return

    occupants = [
        s for s in students
        if s["active"] and s["room_id"] == room_id
    ]

    if len(occupants) >= room["capacity"]:
        print("This room is full. Choose another room.")
        return

    student_id = max((s["id"] for s in students), default=0) + 1

    student = {
        "id": student_id,
        "name": name,
        "phone": phone,
        "room_id": room_id,
        "monthly_fee": room["monthly_fee"],
        "active": True,
        "joined_date": today(),
        "checkout_date": None
    }

    students.append(student)
    write_data(STUDENTS_FILE, students)

    print(f"Student registered successfully. Student ID: {student_id}")


def list_students(show_inactive=False):
    students = read_data(STUDENTS_FILE)
    rooms = read_data(ROOMS_FILE)
    room_map = {room["id"]: room["room_number"] for room in rooms}

    if not show_inactive:
        students = [s for s in students if s["active"]]

    if not students:
        print("No students found.")
        return

    print("\n" + "-" * 90)
    print(f"{'ID':<6}{'Name':<25}{'Phone':<17}{'Room':<12}{'Status':<12}{'Monthly Fee':>15}")
    print("-" * 90)

    for student in students:
        room_number = room_map.get(student["room_id"], "Not assigned")
        status = "Active" if student["active"] else "Checked out"

        print(
            f"{student['id']:<6}"
            f"{student['name'][:24]:<25}"
            f"{student['phone']:<17}"
            f"{room_number:<12}"
            f"{status:<12}"
            f"₹{student['monthly_fee']:>13.2f}"
        )


def search_student():
    students = read_data(STUDENTS_FILE)
    query = input_required("Enter student ID, name, or phone: ").lower()

    matches = [
        s for s in students
        if query == str(s["id"])
        or query in s["name"].lower()
        or query in s["phone"].lower()
    ]

    if not matches:
        print("No matching students found.")
        return

    for student in matches:
        print("-" * 35)
        print(f"ID: {student['id']}")
        print(f"Name: {student['name']}")
        print(f"Phone: {student['phone']}")
        print(f"Room ID: {student['room_id']}")
        print(f"Monthly Fee: ₹{student['monthly_fee']:.2f}")
        print(f"Status: {'Active' if student['active'] else 'Checked out'}")
        print(f"Joined: {student['joined_date']}")
        print(f"Checkout Date: {student['checkout_date'] or 'N/A'}")


def checkout_student():
    students = read_data(STUDENTS_FILE)

    student_id = input_positive_int("Enter student ID to check out: ")

    student = next(
        (s for s in students if s["id"] == student_id and s["active"]),
        None
    )

    if not student:
        print("Active student not found.")
        return

    confirmation = input(
        f"Check out {student['name']}? Type YES to confirm: "
    ).strip()

    if confirmation != "YES":
        print("Checkout cancelled.")
        return

    student["active"] = False
    student["checkout_date"] = today()

    write_data(STUDENTS_FILE, students)

    print(f"{student['name']} has been checked out successfully.")
