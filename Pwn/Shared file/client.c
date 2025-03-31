//gcc -s -Wall -O0 -no-pie -o client client.c -fno-stack-protector -static

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <sys/stat.h>
#include <sys/sendfile.h>
#include <fcntl.h>

#define SERVER_PORT 4444
#define BUFFER_SIZE 1024

int connect_server(char *ip_server){
    int sock;
    struct sockaddr_in server_addr;

    sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock == -1) {
        perror("socket");
        exit(EXIT_FAILURE);
    }
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(SERVER_PORT);
    if (inet_pton(AF_INET, ip_server, &server_addr.sin_addr) <= 0) {
        perror("inet_pton");
        close(sock);
        exit(EXIT_FAILURE);
    }
    if (connect(sock, (struct sockaddr*)&server_addr, sizeof(server_addr)) == -1) {
        perror("connect");
        close(sock);
        exit(EXIT_FAILURE);
    }

    return sock;
}

void send_secret(int sock, char *secret_file){
    FILE *fp;
    struct stat st;
    char file_size[6];
    ssize_t len;
    char buffer[BUFFER_SIZE];

    if(stat(secret_file, &st) == -1){
        perror("stat");
        close(sock);
        exit(EXIT_FAILURE);
    }
    if((int)st.st_size >= BUFFER_SIZE){
        printf("File to big, max size is %d", BUFFER_SIZE);
        close(sock);
        exit(EXIT_FAILURE);
    }
    sprintf(file_size, "%d\n", (int)st.st_size);

    len = send(sock, file_size, strlen(file_size), 0);
    if (len < 0)
    {
        fprintf(stderr, "Error on sending file size");
        close(sock);
        exit(EXIT_FAILURE);
    }
    fp = fopen(secret_file, "rb");
    if(fp == NULL){
        perror("fopen");
        close(sock);
        exit(EXIT_FAILURE);
    }
    fread(buffer, sizeof(char), (int)st.st_size, fp);
    buffer[(int)st.st_size] = '\0';
    if (send(sock, buffer, st.st_size, 0) < 0) {
        perror("send");
        close(sock);
        exit(EXIT_FAILURE);
    }

    printf("Secret file send\n");
    fclose(fp);
}

int main(int argc, char **argv){
    int sock;
    if(argc != 3){
        fprintf(stderr, "Usage: %s <ip_server> <secret_file>\n", argv[0]);
        return 1;
    }
    sock = connect_server(argv[1]);
    send_secret(sock, argv[2]);
    close(sock);

    return 0;
}