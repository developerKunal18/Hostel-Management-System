from datetime import date, datetime


def today():
    return date.today().isoformat()


def current_month():
    return date.today().strftime("%Y-%m")


def input_required(prompt):
    while True:
        value = input(prompt).strip()

        if value:
            return value

        print("This field is required.")


def input_positive_int(prompt):
    while True:
        try:
            value = int(input(prompt).strip())

            if value > 0:
                return value

            print("Enter a number greater than zero.")

        except ValueError:
            print("Please enter a valid whole number.")


def input_positive_float(prompt):
    while True:
        try:
            value = float(input(prompt).strip())

            if value > 0:
                return round(value, 2)

            print("Enter an amount greater than zero.")

        except ValueError:
            print("Please enter a valid amount.")


def input_date(prompt, allow_blank=False):
    while True:
        value = input(prompt).strip()

        if not value and allow_blank:
            return today()

        try:
            parsed_date = datetime.strptime(value, "%Y-%m-%d").date()

            if parsed_date > date.today():
                print("The date cannot be in the future.")
                continue

            return parsed_date.isoformat()

        except ValueError:
            print("Enter a valid date in YYYY-MM-DD format.")


def pause():
    input("\nPress Enter to continue...")
