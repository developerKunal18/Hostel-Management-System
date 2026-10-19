# Hostel Management System

A simple command-line Hostel Management System built using Python. This project helps manage hostel rooms, student registrations, room allocation, fee payments, checkouts, and reports.

## Features

- Add and view hostel rooms
- Register students and assign rooms
- View active students and checkout history
- Search students by ID, name, or phone number
- Transfer students between rooms
- Check out students and release their beds
- Record hostel fee payments
- View payment history and receipt IDs
- Calculate pending fees for the current month
- Generate room occupancy and payment reports
- Store data locally in JSON files

## Technologies Used

- Python
- JSON
- Python standard library

## Project Structure

```text
HostelManagementSystem/
├── main.py
├── config.py
├── storage.py
├── utils.py
├── student_manager.py
├── room_manager.py
├── fee_manager.py
├── report_manager.py
├── requirements.txt
├── .gitignore
└── data/
    ├── students.json
    ├── rooms.json
    └── payments.json
```

## Requirements

- Python 3.10 or newer recommended
- Any code editor, such as VS Code

No third-party packages are required.

## Installation

1. Download or clone this repository.
2. Open the project folder in VS Code.
3. Make sure the `data` folder and its three JSON files exist.
4. Open the terminal in the project folder.
5. Run the application:

```bash
python main.py
```

On some Windows installations, use:

```bash
py main.py
```

## How to Use

1. Select **Add Room** and create a room with its capacity and monthly fee.
2. Select **Register Student** and assign the student to an available room.
3. Use **View Students** or **Search Student** to find student records.
4. Record payments through **Record Fee Payment**.
5. Check outstanding fees using **View Pending Fees**.
6. Use **Transfer Student** when a student changes rooms.
7. Use **Check Out Student** when a student leaves the hostel.
8. Open the dashboard and reports to review occupancy and payments.

## Data Storage

The application stores its information in JSON files inside the `data` directory. The files are created automatically when the application starts if they do not already exist.

Keep a backup of the `data` folder to protect your records.

## Important Notes

- Room capacity is checked before assigning a student.
- A checked-out student no longer occupies a bed.
- Payments are associated with a date and month.
- Pending fees are calculated for the current calendar month.
- This project is intended for learning and small demonstrations. It does not include authentication, database transactions, or multi-user access controls.

## Future Improvements

- Add a graphical interface using Tkinter
- Add a MySQL database
- Generate printable fee receipts
- Add administrator login
- Export reports to CSV
- Track hostel expenses and maintenance

## Author

Kunal Karbhari

## License

This project is available for educational and personal learning purposes.

# IMPORTANT:
# Use this corrected fee_manager.py in place of the earlier version.
# It supports payments for past months and viewing all payment records.

from config import STUDENTS_FILE, PAYMENTS_FILE
from storage import read_data, write_data
from utils import (
    input_positive_int,
    input_positive_float,
    input_date,
    current_month,
    today
)


def student_by_id(student_id):
    students = read_data(STUDENTS_FILE)

    return next(
        (student for student in students if student["id"] == student_id),
        None
    )


def monthly_paid(student_id, month):
    payments = read_data(PAYMENTS_FILE)

    return round(
        sum(
            float(payment["amount"])
            for payment in payments
            if payment["student_id"] == student_id
            and payment["date"].startswith(month)
        ),
        2
    )


def record_payment():
    student_id = input_positive_int("Enter student ID: ")
    student = student_by_id(student_id)

    if not student or not student["active"]:
        print("Active student not found.")
        return

    payment_date = input_date(
        f"Enter payment date YYYY-MM-DD (blank for {today()}): ",
        allow_blank=True
    )

    target_month = payment_date[:7]
    monthly_fee = float(student["monthly_fee"])
    already_paid = monthly_paid(student_id, target_month)
    remaining = max(0, round(monthly_fee - already_paid, 2))

    print(f"\nStudent: {student['name']}")
    print(f"Fee month: {target_month}")
    print(f"Monthly fee: ₹{monthly_fee:.2f}")
    print(f"Already paid: ₹{already_paid:.2f}")
    print(f"Remaining: ₹{remaining:.2f}")

    if remaining <= 0:
        print("This month's fee is already paid in full.")
        return

    amount = input_positive_float("Enter payment amount: ")

    if amount > remaining:
        print(f"Payment cannot exceed ₹{remaining:.2f}.")
        return

    payments = read_data(PAYMENTS_FILE)
    payment_id = max(
        (payment["id"] for payment in payments),
        default=0
    ) + 1

    payment = {
        "id": payment_id,
        "student_id": student_id,
        "student_name": student["name"],
        "amount": round(amount, 2),
        "date": payment_date,
        "month": target_month
    }

    payments.append(payment)
    write_data(PAYMENTS_FILE, payments)

    print(f"Payment recorded successfully. Receipt ID: {payment_id}")


def view_payment_history():
    value = input(
        "Enter student ID, or type ALL to view every payment: "
    ).strip()

    payments = read_data(PAYMENTS_FILE)

    if value.upper() != "ALL":
        try:
            student_id = int(value)

            if student_id <= 0:
                print("Enter a valid student ID or ALL.")
                return

        except ValueError:
            print("Enter a valid student ID or ALL.")
            return

        payments = [
            payment for payment in payments
            if payment["student_id"] == student_id
        ]

    if not payments:
        print("No payment records found.")
        return

    print("\n" + "-" * 78)
    print(
        f"{'Receipt':<10}{'Student ID':<13}"
        f"{'Student Name':<22}{'Date':<13}{'Amount':>12}"
    )
    print("-" * 78)

    for payment in sorted(
        payments,
        key=lambda item: (item["date"], item["id"])
    ):
        print(
            f"{payment['id']:<10}"
            f"{payment['student_id']:<13}"
            f"{payment['student_name'][:21]:<22}"
            f"{payment['date']:<13}"
            f"₹{payment['amount']:>10.2f}"
        )

    print("-" * 78)
    print(
        f"Total shown: ₹"
        f"{sum(float(payment['amount']) for payment in payments):.2f}"
    )


def show_pending_fees():
    students = read_data(STUDENTS_FILE)
    month = current_month()
    total_pending = 0.0
    found = False

    print(f"\nPending hostel fees for {month}")
    print("-" * 65)

    for student in students:
        if not student["active"]:
            continue

        fee = float(student["monthly_fee"])
        paid = monthly_paid(student["id"], month)
        pending = max(0, round(fee - paid, 2))

        if pending > 0:
            found = True
            total_pending += pending

            print(
                f"ID: {student['id']} | {student['name']} | "
                f"Due: ₹{pending:.2f}"
            )

    if not found:
        print("No pending fees for the current month.")

    print("-" * 65)
    print(f"Total pending: ₹{total_pending:.2f}")
