from storage import initialize_storage
from student_manager import (
    add_student,
    list_students,
    search_student,
    checkout_student
)
from room_manager import (
    add_room,
    list_rooms,
    transfer_student
)
from fee_manager import (
    record_payment,
    view_payment_history,
    show_pending_fees
)
from report_manager import (
    dashboard,
    room_occupancy_report,
    payment_summary
)
from utils import pause


def display_menu():
    print("\n" + "=" * 48)
    print("          HOSTEL MANAGEMENT SYSTEM")
    print("=" * 48)
    print("1.  Dashboard")
    print("2.  Add Room")
    print("3.  View Rooms")
    print("4.  Register Student")
    print("5.  View Active Students")
    print("6.  View All Students")
    print("7.  Search Student")
    print("8.  Transfer Student to Another Room")
    print("9.  Check Out Student")
    print("10. Record Fee Payment")
    print("11. View Payment History")
    print("12. View Pending Fees")
    print("13. Room Occupancy Report")
    print("14. Monthly Payment Summary")
    print("0.  Exit")
    print("=" * 48)


def main():
    initialize_storage()

    actions = {
        "1": dashboard,
        "2": add_room,
        "3": list_rooms,
        "4": add_student,
        "5": list_students,
        "6": lambda: list_students(show_inactive=True),
        "7": search_student,
        "8": transfer_student,
        "9": checkout_student,
        "10": record_payment,
        "11": view_payment_history,
        "12": show_pending_fees,
        "13": room_occupancy_report,
        "14": payment_summary
    }

    while True:
        display_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "0":
            print("Thank you for using Hostel Management System.")
            break

        action = actions.get(choice)

        if action:
            try:
                action()
            except (OSError, ValueError, KeyError, TypeError) as error:
                print(f"Could not complete this operation: {error}")
        else:
            print("Invalid choice. Please select a listed option.")

        if choice != "0":
            pause()


if __name__ == "__main__":
    main()
