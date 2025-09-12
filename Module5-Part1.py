# Part 1: Average Rainfall Over a Period of Years
# - Robust input validation for years and rainfall
# - Graceful handling of KeyboardInterrupt (Ctrl+C)
# - No crashes on invalid input

from typing import Callable

def prompt_positive_int(message: str) -> int:
    """Prompt until the user enters an integer >= 1."""
    while True:
        try:
            raw = input(message + " ").strip()
            n = int(raw)
            if n >= 1:
                return n
            print("Please enter an integer 1 or greater.")
        except ValueError:
            print("Invalid input. Please enter a whole number.")
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            raise SystemExit(1)

def prompt_nonnegative_float(message: str) -> float:
    """Prompt until the user enters a float >= 0."""
    while True:
        try:
            raw = input(message + " ").strip()
            x = float(raw)
            if x >= 0:
                return x
            print("Please enter a number 0 or greater.")
        except ValueError:
            print("Invalid input. Please enter a numeric value.")
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            raise SystemExit(1)

def average_rainfall() -> None:
    years = prompt_positive_int("Enter the number of years:")
    total_rainfall = 0.0
    total_months = 0

    # Collect rainfall for each month of each year
    for year in range(1, years + 1):
        print(f"\nYear {year}")
        for month in range(1, 13):
            inches = prompt_nonnegative_float(
                f"  Enter the inches of rainfall for month {month}:"
            )
            total_rainfall += inches
            total_months += 1

    # Compute and display results
    average = total_rainfall / total_months  # safe: total_months == years * 12
    print("\nResults")
    print(f"  Total months: {total_months}")
    print(f"  Total inches of rainfall: {total_rainfall:.2f}")
    print(f"  Average rainfall per month: {average:.2f} inches")

if __name__ == "__main__":
    try:
        average_rainfall()
    except Exception as e:
        # Catch-all as a final safety net with a friendly message
        print(f"\nAn unexpected error occurred: {e}")
        raise SystemExit(1)
