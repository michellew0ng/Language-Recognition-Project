#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>

#define PORT 54321
#define MEMORY_MAPPED_ADDR 0xA0020000

int main() {
    int server_fd, new_socket;
    struct sockaddr_in address;
    int opt = 1;
    int addrlen = sizeof(address);
    char buffer[1024] = {0};
    
    // Pointer to the memory-mapped address
    volatile unsigned int *vhdl_signal = (unsigned int *)MEMORY_MAPPED_ADDR;

    // Create socket
    server_fd = socket(AF_INET, SOCK_STREAM, 0);
    setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT, &opt, sizeof(opt));
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(PORT);
    bind(server_fd, (struct sockaddr *)&address, sizeof(address));
    listen(server_fd, 3);

    printf("Waiting for connection on port %d...\n", PORT);
    new_socket = accept(server_fd, (struct sockaddr *)&address, (socklen_t*)&addrlen);

    // Read command from client
    int valread = read(new_socket, buffer, 1024);
    buffer[valread] = '\0';

    // Parse the command and write to memory-mapped address
    if (strcmp(buffer, "T") == 0) {
        *vhdl_signal = 1;  // Turn LED ON
    } else if (strcmp(buffer, "F") == 0) {
        *vhdl_signal = 0;  // Turn LED OFF
    } else if (buffer[0] == 'B' && strlen(buffer) > 1) {
        int brightness = atoi(buffer + 1);
        if (brightness >= 1 && brightness <= 255) {
            *vhdl_signal = brightness;  // Set brightness
        }
    } else {
        printf("Invalid command received: %s\n", buffer);
    }

    // Close sockets
    close(new_socket);
    close(server_fd);

    return 0;
}

