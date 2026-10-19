from config import ROOMS_FILE, STUDENTS_FILE
from storage import read_data, write_data
from utils import input_required, input_positive_int, input_positive_float


def get_room(room_id):
    rooms = read_data(ROOMS_FILE)

    for room in rooms:
        if room["id"] == room_id:
            return room

    return None


def get_occupants(room_id):
    students = read_data(STUDENTS_FILE)

    return [
        student for student in students
        if student["active"] and student["room_id"] == room_id
    ]


def add_room():
    rooms = read_data(ROOMS_FILE)

    room_number = input_required("Enter room number: ")

    if any(room["room_number"].lower() == room_number.lower()
           for room in rooms):
        print("A room with this number already exists.")
        return

    capacity = input_positive_int("Enter room capacity: ")
    monthly_fee = input_positive_float("Enter monthly hostel fee per student: ")

    room_id = max((room["id"] for room in rooms), default=0) + 1

    room = {
        "id": room_id,
        "room_number": room_number,
        "capacity": capacity,
        "monthly_fee": monthly_fee
    }

    rooms.append(room)
    write_data(ROOMS_FILE, rooms)

    print(f"Room {room_number} added successfully.")


def list_rooms():
    rooms = read_data(ROOMS_FILE)

    if not rooms:
        print("No rooms have been registered.")
        return

    print("\n" + "-" * 75)
    print(f"{'ID':<6}{'Room':<15}{'Capacity':<12}{'Occupied':<12}{'Available':<12}{'Monthly Fee':>15}")
    print("-" * 75)

    for room in rooms:
        occupied = len(get_occupants(room["id"]))
        available = max(0, room["capacity"] - occupied)

        print(
            f"{room['id']:<6}"
            f"{room['room_number']:<15}"
            f"{room['capacity']:<12}"
            f"{occupied:<12}"
            f"{available:<12}"
            f"₹{room['monthly_fee']:>13.2f}"
        )


def allocate_room(student_id, room_id):
    rooms = read_data(ROOMS_FILE)
    students = read_data(STUDENTS_FILE)

    student = next(
        (s for s in students if s["id"] == student_id and s["active"]),
        None
    )

    room = next((r for r in rooms if r["id"] == room_id), None)

    if not student:
        print("Active student not found.")
        return False

    if not room:
        print("Room not found.")
        return False

    if student["room_id"] == room_id:
        print("This student is already assigned to that room.")
        return False

    occupants = [
        s for s in students
        if s["active"]
        and s["room_id"] == room_id
        and s["id"] != student_id
    ]

    if len(occupants) >= room["capacity"]:
        print("This room is full.")
        return False

    student["room_id"] = room_id
    student["monthly_fee"] = room["monthly_fee"]

    write_data(STUDENTS_FILE, students)

    print(
        f"Room {room['room_number']} allocated to "
        f"{student['name']} successfully."
    )
    return True


def transfer_student():
    students = read_data(STUDENTS_FILE)

    try:
        student_id = input_positive_int("Enter student ID: ")
    except ValueError:
        return

    student = next(
        (s for s in students if s["id"] == student_id and s["active"]),
        None
    )

    if not student:
        print("Active student not found.")
        return

    list_rooms()

    room_id = input_positive_int("Enter destination room ID: ")
    allocate_room(student_id, room_id)
