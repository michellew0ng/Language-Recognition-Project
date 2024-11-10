/** 24T3 COMP3601 Design Project A
 * File name: main.c
 * Description: Example main file for using the audio_i2s driver for your Zynq audio driver.
 *
 * Distributed under the MIT license.
 * Copyright (c) 2022 Elton Shih
 * Permission is hereby granted, free of charge, to any person obtaining a copy of
 * this software and associated documentation files (the "Software"), to deal in
 * the Software without restriction, including without limitation the rights to
 * use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
 * of the Software, and to permit persons to whom the Software is furnished to do
 * so, subject to the following conditions:
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <dirent.h>
#include <stdint.h>
#include <time.h>

#include "audio_i2s.h"

#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>

#include <sys/stat.h> 
#include <sys/types.h>

#define TRANSFER_RUNS 10

#define NUM_CHANNELS 2
#define BPS 24
#define SAMPLE_RATE 44100
#define RECORD_DURATION 25

#define MASK(n) (1 << n) - 1


#define FILENAME_BASE "audio"
#define TMP_DIR "tmp"
#define NUM_FILES_BEFORE_CLEAR 10

/* Buffer that stores 44100 samples per second for RECORD_DURATION number of seconds*/
uint32_t recorded_data[SAMPLE_RATE * RECORD_DURATION * NUM_CHANNELS] = {0};

/**
 * @brief
 *      Handles creating a tmp directory for all the wav samples
 */
void create_tmp(void){
    struct stat st = {0};
    if (stat("tmp", &st) == -1) {
        mkdir(TMP_DIR, 0777);
    } else {
        perror("Couldn't properly create tmp\n");
    }
}

/**
 * @brief
 *      Clears all the files in the tmp directory
 */
void clear_tmp_directory(void) {
    DIR *dir;
    struct dirent *entry;
    char filepath[256];

    dir = opendir(TMP_DIR);
    if (dir == NULL) {
        perror("Unable to open tmp directory");
        return;
    }

    while ((entry = readdir(dir)) != NULL) {
        // Skip `.` and `..` entries
        if (strcmp(entry->d_name, ".") == 0 || strcmp(entry->d_name, "..") == 0) {
            continue;
        }
        // Build the full file path
        snprintf(filepath, sizeof(filepath), "%s/%s", TMP_DIR, entry->d_name);
        remove(filepath);
    }
    closedir(dir);
}

/**
 * @brief
 *      Removes the tmp directory from the system.
 */
void remove_tmp_directory() {
    // Delete the tmp directory itself
    if (rmdir(TMP_DIR) == 0) {
        printf("Deleted directory: %s\n", TMP_DIR);
    } else {
        perror("Error deleting directory");
    }
}

/**
 * @brief 
 *      Creates a unique filename based on the current timestamp.
 * @param buffer The buffer that holds the new filename
 */
void create_filename(char *buffer) {
    snprintf(buffer, sizeof(buffer), "%s/%s_%lu.wav", TMP_DIR, FILENAME_BASE, time(NULL));
}

/*
    Writes bytes into a file in little endian format
*/
void write_little_endian(uint32_t word, int num_bytes, FILE *wav_file)
{
    unsigned buf;
    while(num_bytes>0) {
        buf = word & 0xff; // extract the least significant byte from the word
        fwrite(&buf, 1,1, wav_file);
        num_bytes--;
        word >>= 8; // move the next least significant byte down to the least significant bytes position
    }
}

/**
 * @brief
 *      this function reversed the given 32 bits number for 24 times (reverse and save the last 24 bits)
 *      and store the reversed number into the give file when the number is not 0
 *      we ignore 0 at here to avoid electronic noise
 * @param word the 32 bits sample we get from the i2s
 * @param wav_file the output wavefile we want to create
 */
void write_backward_24(uint32_t word, FILE *wav_file) {
    uint32_t real = 0;
    uint32_t temp = 0;
    for(int i = 0; i < 24; i++) {
        real = real << 1;
        temp = word & 1; // the LSB of the word
        real = real + temp;
        word = word >> 1;
    }
    if (real != 0) {
        fwrite(&real, 3, 1, wav_file);
    }
}


