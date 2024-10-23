# LED Control using Language Recognition

COMP3601 Project 24T3. Implementing voice recognition to control an LED. 
Developed by Michelle Wong, Hasitha Peter, and Max Jaroenkitphan

## Milestone 4 

![image](https://github.com/user-attachments/assets/19ea688e-7bc7-4cf1-9c4e-92b774c0bfa3)

Milestone 4 implements a simple I2S MEMS microphone -> Kria board -> WAV file output. 

### Hardware:
1. Kria KV260 FPGA
2. ADAFruit i2s MEMs Microphone
3. Ethernet cable

### Software:
1. Xilinx Vivado 2021.2
2. Whisper API
3. ChatGPT 4.0

### Progress Checkpoints:
Milestone 3: We were able to capture audio samples by setting up the i2s.master and the fifo.vhd.

Milestone 4: We are currently converting the captured audio samples into a .wav file. The code for this is under the app/src/main.c file.

### Instructions 
1. Connect an ethernet cable running between your Kira board and the PC.
2. ifconfig 192.168.1.2 netmask 255.255.255.0 to set an ip address for your kriaboard
3. Turn off firewall for your pc.
4. ping the kria ip address to check for connectivity between your pc terminal and kria board.
5. send the src and main files to board using pscp command
6. Compile code for the board and program device.
7. Compile c files on board and run
8. Transfer the .wav file back to pc using pscp command and play it back.


## Milestone 5

Milestone 5 implements realtime data streaming through the microphone over Ethernet to be processed by a 
