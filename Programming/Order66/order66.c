#include <sys/ptrace.h>
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <err.h>
#include <sys/user.h>
#include <sys/wait.h>
#include <signal.h>
#include <string.h>
#include <sys/mman.h>
#include <time.h>
#include <stdint.h>

#define __NR_exit 60
#define __NR_open 2
#define __NR_close 3
#define __NR_read 0
#define __NR_write 1
#define __NR_access 21
#define __NR_sigaction 13

#define SHELLCODE_SIZE 128
#define NUMBER_EGG 2
#define MMAPSIZE 65536

static int order66[NUMBER_EGG] = {0x6564726f, 0x00363672};

static const char hidden_payload[] = { 
    0x48,0x31,0xc0,0xb8,0x0a,0x00,0x00,0x00,0x50,0x48,
    0xb8,0x72,0x64,0x65,0x72,0x20,0x36,0x36,0x3a,0x50,
    0x48,0xb8,0x6e,0x64,0x20,0x74,0x68,0x65,0x20,0x6f,
    0x50,0x48,0xb8,0x2c,0x20,0x79,0x6f,0x75,0x20,0x66,
    0x69,0x50,0x48,0xb8,0x43,0x6f,0x6e,0x67,0x72,0x61,
    0x74,0x65,0x50,0xb8,0x01,0x00,0x00,0x00,0xbf,0x01,
    0x00,0x00,0x00,0x48,0x89,0xe6,0xba,0x21,0x00,0x00,
    0x00,0x0f,0x05,0x48,0x31,0xc0,0x50,0x48,0xb8,0x66,
    0x6c,0x61,0x67,0x2e,0x74,0x78,0x74,0x50,0x48,0x89,
    0xe7,0x48,0x31,0xc0,0xb8,0x02,0x00,0x00,0x00,0x48,
    0x31,0xf6,0x0f,0x05,0x48,0x89,0xc7,0xb8,0x00,0x00,
    0x00,0x00,0x48,0x89,0xe6,0xba,0x20,0x00,0x00,0x00,
    0x0f,0x05,0xb8,0x01,0x00,0x00,0x00,0xbf,0x01,0x00,
    0x00,0x00,0x48,0x89,0xe6,0x0f,0x05,0xb8,0x3c,0x00,
    0x00,0x00,0x48,0x31,0xff,0x0f,0x05
};

static void * hidden_shellcode;

typedef struct{
    int syscall;
    void (*callback)(pid_t child, struct user_regs_struct *regs);
} syscall_handler;

static void kill_child_process(pid_t pid) {

    kill(pid, SIGKILL);
    wait(NULL);
    exit(EXIT_FAILURE);
}

static void handle_sys_open(pid_t pid, struct user_regs_struct *regs){

    uintptr_t offset = (uintptr_t)regs->rip - (uintptr_t)hidden_shellcode;
    if (offset >= (uintptr_t)sizeof(hidden_payload)){
        printf("Follow the order, that's not the chosen one\n");
        kill_child_process(pid);
    }
}

static syscall_handler syscalls_handlers[] = {
    {__NR_exit,           NULL},
    {__NR_open,           handle_sys_open},
    {__NR_close,          NULL},
    {__NR_read,           NULL},
    {__NR_write,          NULL},
    {__NR_access,         NULL},
    {__NR_sigaction,      NULL},
};

static void hide_egg(void) {
    int max_offset;
    int offset;
    hidden_shellcode = mmap(NULL, MMAPSIZE, PROT_READ | PROT_WRITE | PROT_EXEC,
                    MAP_SHARED | MAP_ANONYMOUS, -1, 0);
    if (hidden_shellcode == MAP_FAILED) {
        perror("mmap");
        exit(EXIT_FAILURE);
    }
    long hint = (long)hidden_shellcode;
    srand(time(NULL));
    max_offset = MMAPSIZE - sizeof(hidden_payload) - sizeof(int);
    max_offset -= max_offset % 4;
    offset = rand() % max_offset;
    offset -= offset % 4;
    for(int i=0; i < NUMBER_EGG; i++){
        *(int *)((char *)hidden_shellcode + offset) = order66[i];
        offset += 4;
    }
    hidden_shellcode += offset;
    printf("[Hint] %lx\n",hint & 0xFFFFFFF00000);
    memcpy((char *)hidden_shellcode, hidden_payload, sizeof(hidden_payload));
}

static void handle_syscall_child(pid_t child_pid) {
    int i;
    struct user_regs_struct regs;

    if(ptrace(PTRACE_GETREGS, child_pid, NULL, &regs) < 0){
        perror("PTRACE_GETREGS");
        exit(EXIT_FAILURE);
    }

    for(i = 0; i < sizeof(syscalls_handlers)/sizeof(*syscalls_handlers); i++) {
        if(regs.orig_rax == syscalls_handlers[i].syscall) {
            if(syscalls_handlers[i].callback != NULL){
                syscalls_handlers[i].callback(child_pid, &regs);
            }
            return;
        }
    }
    if((long long int)regs.orig_rax < 0) {
        printf("Segfault! The Empire does not allow failure!\n");
    } else {
        printf("(%llu) instruction is not in the order, You have disappointed the Empire!\n", regs.orig_rax);
    }
    kill_child_process(child_pid);
}

static void start_finder(void) {
    char shellcode[SHELLCODE_SIZE];
    char texte[] = "find the Order 66 !\n";

    write(1, texte, sizeof(texte) - 1);
    read(0, shellcode, SHELLCODE_SIZE);
    ((void (*) (void)) shellcode) ();
}

static pid_t init_tracee_child(void) {
    pid_t pid = fork();
    if(pid == -1){
        perror("fork");
        exit(EXIT_FAILURE);
    }
    if(pid == 0) {
        if(ptrace(PTRACE_TRACEME, 0, NULL, NULL) < 0){
            perror("PTRACE_TRACEME");
            exit(EXIT_FAILURE);
        }
        hidden_shellcode = 0x0;
        raise(SIGCONT);
        start_finder();
    } else {
        wait(NULL);
    }
    return pid;
}

static void tracee_child(pid_t child_pid){
    int status;
    if(ptrace(PTRACE_SYSCALL, child_pid, NULL, NULL) < 0){
        perror("PTRACE_SYSCALL");
        exit(EXIT_FAILURE);
    }
    wait(&status);
    if(WIFEXITED(status)){
        exit(EXIT_SUCCESS);
    }
    handle_syscall_child(child_pid);
}

int main (int argc, char * argv[]) {
    hide_egg();
    pid_t child_pid = init_tracee_child();
    if(child_pid > 0) {
        for(;;) {
            tracee_child(child_pid);
        }
    }
}