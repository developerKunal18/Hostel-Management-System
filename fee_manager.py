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
        (s for s in students if s["id"] == student_id),
        None
    )


def monthly_paid(student_id, month):
    payments = read_data(PAYMENTS_FILE)

    return round(
        sum(
            payment["amount"]
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

    month = current_month()
    fee = float(student["monthly_fee"])
    already_paid = monthly_paid(student_id, month)
    remaining = max(0, round(fee - already_paid, 2))

    print(f"Student: {student['name']}")
    print(f"Monthly fee: ₹{fee:.2f}")
    print(f"Paid for {month}: ₹{already_paid:.2f}")
    print(f"Remaining for {month}: ₹{remaining:.2f}")

    if remaining == 0:
        print("This month's fee is already paid in full.")
        return

    amount = input_positive_float("Enter payment amount: ")

    if amount > remaining:
        print(f"Payment cannot exceed the remaining fee of ₹{remaining:.2f}.")
        return

    payment_date = input_date(
        f"Enter payment date YYYY-MM-DD (blank for {today()}): ",
        allow_blank=True
    )

    # Prevent a payment dated in a different month from exceeding that
    # month's fee. Payments are recorded against their payment date.
    target_month = payment_date[:7]
    paid_for_target_month = monthly_paid(student_id, target_month)
    remaining_for_target_month = max(
        0, round(fee - paid_for_target_month, 2)
    )

    if amount > remaining_for_target_month:
        print(
            f"Payment exceeds the remaining fee for {target_month}: "
            f"₹{remaining_for_target_month:.2f}."
        )
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
    student_id = input_positive_int(
        "Enter student ID, or enter 0 to view all payments: "
    )

    payments = read_data(PAYMENTS_FILE)

    if student_id != 0:
        payments = [
            p for p in payments if p["student_id"] == student_id
        ]

    if not payments:
        print("No payments found.")
        return

    print("\n" + "-" * 78)
    print(f"{'Receipt':<10}{'Student ID':<13}{'Student Name':<22}{'Date':<13}{'Amount':>12}")
    print("-" * 78)

    for payment in sorted(payments, key=lambda p: (p["date"], p["id"])):
        print(
            f"{payment['id']:<10}"
            f"{payment['student_id']:<13}"
            f"{payment['student_name'][:21]:<22}"
            f"{payment['date']:<13}"
            f"₹{payment['amount']:>10.2f}"
        )


def show_pending_fees():
    students = read_data(STUDENTS_FILE)
    month = current_month()
    found = False
    total_pending = 0.0

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
