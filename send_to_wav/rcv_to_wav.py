import socket
import struct

SAMPLE_RATE = 40000
NUM_CHANNELS = 1
BITS_PER_SAMPLE = 24
BYTE_RATE = (SAMPLE_RATE * NUM_CHANNELS * BITS_PER_SAMPLE) // 8

# Create a WAV file header
def write_wav_header(wav_file, data_chunk_size):
    wav_file.write(b'RIFF')
    wav_file.write(struct.pack('<I', 36 + data_chunk_size))  # ChunkSize
    wav_file.write(b'WAVE')

    # fmt subchunk
    wav_file.write(b'fmt ')
    wav_file.write(struct.pack('<IHHIIHH', 16, 1, NUM_CHANNELS, SAMPLE_RATE,
                               BYTE_RATE, NUM_CHANNELS * BITS_PER_SAMPLE // 8, BITS_PER_SAMPLE))

    # data subchunk
    wav_file.write(b'data')
    wav_file.write(struct.pack('<I', data_chunk_size))  # SubChunk2Size

def receive_audio_data():
    # Setup UDP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('192.168.0.149', 2000)
    
    # Send initial message to server
    message = "Requesting audio data"
    client_socket.sendto(message.encode(), server_address)
    
    # Open a WAV file for writing
    with open("audio_output.wav", "wb") as wav_file:
        write_wav_header(wav_file, 0)  # Temporary header with 0 data size, we'll update later
        
        data_received = 0
        counter = 0
        
        while True:
            data, addr = client_socket.recvfrom(2048)  # Receive audio data from server
            if not data:
                break  # Stop if no more data
            
            # Process the 24-bit audio data (here assuming it is received in 32-bit format)
            for i in range(0, len(data), 4):  # Process each 32-bit sample
                sample = struct.unpack('<I', data[i:i+4])[0]
                reversed_sample = reverse_24_bits(sample)
                wav_file.write(struct.pack('<I', reversed_sample & 0xFFFFFF)[:3])  # Write the least significant 24 bits
            
            data_received += len(data)
            counter += 1
            if counter % 175 == 0:
                print(f"Received {counter / 175} seconds of audio")
        
        # Update the WAV header with the correct file size
        wav_file.seek(4)
        wav_file.write(struct.pack('<I', 36 + data_received))
        wav_file.seek(40)
        wav_file.write(struct.pack('<I', data_received))

def reverse_24_bits(word):
    reversed_word = 0
    for _ in range(24):
        reversed_word = (reversed_word << 1) | (word & 1)
        word >>= 1
    return reversed_word

if __name__ == "__main__":
    receive_audio_data()