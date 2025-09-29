"""
Online Shopping Cart — Final Consolidated Solution
Completes Steps 1–10 with robust validation, exception safety, and clear I/O.

Features:
- ItemToPurchase with name, price, quantity, description, print helpers, and validated update()
- ShoppingCart with add, remove, modify, totals, descriptions, and required messages
- Interactive print_menu loop supporting options a, r, c, i, o, q
- Defensive input helpers for strings, ints, floats
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Mapping
import sys


# ---------------------------
# Formatting helper
# ---------------------------

def money_str(x: float) -> str:
    """
    Render a monetary value without losing cents.
    If the value is an integer, print as integer. Otherwise print with two decimals.
    """
    try:
        if float(x).is_integer():
            return f"{int(round(x))}"
        return f"{x:.2f}"
    except Exception:
        # Fallback for pathological inputs
        return f"{x}"


# ---------------------------
# Input helpers
# ---------------------------

def prompt_nonempty_string(message: str, *, default: str = "none") -> str:
    """
    Prompt for a non-empty string, trimming whitespace.
    Returns default on Ctrl+C or EOF to keep the program resilient.
    """
    while True:
        try:
            s = input(message).strip()
            if s:
                return s
            print("Input cannot be empty. Please try again.")
        except (EOFError, KeyboardInterrupt):
            print("\nInput cancelled. Using default.")
            return default


def prompt_nonnegative_int(message: str, *, default: int = 0) -> int:
    """
    Prompt for a non-negative integer. Returns default on Ctrl+C or EOF.
    """
    while True:
        try:
            raw = input(message).strip()
            if raw == "":
                print("Please enter a whole number.")
                continue
            if "." in raw:
                raise ValueError("Quantity must be a whole number.")
            n = int(raw)
            if n < 0:
                print("Value must be nonnegative.")
                continue
            return n
        except ValueError:
            print("Invalid input. Enter a whole number such as 0, 1, 2.")
        except (EOFError, KeyboardInterrupt):
            print("\nInput cancelled. Using default.")
            return default


def prompt_nonnegative_float(message: str, *, default: float = 0.0) -> float:
    """
    Prompt for a non-negative float. Returns default on Ctrl+C or EOF.
    """
    while True:
        try:
            raw = input(message).strip()
            x = float(raw)
            if x < 0:
                print("Value must be nonnegative.")
                continue
            return x
        except ValueError:
            print("Invalid input. Enter a number such as 3 or 3.5.")
        except (EOFError, KeyboardInterrupt):
            print("\nInput cancelled. Using default.")
            return default


# ---------------------------
# ItemToPurchase
# ---------------------------

@dataclass
class ItemToPurchase:
    """
    Represents a purchasable item with optional description.
    Default constructor sets 'none' or 0 values per specification.
    """
    item_name: str = "none"
    item_price: float = 0.0
    item_quantity: int = 0
    item_description: str = "none"

    def total_cost(self) -> float:
        """Return nonnegative price * nonnegative quantity."""
        price = self.item_price if self.item_price >= 0 else 0.0
        qty = self.item_quantity if self.item_quantity >= 0 else 0
        return price * qty

    def print_item_cost(self) -> None:
        """
        Print in required format:
        <name> <qty> @ $<price> = $<total>
        Price and total are shown in integer form if whole dollars,
        else two decimals.
        """
        total = self.total_cost()
        print(f"{self.item_name} {self.item_quantity} @ ${money_str(self.item_price)} = ${money_str(total)}")

    def print_item_description(self) -> None:
        """Print '<name>: <description>'."""
        print(f"{self.item_name}: {self.item_description}")

    def update(
        self,
        *,
        name: Optional[str] = None,
        description: Optional[str] = None,
        price: Optional[float] = None,
        quantity: Optional[int] = None,
    ) -> None:
        """
        Validated partial update.
        - name and description must be non-empty if provided
        - price must be nonnegative if provided
        - quantity must be a nonnegative integer if provided
        """
        if name is not None:
            name = name.strip()
            if not name:
                raise ValueError("Item name cannot be empty.")
            self.item_name = name
        if description is not None:
            description = description.strip()
            if not description:
                raise ValueError("Item description cannot be empty.")
            self.item_description = description
        if price is not None:
            try:
                price = float(price)
            except Exception:
                raise ValueError("Item price must be a number.")
            if price < 0:
                raise ValueError("Item price cannot be negative.")
            self.item_price = price
        if quantity is not None:
            if not isinstance(quantity, int):
                raise ValueError("Item quantity must be a whole number.")
            if quantity < 0:
                raise ValueError("Item quantity cannot be negative.")
            self.item_quantity = quantity


# ---------------------------
# ShoppingCart
# ---------------------------

@dataclass
class ShoppingCart:
    """
    Encapsulates cart behavior and required printouts.
    """
    customer_name: str = "none"
    current_date: str = "January 1, 2020"
    cart_items: List[ItemToPurchase] = field(default_factory=list)

    def add_item(self, item_to_purchase: ItemToPurchase) -> None:
        """Append an item to the cart."""
        self.cart_items.append(item_to_purchase)

    def remove_item(self, item_name: str) -> None:
        """
        Remove the first matching item by case-insensitive name.
        Print required message if not found.
        """
        name = item_name.strip().lower()
        for i, it in enumerate(self.cart_items):
            if it.item_name.lower() == name:
                del self.cart_items[i]
                return
        print("Item not found in cart. Nothing removed.")

    def modify_item(self, item_to_purchase: ItemToPurchase) -> None:
        """
        Modify an existing item matched by name.
        Only apply fields that are not defaults:
          description != 'none', price != 0, quantity != 0.
        Print required message if item not found.
        """
        name = item_to_purchase.item_name.strip().lower()
        target: Optional[ItemToPurchase] = None
        for it in self.cart_items:
            if it.item_name.lower() == name:
                target = it
                break
        if target is None:
            print("Item not found in cart. Nothing modified.")
            return

        try:
            if item_to_purchase.item_description != "none":
                target.update(description=item_to_purchase.item_description)
            if item_to_purchase.item_price != 0:
                target.update(price=item_to_purchase.item_price)
            if item_to_purchase.item_quantity != 0:
                target.update(quantity=int(item_to_purchase.item_quantity))
        except ValueError as e:
            print(f"Modification rejected: {e}")

    def get_num_items_in_cart(self) -> int:
        """Return total quantity across all items, clamped at zero."""
        return sum(max(0, it.item_quantity) for it in self.cart_items)

    def get_cost_of_cart(self) -> float:
        """Return total cost across all items."""
        return sum(it.total_cost() for it in self.cart_items)

    def print_total(self) -> None:
        """Output the cart header, all item lines, and the total per specification."""
        print(f"{self.customer_name}'s Shopping Cart - {self.current_date}")
        num_items = self.get_num_items_in_cart()
        print(f"Number of Items: {num_items}")
        if num_items == 0:
            print("SHOPPING CART IS EMPTY")
            return
        for it in self.cart_items:
            it.print_item_cost()
        print(f"Total: ${money_str(self.get_cost_of_cart())}")

    def print_descriptions(self) -> None:
        """Output the cart header and each item's description."""
        print(f"{self.customer_name}'s Shopping Cart - {self.current_date}")
        print("Item Descriptions")
        for it in self.cart_items:
            it.print_item_description()


