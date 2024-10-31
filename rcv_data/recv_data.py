import socket

# Define server IP and port (the IP should match the IP of the machine running this Python code)
SERVER_IP = '10.4.49.184'  # Update this to your machine's IP address
PORT = 49152
BUFFER_SIZE = 1024  # Size of each data packet received

# Define output .wav file name
OUTPUT_FILE = "received_audio.wav"

def receive_audio_data():
    """Function to receive audio data over UDP and save it to a .wav file."""
    # Create a UDP socket
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((SERVER_IP, PORT))
        print(f"Listening on {SERVER_IP}:{PORT} for incoming .wav file data...")

        with open(OUTPUT_FILE, 'wb') as wav_file:
            while True:
                # Receive data in chunks
                data, addr = s.recvfrom(BUFFER_SIZE)
                
                # Check if we received a signal to end the transmission
                if data == b'END':
                    print("Received end of file signal.")
                    break
                
                # Write the received data chunk to the .wav file
                wav_file.write(data)

            print(f"File transfer completed. Audio data saved as {OUTPUT_FILE}")

if __name__ == "__main__":
    receive_audio_data()
