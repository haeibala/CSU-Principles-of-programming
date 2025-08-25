# Meal Price Calculator with Tip and Tax
# Calculates the total cost of a meal including 18% tip and 7% sales tax

def meal_price_calculator():
    while True:
        try:
            # Ask the user for the food charge
            food_charge = float(input("Enter the charge for the food: $"))
            
            # Validate that the input is positive
            if food_charge < 0:
                print("Food charge cannot be negative. Please try again.")
                continue

            # Calculate tip (18%) and sales tax (7%)
            tip = food_charge * 0.18
            tax = food_charge * 0.07
            total = food_charge + tip + tax

            # Display results with two decimal places
            print("\n----- Receipt -----")
            print(f"Food Charge:   ${food_charge:.2f}")
            print(f"Tip (18%):     ${tip:.2f}")
            print(f"Sales Tax (7%):${tax:.2f}")
            print(f"Total Price:   ${total:.2f}")
            print("-------------------")
            break  # Exit loop once valid input is processed

        except ValueError:
            # Handle non-numeric input
            print("Invalid input. Please enter a valid number for the food charge.")

# Run the calculator
meal_price_calculator()