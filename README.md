# Description
The New York Times' game Wordle, now on a Raspberry Pi Zero! Program is displayed on an LTP-2558AA series LED Multicolour Matrix Display through user manipulation in command line arguments.
RPi.GPIO, random, and time libraries are used.

Users have eight guesses on the display to find the randomly selected word from a text file containing five-letter words. When a user enters a guess:

1.	Entered word is checked by program: must be a valid five-letter word.
    If not, the program will display an error message and ask the user to try again.
2.	If this criteria is met, guessed entry is compared to the target word.
3.	Each attempt represents a row on the display. The row will display:
   
    a.	Green on the LED corresponding to letter position in word, only if that letter is in the 
        word, and it is in the correct spot.
  	
    b.	Yellow on the LED corresponding to letter position in word, only if that letter is in 
        the word, but it is not in the correct spot.
  	
    c.	Red on the LED corresponding to letter position in word, only if that letter is not in 
        the word.
  	
4.	If guess is correct, win message is displayed and LEDs flash green.
5.	If user runs out of attempts, lose message is displayed and LEDs flash red.

The display is connected to every available pin on a Raspberry Pi Cobbler Breakout Board. 
This allows control over each individual row and column on the display. 
HIGH/LOW are set for operation of LEDs.
Each LED on the matrix is controlled with two separate green and red LEDs. Pulse width modulation (PWM) is used to lower the brightness of the red LED, creating a yellow output.

My program was wired as follows:

---Row 1 = GPIO 17 (G) + 21 (R)---

---Row 2 = GPIO 27 (G) + 22 (R)---

---Row 3 = GPIO 0  (G) + 16 (R)---

---Row 4 = GPIO 23 (G) + 24 (R)---

---Row 5 = GPIO 9  (G) + 10 (R)---

---Row 6 = GPIO 1  (G) + 2  (R)---

---Row 7 = GPIO 13 (G) + 18 (R)---

---Row 8 = GPIO 3  (G) + 4  (R)---


|||Column 1 GPIO 25 (G) + 26 (R)|||

|||Column 2 GPIO 5  (G) + 6  (R)|||

|||Column 3 GPIO 7  (G) + 8  (R)|||

|||Column 4 GPIO 19 (G) + 20 (R)|||

|||Column 5 GPIO 11 (G) + 12 (R)|||

Datasheet for understanding row and column pinouts.

![image](https://github.com/user-attachments/assets/dcb4ac0a-8d9d-4240-b492-76c7c90ead19)

# Execution
Install Putty or whichever program allows communication through a TTL-serial cable (drivers may be needed):

https://embetronicx.com/uncategorized/fixed-prolific-pl2303ta-usb-to-serial-and-windows-11/ (for Windows).

Wires to connect to the Pi Cobbler Breakout Board are TXD, RXD, and GND.

If using Putty, create a Serial connection type, set Speed to 115200, and Serial line to COMXX, where XX is the number of the port, found in device manager under Ports:

![image](https://github.com/user-attachments/assets/4259d618-c931-406b-be17-0476233cefee)

![image](https://github.com/user-attachments/assets/6dcaf2fe-f226-4751-844d-6953a028feab)

Wire the LTP-2558AA series matrix display to the Pi Cobbler.
My design was a bit messy, but this is what it looked like:
![IMG_1124](https://github.com/user-attachments/assets/7a8329f6-e738-4d55-b0c2-bc5e33c4bcd9)
If needed, follow the wiring guide provided above.

Make sure to attatch resistors to cathodes to ensure LED operation. In my case, I used 220 Ohms for each column on the display.
Place column wires before or after resistors on column pins.

Download wordle.py and 5_letter_bank.txt to your device.
Ensure the text file is placed on your Pi, whether through mounting, online copying, or any method.

In a command terminal (Windows CMD, Powershell, Terminal, etc.) navigate to downloads using the "cd" command 
(for example: C:\User\fstan> cd Downloads) or wherever the files have been saved. 

Run the game file using "python wordle.py".

Now, your device should be communicating with the Pi and the display, given by the welcome message when running the program. Now you can input guesses for Wordle, and the display will reflect your results.

Errors may occur if python is not installed on your local terminal. If so, make sure to download the correct version for your system.

Wordle GPIO Setup.txt contains some code that might prove useful for testing display functionality.

# Difficulties
The major challenge of this device was understanding how the display itself works when activating green, red, or both LEDs. 

I started with wiring rows 6, 7, 8 and their pins to GPIO pins, and grounding 220Ω resistors to the column pins. I faced a dilemma in testing:

Output high for GPIO 1 and output low for GPIO 25 turns Row 6 Column 1 green LED on.

Output high for GPIO 2 and output low for GPIO 26 turns Row 6 Column 1 red LED on.

Combine both, and Row 6 Column 1 LED turns orange.

However, the following rows (7 and 8) will copy what the row above displays due to the columns having set values for the whole LED matrix. Inserting wires before the resistors on the column pins allowed more functionality with the display, but not enough to avoid the “inheritance problem” as I called it; column values are set for the whole display, not individual rows.

The issue here for a game like Wordle is it allows users to see their previous entries and what the results were. This is sadly unachievable from a hardware aspect. Example:

![image](https://github.com/user-attachments/assets/459e0458-1a8f-48b4-b252-b242b3671782)

This result cannot be displayed properly, as a yellow LED requires green and red to be active on Row 2 and Column 2. Following the matrix wiring, Row 3 Column 2 would become yellow instead of the required green as the column still has red active to accurately show the previous guess’ results. In light of this, the previous guesses are not shown, and attempts cycle down from the first row to the last.

Another challenge concerned activating PWM. LEDs will turn on based on column activation. Rows are always active for both green and red, allowing column activation to control exactly what colour is produced for each LED in a row. However, with columns: HIGH = off and LOW = on due to the need for GND on the LED cathodes.

The way to utilize PWM in code for the columns then, is to set frequency to 5000Hz to reduce flickering in the red LED, and when changing the duty cycle, remembering:

100 = off and 0 = on, again, since columns need to be grounded for LEDs to turn on.

# Useful URLs
The game my program is based on:

https://www.nytimes.com/games/wordle/index.html

Rules for the game are found here, giving a basis of what the program must accomplish. Edge cases are discerned from here as well, all to mimic the original game better. Example:

![image](https://github.com/user-attachments/assets/0749ac85-f828-49dc-935f-1497e7276f8f)

Initially the program would take this guess, and
display the second ‘R’ as yellow instead of the
required gray, implying the word had an incorrect 
amount of 3 ‘R’s and not the correct amount of 2.

Source for used text file containing the list of five-letter words:

https://charlesreid1.com/wiki/Five_Letter_Words

This allowed for the program to create a list of words to randomly choose from with ease. Only requirements were mounting a USB to copy the file, and the Pi can access it.

Having a random word bank to choose from every time the program is run mimics Wordle’s style of a new word every time you play.

Datasheet for the LTP-2558AA and similar models:

http://denethor.wlu.ca/pc300/projects/sensors/LPT2558AA.pdf

Without this datasheet, understanding the device would have been much more difficult. With this, finding Pin 1, knowing what each pin activates, and how to manipulate the green and red LEDs for the whole matrix made wiring the device to GPIO pins a simple task.

# Future Improvements
Working with a display such as this was limiting, but trial and error, with lots of experimentation proved a useful commitment to my resilience.

I would hope to work with a MAX7219 Matrix Display as it seems much more suited to my uses.
