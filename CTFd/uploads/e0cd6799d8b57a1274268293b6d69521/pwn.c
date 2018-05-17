#include <stdio.h>
int main(int argc, char** argv)
{
    int modified;
    char buffer[10];
    modified = 0;
    printf("Please fill the buffer:\n");
    fflush(stdout);
    gets(buffer);
    if (modified != 0)
    {
        printf("Congratulations, you got the shell.\n");
        printf("Remember you can only read your own team's flag!\n");
        fflush(stdout);
        system("/bin/sh");
        exit(0);
    }
    else
    {
        printf("Please try again.\n");
    }
    return 0;
}
