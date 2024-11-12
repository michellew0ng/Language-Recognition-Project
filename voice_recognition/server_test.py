import wave
import numpy as np
import socket
import time

def create_wav_file(filename, duration=5, sample_rate=44100):
    """
    Generate a 5-second mono sine wave at 440Hz (A4).
    """
    frequency = 440.0
    amplitude = 0.5
    n_samples = duration * sample_rate
    t = np.linspace(0, duration, int(n_samples), False)
    audio_data = (amplitude * np.sin(2 * np.pi * frequency * t)).astype(np.float32)

    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 2 bytes per sample (16-bit PCM)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes((audio_data * 32767).astype(np.int16).tobytes())

def send_wav_files_continuously():
    server_address = ('localhost', 6000)
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
        server_socket.bind(server_address)
        server_socket.listen(1)
        print(f"Server is listening on {server_address}...")

        client_socket, client_address = server_socket.accept()
        with client_socket:
            print(f"Connection established with {client_address}")

            file_counter = 0
            while True:
                # Generate a new WAV file with a unique name
                filename = f"test_{file_counter}.wav"
                create_wav_file(filename)

                # Open the WAV file and send it over the socket
                with open(filename, 'rb') as wav_file:
                    print(f"Sending {filename}...")
                    while True:
                        chunk = wav_file.read(1024)
                        if not chunk:
                            break
                        client_socket.sendall(chunk)

                # Send the 'END' signal to indicate completion
                client_socket.sendall(b'END')
                print(f"{filename} sent successfully. 'END' sent.")

                file_counter += 1
                time.sleep(1)  # Wait 1 second before sending the next file

# Start the continuous WAV file generation and transmission
send_wav_files_continuously()