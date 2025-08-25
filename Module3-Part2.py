# Alarm Clock Time Calculator
# Calculates what time an alarm will go off on a 24-hour clock

def alarm_clock_calculator():
    while True:
        try:
            # Ask the user for the current time in hours (0-23)
            current_hour = int(input("Enter the current hour (0–23): "))
            
            # Validate that current_hour is within valid 24-hour range
            if current_hour < 0 or current_hour > 23:
                print("Invalid hour. Please enter a number between 0 and 23.")
                continue

            # Ask the user for the number of hours to wait for the alarm
            wait_hours = int(input("Enter number of hours to wait for the alarm: "))
            
            if wait_hours < 0:
                print("Wait time cannot be negative. Please enter a valid number.")
                continue

            # Compute the alarm time using modulo arithmetic
            alarm_time = (current_hour + wait_hours) % 24

            # Display result with formatting
            print("\n----- Alarm Clock -----")
            print(f"Current Time: {current_hour:02d}:00 hours")
            print(f"Wait Hours:   {wait_hours}")
            print(f"Alarm Time:   {alarm_time:02d}:00 hours (24-hour clock)")
            print("-----------------------")
            break  # Exit loop once valid input is processed

        except ValueError:
            # Handle non-integer input
            print("Invalid input. Please enter numeric values only.")

# Run the calculator
alarm_clock_calculator()