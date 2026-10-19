from config import STUDENTS_FILE, ROOMS_FILE, PAYMENTS_FILE
from storage import read_data
from fee_manager import monthly_paid
from utils import current_month


def dashboard():
    students = read_data(STUDENTS_FILE)
    rooms = read_data(ROOMS_FILE)
    payments = read_data(PAYMENTS_FILE)

    active_students = [s for s in students if s["active"]]
    inactive_students = [s for s in students if not s["active"]]

    total_capacity = sum(room["capacity"] for room in rooms)
    occupied_beds = len(active_students)
    available_beds = max(0, total_capacity - occupied_beds)

    month = current_month()
    month_payments = [
        p for p in payments if p["date"].startswith(month)
    ]
    total_collected = sum(p["amount"] for p in month_payments)

    total_pending = sum(
        max(
            0,
            round(
                float(student["monthly_fee"])
                - monthly_paid(student["id"], month),
                2
            )
        )
        for student in active_students
    )

    print("\n" + "=" * 45)
    print("        HOSTEL MANAGEMENT DASHBOARD")
    print("=" * 45)
    print(f"Total rooms:             {len(rooms)}")
    print(f"Total bed capacity:      {total_capacity}")
    print(f"Occupied beds:           {occupied_beds}")
    print(f"Available beds:          {available_beds}")
    print(f"Active students:         {len(active_students)}")
    print(f"Checked-out students:    {len(inactive_students)}")
    print(f"Payments collected ({month}): ₹{total_collected:.2f}")
    print(f"Pending fees ({month}):      ₹{total_pending:.2f}")
    print("=" * 45)


def room_occupancy_report():
    rooms = read_data(ROOMS_FILE)
    students = read_data(STUDENTS_FILE)

    if not rooms:
        print("No rooms have been registered.")
        return

    print("\nROOM OCCUPANCY REPORT")
    print("-" * 60)

    for room in rooms:
        occupants = [
            student for student in students
            if student["active"] and student["room_id"] == room["id"]
        ]

        available = max(0, room["capacity"] - len(occupants))
        occupancy_rate = (
            len(occupants) / room["capacity"] * 100
            if room["capacity"] else 0
        )

        print(f"Room: {room['room_number']}")
        print(f"Capacity: {room['capacity']}")
        print(f"Occupied: {len(occupants)}")
        print(f"Available: {available}")
        print(f"Occupancy: {occupancy_rate:.1f}%")
        print("-" * 60)


def payment_summary():
    payments = read_data(PAYMENTS_FILE)

    if not payments:
        print("No payment records available.")
        return

    monthly_totals = {}

    for payment in payments:
        month = payment["date"][:7]
        monthly_totals[month] = (
            monthly_totals.get(month, 0) + payment["amount"]
        )

    print("\nMONTHLY PAYMENT SUMMARY")
    print("-" * 40)

    for month in sorted(monthly_totals):
        print(f"{month}: ₹{monthly_totals[month]:.2f}")

    print("-" * 40)
    print(f"Lifetime collected: ₹{sum(p['amount'] for p in payments):.2f}")
