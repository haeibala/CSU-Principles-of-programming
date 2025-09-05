from typing import Tuple


class ItemToPurchase:
    """
    Represents a purchasable item with a name, unit price, and quantity.

    The class provides:
      - total_cost(): compute price * quantity.
      - print_item_cost(): print in the exact format required by the assignment.
    """

    def __init__(self) -> None:
        # Defaults per specification
        self.item_name: str = "none"
        self.item_price: float = 0.0
        self.item_quantity: int = 0

    def total_cost(self) -> float:
        """Compute the total cost for this item."""
        # Guard against unexpected numeric anomalies
        price = self.item_price if self.item_price >= 0 else 0.0
        qty = self.item_quantity if self.item_quantity >= 0 else 0
        return price * qty

    def print_item_cost(self) -> None:
        """
        Print cost line in assignment format.

        Example:
            Bottled Water 10 @ $1 = $10
        The sample output uses integer formatting for price and total.
        """
        total = self.total_cost()
        print(f"{self.item_name} {self.item_quantity} @ ${int(self.item_price)} = ${int(total)}")


def prompt_nonempty_string(prompt_text: str) -> str:
    """
    Prompt for a nonempty string. On user cancel, return 'none'.
    Handles EOFError and KeyboardInterrupt gracefully.
    """
    while True:
        try:
            s = input(prompt_text).strip()
            if s:
                return s
            print("Input cannot be empty. Please try again.")
        except (EOFError, KeyboardInterrupt):
            print("Input cancelled. Defaulting to 'none'.")
            return "none"


def prompt_nonnegative_float(prompt_text: str) -> float:
    """
    Prompt for a nonnegative float. On invalid entry, re-prompt.
    On user cancel, return 0.0.

    This defends against ValueError and user cancellation.
    """
    while True:
        try:
            s = input(prompt_text).strip()
            value = float(s)
            if value >= 0:
                return value
            print("Value must be nonnegative. Please try again.")
        except ValueError:
            print("Enter a valid number. Example: 3 or 3.0.")
        except (EOFError, KeyboardInterrupt):
            print("Input cancelled. Defaulting to 0.")
            return 0.0


def prompt_nonnegative_int(prompt_text: str) -> int:
    """
    Prompt for a nonnegative integer. Reject fractional inputs.
    On user cancel, return 0.

    This defends against ValueError and user cancellation.
    """
    while True:
        try:
            s = input(prompt_text).strip()
            # Explicitly disallow fractional quantities like "2.5"
            if "." in s:
                raise ValueError("Quantity must be a whole number.")
            value = int(s)
            if value >= 0:
                return value
            print("Quantity must be nonnegative. Please try again.")
        except ValueError:
            print("Enter a whole number. Example: 0, 1, 2.")
        except (EOFError, KeyboardInterrupt):
            print("Input cancelled. Defaulting to 0.")
            return 0


def collect_item(label: str) -> ItemToPurchase:
    """
    Collect a single item's details from the user.

    Prompts for name, price, and quantity with robust validation.
    """
    print(label)
    item = ItemToPurchase()
    item.item_name = prompt_nonempty_string("Enter the item name: ")
    item.item_price = prompt_nonnegative_float("Enter the item price: ")
    item.item_quantity = prompt_nonnegative_int("Enter the item quantity: ")
    return item


def main() -> None:
    """
    Main program flow:
      - Prompt for two items
      - Print each cost line
      - Print total
    All inputs validated. Output matches assignment format.
    """
    # Collect two items with clear sectioning
    item1 = collect_item("Item 1")
    print()  # blank line for readability
    item2 = collect_item("Item 2")

    # Output section
    print("\nTOTAL COST")
    item1.print_item_cost()
    item2.print_item_cost()

    # Sum total with numeric safety. Division by zero is not applicable here,
    # but we still safeguard by ensuring nonnegatives in total_cost().
    total = item1.total_cost() + item2.total_cost()
    print(f"\nTotal: ${int(total)}")


if __name__ == "__main__":
    # Top-level guard ensures clean module import behavior and straightforward execution.
    main()