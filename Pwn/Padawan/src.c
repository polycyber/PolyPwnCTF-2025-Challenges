//gcc -o padawan src.c -m32 -no-pie -fno-stack-protector
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <unistd.h>
 
void win(int a, int b) {

    if(a == 1234 && b == 5678){
        printf("You did it, can you feel the Force ?\n");
        system("cat ./flag.txt");
    }
}
 
void lose(void) {
    printf("May the force be with you\n");
}

void func(void){
    char buf[10];
    printf("What is your name young padawan?\n");
    fgets(buf,40,stdin);
}

void init(void){
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

void main(void)
{
    init();
    func();
    lose();
}