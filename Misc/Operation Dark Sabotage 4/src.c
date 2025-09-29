#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/stat.h>

void get_size(char *file_name){
    struct stat st;

    stat(file_name, &st);
    printf("File size: %ld\n", st.st_size);
}

void get_permission(char * file_name){
    struct stat st;

    stat(file_name, &st);
    printf("File permission: %o\n", st.st_mode & 0777);
}

void get_content(char *file_name){
    FILE *fp;
    char ch;

    fp = fopen(file_name, "r");
    while((ch = fgetc(fp)) != EOF)
    {
        printf("%c", ch);
    } 
    fclose(fp);
}


int main(int argc, char **argv)
{
    int choice = 0;

    if(argc != 2) {
        fprintf(stderr, "Usage: %s <file>\n", argv[0]);
        return 1;
    }

    if (!access(argv[1], W_OK))
    {
        printf("Choice: \n"
                "\t[1] Display file size\n"
                "\t[2] Display file permission\n"
                "\t[3] Display file content\n"
                " -> ");
        scanf("%d", &choice);
        switch (choice)
        {
            case 1:
                get_size(argv[1]);
                break;
            case 2:
                get_permission(argv[1]);
                break;
            case 3:
                get_content(argv[1]);
                break;
            default:
                break;
        }
        return 0;
    }
    else
    {
        fprintf(stderr,"%s: %s: Permission denied\n", argv[0], argv[1]);
        return 1;
    }
}
