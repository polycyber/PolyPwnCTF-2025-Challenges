#include <stdio.h>
#include <stdlib.h>
#include <sys/ptrace.h>
#include <string.h>


static int test_password(char *input){
    char *a = "5/7_-j>PDepdy{V=1R8(aON,IH`W2+!.#Qb6ch&A4oSMkxzn<)tEZlUis:KrTfFmGJX~Cq9v}^Y?|*g;w3uL@$0'B";
    int b[35] ={10, 41, 53, 12, 36, 12, 34, 9, 59, 13, 63, 12, 3, 56, 81, 36, 59, 81, 50, 3, 59, 81, 34, 81, 53, 3, 10, 84, 56, 56, 80, 86, 59, 11, 72};
    
    size_t c = sizeof(b) / sizeof(b[0]);
    if(strlen(input) != c) return 1;
    for(int i =0; i < c ; i++){
        if(input[i] != a[b[i]]) return 1;
    }
    return 0;
    
}

int main(int argc, char **argv){
    if(argc != 2){
        exit(EXIT_FAILURE);
    }
    if (ptrace(PTRACE_TRACEME, 0, NULL, NULL) == -1) {
        printf("You will never get my passwor sith !\n");
        exit(EXIT_FAILURE);
    }
    if(test_password(argv[1])){
        printf("Are you a sith?\n");
        return 1;
    }else{
        printf("Dont share my secret password\n");
    }
    return 0;
}


