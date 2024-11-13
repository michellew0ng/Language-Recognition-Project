# LED Control using Language Recognition

COMP3601 Project 24T3. Implementing voice recognition to control an LED. 
Developed by Michelle Wong, Hasitha Peter, and Natakorn Jaroenkitphan


## Milestone 5

![Blank diagram](https://github.com/user-attachments/assets/3ed24ee2-c884-4641-ad82-6464d482d598)

Milestone 5 builds upon Milestone 4 by sending the WAV file to a Python client for processing and interpretation and sending the resulting signal back to the Kria KV260 to control the state of the LED. The extension was not implemented fully due to time constraints.



### Hardware:
1. Kria KV260 FPGA
2. ADAFruit i2s MEMs Microphone
3. UNSW CSE Design Project A/B PMOD board
4. Ethernet cable

### Software:
1. Xilinx Vivado 2021.2
2. Whisper API
3. ChatGPT 4.0
4. Python3


### Instructions 
1. Connect an ethernet cable running between your Kira board and the PC.
2. sudo ifconfig eth0 192.168.1.2 netmask 255.255.255.0 to set an ip address for your kriaboard
3. Turn off firewall for your pc.
4. ping the kria ip address to check for connectivity between your pc terminal and kria board.
5. send the src and main files to board using pscp command.
6. Compile code for the board and program device.
7. Compile the c files with the -lpthread and -lz to run the threads and zlib for WAV file compression.

### Usage:
1. run the main.py file first to make sure it listens for the files without corruption.
2. run the output executable file on the puTTY terminal to begin transmission of data.
3. hit CTRL + C on your keyboard to terminate transmission of WAV files manually.






