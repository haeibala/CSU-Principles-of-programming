# Part 2: Multiplication and Division
num1 = float(input("Enter the first number: "))
num2 = float(input("Enter the second number: "))

multiplication = num1 * num2

# Avoid division by zero
if num2 != 0:
    division = num1 / num2
    print(f"Multiplication result: {multiplication}")
    print(f"Division result: {division}")
else:
    print("Division by zero is not allowed.")
