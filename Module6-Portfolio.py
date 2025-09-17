"""
Shopping Cart Program — Combined Single File
- Integrates the enhanced ShoppingCart solution with prior steps
- Robust input validation, exception safety, and detailed comments
- Backward-compatible method names to reduce breakage with earlier steps

Run:
  python ShoppingCart_Combined.py

Features:
- ItemToPurchase with validated update(...) setter per feedback
- ShoppingCart with add_item, remove_item, modify_item, get_num_items_in_cart,
  get_cost_of_cart, print_total, print_descriptions
- Interactive print_menu(cart) implementing options a, r, c, i, o, q
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional
import sys


# ==============================
# Input helper utilities
# ==============================

def prompt_nonempty_string(message: str, *, default: str = "none") -> str:
    """
    Prompt the user for a non-empty string.
    Returns 'default' if the user cancels with Ctrl+C or sends EOF.
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
    Prompt the user for a non-negative integer.
    Returns 'default' if the user cancels input.
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
    Prompt the user for a non-negative float.
    Returns 'default' if the user cancels input.
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


# ==============================
# ItemToPurchase
# ==============================

@dataclass
class ItemToPurchase:
    """
    Represents a purchasable item.
    Fields match the common zyBooks-style spec used in earlier steps.
    """
    item_name: str = "none"
    item_price: float = 0.0
    item_quantity: int = 0
    item_description: str = "none"

    def total_cost(self) -> float:
        """Return price * quantity, guarding against negative values."""
        price = self.item_price if self.item_price >= 0 else 0.0
        qty = self.item_quantity if self.item_quantity >= 0 else 0
        return price * qty

    def print_item_cost(self) -> None:
        """
        Print in the assignment's integer-format style:
        <name> <qty> @ $<price> = $<total>
        """
        total = self.total_cost()
        print(f"{self.item_name} {self.item_quantity} @ ${int(self.item_price)} = ${int(total)}")

    def print_item_description(self) -> None:
        """Print '<name>: <description>' to match earlier steps."""
        print(f"{self.item_name}: {self.item_description}")

    # Enhancement: validated dynamic updates per instructor feedback
    def update(
        self,
        *,
        name: Optional[str] = None,
        description: Optional[str] = None,
        price: Optional[float] = None,
        quantity: Optional[int] = None,
    ) -> None:
        """
        Update one or more fields with validation.
        - name and description must be non-empty if provided
        - price and quantity must be nonnegative if provided
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
            if price < 0:
                raise ValueError("Item price cannot be negative.")
            self.item_price = float(price)
        if quantity is not None:
            if not isinstance(quantity, int):
                raise ValueError("Item quantity must be a whole number.")
            if quantity < 0:
                raise ValueError("Item quantity cannot be negative.")
            self.item_quantity = quantity


# ==============================
# ShoppingCart
# ==============================

@dataclass
class ShoppingCart:
    """
    Shopping cart with required behaviors per assignment.
    """
    customer_name: str = "none"
    current_date: str = "January 1, 2020"
    cart_items: List[ItemToPurchase] = field(default_factory=list)

    def add_item(self, item_to_purchase: ItemToPurchase) -> None:
        """Append an item to the cart."""
        self.cart_items.append(item_to_purchase)

    def remove_item(self, item_name: str) -> None:
        """
        Remove by name, case-insensitive.
        If not found, print the required message.
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
        Only modify description, price, quantity when non-default values are passed.
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
        """Return total quantity across all items."""
        return sum(max(0, it.item_quantity) for it in self.cart_items)

    def get_cost_of_cart(self) -> float:
        """Return total cost across all items."""
        return sum(it.total_cost() for it in self.cart_items)

    def print_total(self) -> None:
        """Print the cart total in the assignment's format."""
        print(f"{self.customer_name}'s Shopping Cart - {self.current_date}")
        num_items = self.get_num_items_in_cart()
        print(f"Number of Items: {num_items}")
        if num_items == 0:
            print("SHOPPING CART IS EMPTY")
            return
        for it in self.cart_items:
            it.print_item_cost()
        print(f"Total: ${int(self.get_cost_of_cart())}")

    def print_descriptions(self) -> None:
        """Print item descriptions in the assignment's format."""
        print(f"{self.customer_name}'s Shopping Cart - {self.current_date}")
        print("Item Descriptions")
        for it in self.cart_items:
            it.print_item_description()


# ==============================
# Menu
# ==============================

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
    Interactive loop that continues until the user chooses 'q'.
    All branches handle input errors and continue gracefully.
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
            # Add item flow
            name = prompt_nonempty_string("Enter the item name: ")
            desc = prompt_nonempty_string("Enter the item description: ")
            price = prompt_nonnegative_float("Enter the item price: ")
            qty = prompt_nonnegative_int("Enter the item quantity: ")
            item = ItemToPurchase(item_name=name, item_description=desc, item_price=price, item_quantity=qty)
            cart.add_item(item)
        elif choice == "r":
            name = prompt_nonempty_string("Enter name of item to remove: ")
            cart.remove_item(name)
        elif choice == "c":
            name = prompt_nonempty_string("Enter the item name to modify: ")
            qty = prompt_nonnegative_int("Enter the new quantity: ")
            stub = ItemToPurchase(item_name=name, item_quantity=qty)
            cart.modify_item(stub)
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


# ==============================
# Entry point
# ==============================

def main() -> None:
    """Collect header info and start the menu loop."""
    print("Shopping Cart Program")
    customer_name = prompt_nonempty_string("Enter customer's name: ")
    current_date = prompt_nonempty_string("Enter today's date: ")
    cart = ShoppingCart(customer_name=customer_name, current_date=current_date)
    print_menu(cart)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"\nAn unexpected error occurred: {exc}")
        sys.exit(1)
