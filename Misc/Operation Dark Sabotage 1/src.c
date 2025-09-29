#include <stdlib.h>
#include <sys/types.h>
#include <unistd.h>
#include <stdio.h>

int main(int argc, char **argv)
{
    char command[100];
    if (argc < 2)
    {
        printf("Usage: %s <path>\n", argv[0]);
        exit(0);
    }

    snprintf(command, sizeof(command),"find -L %s", argv[1]);
    setreuid(geteuid(), geteuid());
    system(command); 
}