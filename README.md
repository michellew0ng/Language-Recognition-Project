# LED Control using Language Recognition

COMP3601 Project 24T3. Implementing voice recognition to control an LED. 
Developed by Michelle Wong, Hasitha Peter, and Max Jaroenkitphan

![462536604_546912724753282_2631495542290620869_n](https://github.com/user-attachments/assets/dfdc54bb-c350-4450-8c1d-1fa393f99e07)


### Hardware:
1. Kria KV260 FPGA
2. ADAFruit i2s MEMs Microphone
3. Ethernet Cable
   
### Software:
1. Xilinx Vivado 2021.2
2. Whisper API
3. ChatGPT 4.0


## Progress Checkpoint
Milestone 3: We were able to capture audio signals by setting up the i2s_master.vhd and the fifo.vhd
Milestone 4: We are currently converting the captured audio samples into a .wav file. The code for this is under the src/main.c file.

## Instructions 
1. Connect an ethernet cable running between your Kira board and the PC.
2. ifconfig 192.168.1.2 netmask 255.255.255.0 to set an ip address for your kriaboard
3. Turn off firewall for your pc.
4. ping the kria ip address to check for connectivity between your pc terminal and kria board.
5. send the src and main files to board using pscp command
6. Compile code for the board and program device.
7. Compile c files on board and run
8. Transfer the .wav file back to pc using pscp command and play it back.

## Future Integration
For Milestone 5, we plan to integrate the current system with the python client that has been set up by opening up a socket to allow for bidirectional communication between the i2s driver and the client, and by proxy the kria board to facilitate the complete process of controlling the LED's on and off state.

### Reference for .wav file format: 
https://ccrma.stanford.edu/courses/422-winter-2014/projects/WaveFormat/#:~:text=A%20WAVE%20file%20is%20often,form%20the%20%22Canonical%20form%22.