/*
    Writes the header and the data to a wav file.
*/
void write_wav(unsigned long num_samples, uint32_t *data)
{
    // Audio information
    unsigned int sample_rate = SAMPLE_RATE;
    unsigned int num_channels = NUM_CHANNELS;
    unsigned int bits_per_sample = BPS;

    // Wav file information
    unsigned int byte_rate = (sample_rate * num_channels * bits_per_sample) / 8;
    unsigned int chunk_size = 36 + (bits_per_sample / 8) * num_samples * num_channels;
    unsigned int sub_chunk_1 = 16;
    unsigned int sub_chunk_2 = (bits_per_sample / 8) * num_samples * num_channels;

    // Open file and write header -- https://ccrma.stanford.edu/courses/422-winter-2014/projects/WaveFormat/#:~:text=A%20WAVE%20file%20is%20often,form%20the%20%22Canonical%20form%22.
    char filename[100];
    create_filename(filename);
    
    FILE* wav_file = fopen(filename, "wb");

    // RIFF header
    fwrite("RIFF", 1, 4, wav_file); // ChunkID
    write_little_endian(chunk_size, 4, wav_file); // ChunkSize
    fwrite("WAVE", 1, 4, wav_file); // Format

    // fmt subchunk
    fwrite("fmt ", 1, 4, wav_file); // SubChunk1ID
    write_little_endian(sub_chunk_1, 4, wav_file); // SubChunk1Size
    write_little_endian(1, 2, wav_file); // PCM = 1
    write_little_endian(num_channels, 2, wav_file); // NumChannels
    write_little_endian(sample_rate, 4, wav_file); // SampleRate
    write_little_endian(byte_rate, 4, wav_file); // ByteRate (SampleRate * NumChannels * BitsPerSample) / 8
    write_little_endian(num_channels * bits_per_sample / 8, 2, wav_file); // BlockAlign
    write_little_endian(bits_per_sample, 2, wav_file); // BitsPerSample

    // data subchunk
    fwrite("data", 1, 4, wav_file); // SubChunk2ID
    write_little_endian(sub_chunk_2, 4, wav_file); // SubChunk2Size
    for (unsigned long i = 0; i < num_samples; i++) {
        write_backward_24((unsigned int) data[i], wav_file); // write the data
    }

    fclose(wav_file);
}

int main() {

    audio_i2s_t my_config;
    if (audio_i2s_init(&my_config) < 0) {
        printf("Error initializing audio_i2s\n");
        return -1;
    }

    // initialize
    printf("mmapped address: %p\n", my_config.v_baseaddr);
    printf("Before writing to CR: %08x\n", audio_i2s_get_reg(&my_config, AUDIO_I2S_CR));
    audio_i2s_set_reg(&my_config, AUDIO_I2S_CR, 0x1);
    printf("After writing to CR: %08x\n", audio_i2s_get_reg(&my_config, AUDIO_I2S_CR));
    printf("SR: %08x\n", audio_i2s_get_reg(&my_config, AUDIO_I2S_SR));
    printf("Key: %08x\n", audio_i2s_get_reg(&my_config, AUDIO_I2S_KEY));
    printf("Before writing to gain: %08x\n", audio_i2s_get_reg(&my_config, AUDIO_I2S_GAIN));
    audio_i2s_set_reg(&my_config, AUDIO_I2S_GAIN, 0x1);
    printf("After writing to gain: %08x\n", audio_i2s_get_reg(&my_config, AUDIO_I2S_GAIN));
    printf("Initialized audio_i2s\n");

    unsigned long sampleNum = 0;

    printf("Starting audio_i2s_recv\n");
    create_tmp();

    // calculate how many frames(blocks) we need from the i2s
    // we get data from the i2s with 2 channels but we only need 1 in the wave file
    // meanwhile, for each channel, the last 2 samples each frame are useless, so we need to ignore them ass well.
    int sampleCounter = SAMPLE_RATE * RECORD_DURATION * 2 / (TRANSFER_LEN - 4);

    for (int i = 0; i < sampleCounter; i++) {
        int32_t *samples = audio_i2s_recv(&my_config);
        printf("i2s counter: %d\n", i); // use printf to slow down the loop, so that the i2s buffer can refill
        for (int j = 0; j < TRANSFER_LEN - 4; j++) {
            // record both channels 
            if (j % 2 == 0) {
                recorded_data[sampleNum + j] = samples[j];
            }
        }
        sampleNum += TRANSFER_LEN - 4;
    }

    printf("Start convert to wav file\n");

    int audio_count = 0;
    while (1) {
        // Clear audio count every 10 samples to keep tmp folder clean
        if (audio_count == NUM_FILES_BEFORE_CLEAR) {
            audio_count = 0;
            clear_tmp_directory();
        }
        write_wav(RECORD_DURATION * SAMPLE_RATE, recorded_data);
        audio_i2s_release(&my_config);
        printf("File written\n");
        audio_count++;

    }

    clear_tmp_directory();
    remove_tmp_directory();

    return 0;
}

