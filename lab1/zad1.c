#include <string.h>
#include <unistd.h>
#include <pthread.h>
#include <malloc.h>
#include <stdlib.h>
#include <sys/shm.h>
#include <sys/ipc.h>
#include <sys/wait.h>

void carousselProcess() {

}

void visitorProcess() {

}

int main(int argc, char *argv[]) {

    int processId;
    printf("\n\tCreating caroussel process...\n");

    switch (processId = fork()) {
            case -1:
                printf("\t\nUnable to create new process!\n");
                exit(1);
                
            case 0:
                carousselProcess();
                exit(0);
            
            default:
                break;
    }

    for(int i = 0; i < 8; i++) {
        switch (processId = fork()) {
            case -1:
                printf("\t\nUnable to create new process!\n");
                exit(1);
                
            case 0:
                printf("\n\tCreated %d. visitor process!\n", i+1);
                visitorProcess();
                exit(0);
            
            default:
                break;
        }
    }

    return 0;
}