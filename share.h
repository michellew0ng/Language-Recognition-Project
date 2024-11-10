// shared.h
#ifndef SHARED_H
#define SHARED_H

#include <stdint.h>

extern uint32_t recorded_data[];  // Declare it as an extern variable

void create_tmp(void);
void clear_tmp_directory(void);
void remove_tmp_directory(void);
void create_filename(char *buffer);
void write_little_endian(uint32_t word, int num_bytes, FILE *wav_file);
void write_backward_24(uint32_t word, FILE *wav_file);
void write_wav(unsigned long num_samples, uint32_t *data);
int main_m5_task(void);

#endif
