// wav_utils.c

#include <sys/stat.h> 
#include <sys/types.h>
#include <dirent.h>

#include "include/share.h"

#define FILENAME_BASE "audio"
#define TMP_DIR "tmp"
#define NUM_FILES_BEFORE_CLEAR 10

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