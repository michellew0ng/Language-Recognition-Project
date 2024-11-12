import socket
import wave
import numpy as np
import time
import zlib

def receive_wav_files():
    server_address = ('192.168.1.1', 49152)
    file_counter = 0

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        client_socket.bind(server_address)
        print("Connected to server.")

        while True:
            filename = f"received_{file_counter}.wav"
            decompressor = zlib.decompressobj(-zlib.MAX_WBITS)
            compressed_data = bytearray()

            with open(filename, 'wb') as wav_file:
                print(f"Receiving {filename}...")

                while True:
                    print("fuck")
                    #time.sleep(0.01)
                    chunk, addr = client_socket.recvfrom(65507)
                    if chunk == b'END':
                        print(f"Finished receiving {filename}.")
                        break
                    compressed_data.extend(chunk[2:])
                    wav_file.write(chunk[2:])

                try:
                    #decompressed_data = zlib.decompress(compressed_data, -zlib.MAX_WBITS)
                    decompressed_data = decompressor.decompress(compressed_data)
                    decompressed_data += decompressor.flush()  # Ensure all remaining data is flushed
                    with open(filename, 'wb') as wav_file:
                        wav_file.write(decompressed_data)
                    print(f"Decompressed and saved {filename}.")
                except zlib.error as e:
                    print(f"Decompression error: {e}")
            
            validate_wav_file(filename)
            file_counter += 1

def validate_wav_file(filename):
    """
    Validate if the received .wav file contains a 440 Hz tone for approximately 5 seconds.
    """
    try:
        print(f"\nValidating '{filename}'...")

        # Step 1: Open the .wav file
        with wave.open(filename, 'rb') as wav_file:
            # Step 2: Extract properties
            channels = wav_file.getnchannels()
            sample_width = wav_file.getsampwidth()
            frame_rate = wav_file.getframerate()
            num_frames = wav_file.getnframes()
            duration = num_frames / frame_rate

            # Step 3: Validate channels
            if channels == 1:
                print("Pass: The file is mono.")
            else:
                print("Fail: The file is not mono.")
                return False

            # Step 4: Validate sample width (expecting 16-bit)
            if sample_width == 2:
                print("Pass: Sample width is 16 bits.")
            else:
                print(f"Fail: Sample width is {sample_width * 8} bits (expected 16 bits).")
                return False

            # Step 5: Validate frame rate (expecting 44100 Hz)
            if frame_rate == 44100:
                print("Pass: Frame rate is 44100 Hz.")
            else:
                print(f"Fail: Frame rate is {frame_rate} Hz (expected 44100 Hz).")
                return False

            # Step 6: Validate duration (expecting approximately 5 seconds)
            if 4.9 <= duration <= 5.1:
                print(f"Pass: Duration is approximately 5 seconds ({duration:.2f} seconds).")
            else:
                print(f"Fail: Duration is {duration:.2f} seconds (expected ~5 seconds).")
                return False

            # Step 7: Read the audio frames and convert to numpy array
            audio_frames = wav_file.readframes(num_frames)
            audio_data = np.frombuffer(audio_frames, dtype=np.int16)

        # Step 8: Perform Fourier Transform to find the dominant frequency
        freqs = np.fft.fftfreq(len(audio_data), d=1/frame_rate)
        fft_spectrum = np.fft.fft(audio_data)
        peak_freq = abs(freqs[np.argmax(np.abs(fft_spectrum))])

        # Step 9: Validate the dominant frequency (expecting 440 Hz)
        if 438 <= peak_freq <= 442:
            print(f"Pass: Dominant frequency is approximately 440 Hz ({peak_freq:.2f} Hz).")
        else:
            print(f"Fail: Dominant frequency is {peak_freq:.2f} Hz (expected ~440 Hz).")
            return False

        # If all checks passed
        print("All tests passed. The .wav file is valid.")
        return True

    except Exception as e:
        print(f"Error validating WAV file: {e}")
        return False
    
# Start receiving WAV files
receive_wav_files()

