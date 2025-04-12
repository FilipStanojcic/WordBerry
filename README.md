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

The display is connected to every availalbe pin on a Raspberry Pi Cobbler Breakout Board. 
This allows control over each individual row and column on the display. 
HIGH/LOW are set for operation of LEDs. P
Each LED on the matrix is controlled with two separate green and red LEDs. Pulse width modulation is used to lower the brightness of the red LED, creating a yellow output.

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

# Difficulties


# Future Improvements
