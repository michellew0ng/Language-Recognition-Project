#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>

#define PORT 54321

int process_signal() {
    int server_fd, new_socket;
    struct sockaddr_in address;
    int opt = 1;
    int addrlen = sizeof(address);
    char buffer[1024] = {0};
    volatile unsigned int *vhdl_signal = (unsigned int *)0xA0020000; // Replace with appropriate memory-mapped address

    // Create socket file descriptor
    if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0) {
        perror("Socket failed");
        exit(EXIT_FAILURE);
    }

    // Forcefully attaching socket to the port
    if (setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT, &opt, sizeof(opt))) {
        perror("setsockopt");
        close(server_fd);
        exit(EXIT_FAILURE);
    }

    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(PORT);

    // Bind the socket
    if (bind(server_fd, (struct sockaddr *)&address, sizeof(address)) < 0) {
        perror("Bind failed");
        close(server_fd);
        exit(EXIT_FAILURE);
    }

    // Listen for incoming connections
    if (listen(server_fd, 3) < 0) {
        perror("Listen failed");
        close(server_fd);
        exit(EXIT_FAILURE);
    }

    printf("Waiting for a connection on port %d...\n", PORT);

    // Accept an incoming connection
    if ((new_socket = accept(server_fd, (struct sockaddr *)&address, (socklen_t*)&addrlen)) < 0) {
        perror("Accept failed");
        close(server_fd);
        exit(EXIT_FAILURE);
    }

    // Read data from the client
    int valread = read(new_socket, buffer, 1024);
    printf("Received data: %s\n", buffer);

    // Check the signal received and send it to the VHDL module
    if (strstr(buffer, "T") != NULL) {
        *vhdl_signal = 1;  // Send signal to turn on
        printf("VHDL signal set to TURN ON\n");
    } else if (strstr(buffer, "F") != NULL) {
        *vhdl_signal = 0;  // Send signal to turn off
        printf("VHDL signal set to TURN OFF\n");
    } else {
        printf("Unknown command\n");
    }

    // Close the sockets
    close(new_socket);
    close(server_fd);

    return 0;
}
