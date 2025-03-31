//ar x libc.a system.o
//gcc -Wall -O0 -no-pie -o server server.c -fno-stack-protector -static system.o gadget.s

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>

#define PORT 4444
#define BUFFER_SIZE 1024

int init_server(int port) {
    int server_fd;
    struct sockaddr_in address;
    int opt = 1;

    if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == -1) {
        perror("socket");
        exit(EXIT_FAILURE);
    }
    
    if (setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt)) < 0) {
        perror("setsockopt");
        close(server_fd);
        exit(EXIT_FAILURE);
    }

    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(port);

    if (bind(server_fd, (struct sockaddr *)&address, sizeof(address)) < 0) {
        perror("bind");
        close(server_fd);
        exit(EXIT_FAILURE);
    }

    if (listen(server_fd, 5) < 0) {
        perror("listen");
        close(server_fd);
        exit(EXIT_FAILURE);
    }
    return server_fd;
}

int accept_client(int server_fd){
    int client_socket;
    struct sockaddr_in client_address;
    socklen_t client_addr_len = sizeof(client_address);

    printf("Waiting for a jedi...\n");
    if ((client_socket = accept(server_fd, (struct sockaddr *)&client_address, &client_addr_len)) < 0) {
        perror("accept");
        close(server_fd);
        exit(EXIT_FAILURE);
    }
    dup2(client_socket, 0);
    dup2(client_socket, 1);
    dup2(client_socket, 2);

    return client_socket;
}

int get_data_size(int client_socket){
    char buffer[BUFFER_SIZE] = {0};
    char byte;
    int bytes_read = 0;

    while(read(client_socket, &byte, 1) > 0){
        if(byte == '\n'){
            break;
        }
        buffer[bytes_read++] = byte;
        if (bytes_read >= BUFFER_SIZE - 1){
            return 0;
        }
    }
    if(bytes_read > 0){
        buffer[bytes_read] = '\0';
    }
    return atoi(buffer);
}

void get_data(int client_socket, int size_data){
    char byte;
    char buffer[BUFFER_SIZE] = {0};
    int bytes_read = 0;
    FILE *fp;

    while(read(client_socket, &byte, 1) > 0){
        if(bytes_read == size_data) break;
        buffer[bytes_read++] = byte;
    }
    if(bytes_read > 0){
        buffer[bytes_read] = '\0';
        fp = fopen("./secret.txt", "w");
        fprintf(fp, "%s", buffer);
        fclose(fp);
    }
}

void handle_con(int client_socket){
    int size_file = get_data_size(client_socket);
    get_data(client_socket, size_file);
    close(client_socket);
}

int main(int argc, char **argv){
    int server_fd,client_socket;
    server_fd = init_server(PORT);
    client_socket = accept_client(server_fd);
    handle_con(client_socket);
    close(server_fd);

    return 0;
}