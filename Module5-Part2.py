# Part 2: CSU Global Book Club Points
# - Robust input validation for book count
# - Clear, maintainable mapping to points
# - Graceful handling of user cancellation

def prompt_nonnegative_int(message: str) -> int:
    """Prompt until the user enters an integer >= 0."""
    while True:
        try:
            raw = input(message + " ").strip()
            n = int(raw)
            if n >= 0:
                return n
            print("Please enter an integer 0 or greater.")
        except ValueError:
            print("Invalid input. Please enter a whole number.")
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            raise SystemExit(1)

def book_club_points() -> None:
    books = prompt_nonnegative_int("Enter the number of books purchased this month:")

    # Descending thresholds ensure ranges are handled correctly
    if books >= 8:
        points = 60
    elif books >= 6:
        points = 30
    elif books >= 4:
        points = 15
    elif books >= 2:
        points = 5
    else:
        points = 0

    print(f"Points earned: {points}")

if __name__ == "__main__":
    try:
        book_club_points()
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        raise SystemExit(1)
