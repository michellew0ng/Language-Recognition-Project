#include <pthread.h>
#include <stdio.h>
 

// Declarations of external functions
int process_signal();
int send_wav();

void* thread1_func(void* arg) {
    process_signal();
    return NULL;
}

void* thread2_func(void* arg) {
    send_wav();
    return NULL;
}

int main() {
    pthread_t thread1, thread2;

    // Create threads
    pthread_create(&thread1, NULL, thread1_func, NULL);
    pthread_create(&thread2, NULL, thread2_func, NULL);

    // Wait for threads to complete
    pthread_join(thread1, NULL);
    pthread_join(thread2, NULL);

    printf("Threads have completed.\n");
    return 0;
}