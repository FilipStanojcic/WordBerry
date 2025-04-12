import RPi.GPIO as GPIO
import time
import random

# Generate word list from given file

def load_word_list(filename):
        with open(filename, "r") as file:
                words = [line.strip().upper() for line in file]
        return words

# Select target word at random

WORD_LIST = load_word_list("5_letter_bank.txt")
TARGET_WORD = random.choice(WORD_LIST)

# Row and column GPIO pins for 5x8 matrix

ROWS = [(17, 21), (27, 22), (0, 16), (23, 24), (9, 10), (1, 2), (13, 18), (3, 4)]
COLUMNS = [(25, 26), (5, 6), (7, 8), (19, 20), (11, 12)]

GPIO.setmode(GPIO.BCM)

pwm_pins = {}

# Row and column pin setup for display control

for green_pin, red_pin in ROWS:
        GPIO.setup(green_pin, GPIO.OUT)
        GPIO.setup(red_pin, GPIO.OUT)
        pwm_pins[green_pin] = GPIO.PWM(green_pin, 5000) #5000Hz
        pwm_pins[red_pin] = GPIO.PWM(red_pin, 5000) #5000Hz
        pwm_pins[green_pin].start(0) # Start with LEDs off
        pwm_pins[red_pin].start(0)

for green_pin, red_pin in COLUMNS:
        GPIO.setup(green_pin, GPIO.OUT)
        GPIO.setup(red_pin, GPIO.OUT)
        pwm_pins[green_pin] = GPIO.PWM(green_pin, 5000)
        pwm_pins[red_pin] = GPIO.PWM(red_pin, 5000)
        pwm_pins[green_pin].start(100) # Start with LEDs off (100% duty cycle for columns = off)
        pwm_pins[red_pin].start(100)

# Function to compare user guess with target word and return feedback (green/yellow/off)

def evaluate_guess(guess):
        feedback = ["off"] * 5 # Default feedback (all letters off)
        
	# Count occurrences of letters in the target word

	word_letter_count = {}
        for letter in TARGET_WORD:
                word_letter_count[letter] = word_letter_count.get(letter, 0) + 1
       
	used_letters = {} # Track letter usage to avoid marking duplicates incorrectly

	# First pass to mark correct positions (green)

        for i, letter in enumerate(guess):
                if letter == TARGET_WORD[i]: # Letter is in the correct position
                        feedback[i] = "green"
                        used_letters[letter] = used_letters.get(letter, 0) + 1
	
	# Second pass to mark correct letters in wrong positions (yellow)

        for i, letter in enumerate(guess):
                if feedback[i] == "off" and letter in TARGET_WORD: # Not in correct position
                        if used_letters.get(letter, 0) < word_letter_count.get(letter, 0):
                                feedback[i] = "yellow"
                                used_letters[letter] = used_letters.get(letter, 0) + 1
        return feedback

def display_row(row_index, feedback):
        
	# Turn off all rows before displaying new row

	for green_row, red_row in ROWS:
                pwm_pins[green_row].ChangeDutyCycle(0)
                pwm_pins[red_row].ChangeDutyCycle(0)

	# Activate current row

        green_row, red_row = ROWS[row_index]
        pwm_pins[green_row].ChangeDutyCycle(100)
        pwm_pins[red_row].ChangeDutyCycle(22)

	# Set column colours based on feedback

        for col_index in range(len(COLUMNS)):
                green_col, red_col = COLUMNS[col_index]
                if feedback[col_index] == "green": # Correct position
                        pwm_pins[green_col].ChangeDutyCycle(0)
                        pwm_pins[red_col].ChangeDutyCycle(100)
                elif feedback[col_index] == "yellow": # Wrong position
                        pwm_pins[green_col].ChangeDutyCycle(0)
                        pwm_pins[red_col].ChangeDutyCycle(0)
                else: # Incorrect letter
                        pwm_pins[green_col].ChangeDutyCycle(100)
                        pwm_pins[red_col].ChangeDutyCycle(0)

def win_animation():
        for duty_cycle in range(100, -1, -5):
                for col in COLUMNS:
                        pwm_pins[col[0]].ChangeDutyCycle(duty_cycle)
                        pwm_pins[col[1]].ChangeDutyCycle(100)

        for _ in range(8):
                for col in COLUMNS:
                        pwm_pins[col[0]].ChangeDutyCycle(0)

                time.sleep(0.2)

                for col in COLUMNS:
                        pwm_pins[col[0]].ChangeDutyCycle(100)

                time.sleep(0.2)

def lose_animation():
        for green_row, red_row in ROWS:
                GPIO.output(green_row, GPIO.LOW)
                GPIO.output(red_row, GPIO.LOW)

        for green_col, red_col in COLUMNS:
                pwm_pins[green_col].ChangeDutyCycle(100)
                pwm_pins[red_col].ChangeDutyCycle(100)

        time.sleep(0.5)

        for _ in range(4):
                for green_row, red_row in ROWS:
                        GPIO.output(red_row, GPIO.HIGH)

                for green_col, red_col in COLUMNS:
                        pwm_pins[red_col].ChangeDutyCycle(0)

                time.sleep(0.5)

                for green_row, red_row in ROWS:
                        GPIO.output(red_row, GPIO.LOW)

                for green_col, red_col in COLUMNS:
                        pwm_pins[red_col].ChangeDutyCycle(100)

                time.sleep(0.5)


try:
        row_index = 0
        print("Welcome to Wordle!")
        while row_index < len(ROWS):

		# Input validation loop

                while True:
                        guess = input(f"Enter a 5-letter guess (Attempt #{row_index+1}): ").upper()
                        if len(guess) == 5 and guess.isalpha() and guess in WORD_LIST:
                                break
                        print("Invalid guess! Please try again.")

		# Evaluate guess and update LEDs

                feedback = evaluate_guess(guess)
                display_row(row_index, feedback)

		# Check for win condition

                if guess == TARGET_WORD:
                        print(f"You guessed it in {row_index+1}!")
                        win_animation()
                        break

                row_index += 1

	# If all rows are used, reveal the correct word

        if row_index == len(ROWS):
                print(f"Out of attempts! The word was **{TARGET_WORD}**.")
                lose_animation()

except KeyboardInterrupt:
        print("Cleaning up...")

finally:
        GPIO.cleanup()