# ---------------------------
# Menu loop
# ---------------------------

MENU_TEXT = (
    "MENU\n"
    "a - Add item to cart\n"
    "r - Remove item from cart\n"
    "c - Change item quantity\n"
    "i - Output items' descriptions\n"
    "o - Output shopping cart\n"
    "q - Quit\n"
)

def print_menu(cart: ShoppingCart) -> None:
    """
    Interactive loop that continues until user enters 'q'.
    All branches are exception-safe and continue gracefully after errors.
    """
    while True:
        try:
            print(MENU_TEXT)
            choice = input("Choose an option: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nSession ended.")
            return

        if choice == "q":
            return

        elif choice == "a":
            print("\nADD ITEM TO CART")
            name = prompt_nonempty_string("Enter the item name: ")
            desc = prompt_nonempty_string("Enter the item description: ")
            price = prompt_nonnegative_float("Enter the item price: ")
            qty = prompt_nonnegative_int("Enter the item quantity: ")
            cart.add_item(ItemToPurchase(
                item_name=name,
                item_description=desc,
                item_price=price,
                item_quantity=qty
            ))

        elif choice == "r":
            print("\nREMOVE ITEM FROM CART")
            name = prompt_nonempty_string("Enter name of item to remove: ")
            cart.remove_item(name)

        elif choice == "c":
            print("\nCHANGE ITEM QUANTITY")
            name = prompt_nonempty_string("Enter the item name: ")
            qty = prompt_nonnegative_int("Enter the new quantity: ")
            # Only quantity is modified; other fields remain default to signal "no change"
            cart.modify_item(ItemToPurchase(item_name=name, item_quantity=qty))

        elif choice == "i":
            print("\nOUTPUT ITEMS' DESCRIPTIONS")
            cart.print_descriptions()
            print()

        elif choice == "o":
            print("\nOUTPUT SHOPPING CART")
            cart.print_total()
            print()

        else:
            print("Invalid choice. Please select a valid option.")


# ---------------------------
# Entry point
# ---------------------------

def main() -> None:
    """Collect customer header, echo, construct cart, and run the menu."""
    print("Shopping Cart Program")
    customer_name = prompt_nonempty_string("Enter customer's name: ")
    current_date = prompt_nonempty_string("Enter today's date: ")
    print(f"Customer name: {customer_name}")
    print(f"Today's date: {current_date}")
    cart = ShoppingCart(customer_name=customer_name, current_date=current_date)
    try:
        print_menu(cart)
    except Exception as e:
        # Last-resort guard so the program exits cleanly even if something unexpected occurs
        print(f"\nAn unexpected error occurred: {type(e).__name__}: {e}")

if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"\nFatal error: {type(exc).__name__}: {exc}")
        sys.exit(1)
