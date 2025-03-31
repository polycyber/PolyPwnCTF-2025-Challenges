//gcc -Wall -o jedi jedi.c -fno-stack-protector
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

void init(void){
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

int main(int argc, char **argv){
    int is_jedi = 0;
    char answer[10];

    init();
    printf("Are you a jedi?\n>>> ");
    fgets(answer,20,stdin);

    if(is_jedi == 0xdeadbeef){
        printf("Hello jedi, this is your secret message\n");
        system("cat flag.txt");
    }else {
        printf("Liar, you are a sith!!\n");
    }

    return 0;
}