#include <stdio.h>
#include <string.h>
#include <stdbool.h>
#include <unistd.h>
#include <pthread.h>
#include <malloc.h>
#include <stdlib.h>
#include <sys/ipc.h>
#include <sys/wait.h>
#include <sys/msg.h>
#include <time.h>

int generateRandomNum(int lower, int upper);
void carousselProcess();
void visitorProcess();

struct msgbuffer {
    long mtype;
    char mtext[200];
};

struct tokenBuffer {
    long mtype;
    bool token;
};

int main(int argc, char *argv[]) {

    int processId, num[8];
    
    srand(time(NULL));
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


    printf("\n\tCreating visitors processes...\n\n");
    //for(int i = 0; i < 8; i++) {
        //num[i] = i;
        switch (processId = fork()) {
            case -1:
                printf("\t\nUnable to create new process!\n");
                exit(1);
                
            case 0:
                visitorProcess(2);
                exit(0);
            
            default:
                break;
        }
    //}

    return 0;
}

void carousselProcess() {

    int visitorsRemaining = 8, msqid, visitorCounter = 0, *visitorIds;
    struct msgbuffer carousselBuffer;
    key_t key = getuid();

    char visitorMsg[] = "I wanna ride!";
    char visitorEndMsg[] = "Visitor is done riding!";
    
    char carousselMsg[] = "Sit down!";
    char carousselEndMsg[] = "Get up!";
    
    if ((msqid = msgget(key, 0600 | IPC_CREAT)) == -1) {
        perror("msgget");
        exit(1);
    }

    while(visitorsRemaining != 0) {

        if (msgrcv(msqid, (struct msgbuffer *)&carousselBuffer, sizeof(carousselBuffer)-sizeof(long), 0, 0) == -1) {
            perror("msgrcv");
            exit(1);
        }

        printf("\n\tReceived message in caroussel ===> %s\n", carousselBuffer.mtext);

/*
        if(strncmp(carousselBuffer.mtext, visitorEndMsg, 7) == 0) {
            visitorsRemaining--;
        }
*/
        if(strcmp(visitorMsg, carousselBuffer.mtext) == 0) {
            printf("Visitor counter => %d\n", visitorCounter);
            // Increase counter till value is 4
            visitorIds[visitorCounter] = carousselBuffer.mtype;
            visitorCounter++;

            // Reply with message "Sit down!"
            memcpy(carousselBuffer.mtext, carousselMsg, strlen(carousselMsg)+1);
            carousselBuffer.mtype = 1;
            if(msgsnd(msqid, (struct msgbuffer *)&carousselBuffer, strlen(carousselMsg) + 1, 0) == -1) perror("msgsnd");

            if(visitorCounter == 4) {
                
                printf("\n\t\tCaroussel active!\n");
                sleep(generateRandomNum(1000, 3000));
                printf("\n\t\tCaroussel done riding!\n");
                visitorCounter = 0;
                
                // Reply to each visitor to get up
                for(int i = 0; i < 4; i++) {
                    memcpy(carousselBuffer.mtext, carousselEndMsg, strlen(carousselEndMsg)+1);
                    carousselBuffer.mtype = visitorIds[i];
                    if(msgsnd(msqid, (struct msgbuffer *)&carousselBuffer, strlen(carousselEndMsg) + 1, 0) == -1) perror("msgsnd");
                }
            }
        }


    }

    msgctl(msqid, IPC_RMID, NULL);

}

void visitorProcess(int num) {

    int visitorId = num, msqid, tokenid;
    struct msgbuffer visitorBuffer;
    key_t key = getuid();
    key_t token_key = getuid() + 1;

    char visitorMsg[] = "I wanna ride!";
    char visitorEndMsg[] = "Visitor is done riding!";

    char carousselMsg[] = "Sit down!";
    char carousselEndMsg[] = "Get up!";

    if ((msqid = msgget(key, 0600 | IPC_CREAT)) == -1) {
        perror("msgget");
        exit(1);
    }

    if ((tokenid = msgget(token_key, 0600 | IPC_CREAT)) == -1) {
        perror("msgget");
        exit(1);
    }

    for(int i = 0; i < 3; i++) {
        printf("Sending message...\n");
        sleep(generateRandomNum(100, 2000));
        // Add request to sit on caroussel in message queue
        memcpy(visitorBuffer.mtext, visitorMsg, strlen(visitorMsg)+1);
        visitorBuffer.mtype = visitorId;
        if (msgsnd(msqid, (struct msgbuffer *)&visitorBuffer, strlen(visitorMsg) + 1, 0) == -1) perror("msgsnd");

        if (msgrcv(msqid, (struct msgbuffer *)&visitorBuffer, sizeof(visitorBuffer)-sizeof(long), 0, 0) == -1) {
            perror("msgrcv");
            exit(1);
        }

/*
        // Receive msg from carousell to sit down
        if (msgrcv(msqid, (struct msgbuffer *)&visitorBuffer, sizeof(visitorBuffer)-sizeof(long), 0, 0) == -1) {
            perror("msgrcv");
            exit(1);
        }

        if(strcmp(visitorBuffer.mtext, carousselMsg) == 0) printf("Visitor %d got up on a carousell", visitorId);

        // Receive msg from carousell to get up
        if (msgrcv(msqid, (struct msgbuffer *)&visitorBuffer, sizeof(visitorBuffer)-sizeof(long), 0, 0) == -1) {
            perror("msgrcv");
            exit(1);
        }

        if(strcmp(visitorBuffer.mtext, carousselEndMsg) == 0) printf("Visitor %d left the carousell", visitorId);
     */   
    }

    printf("\n\tVisitor %d is done riding!\n", visitorId);

    memcpy(visitorBuffer.mtext, visitorEndMsg, strlen(visitorEndMsg)+1);
    visitorBuffer.mtype = visitorId;
    if (msgsnd(msqid, (struct msgbuffer *)&visitorBuffer, strlen(visitorEndMsg) + 1, 0) == -1) perror("msgsnd");

    msgctl(msqid, IPC_RMID, NULL);

}

int generateRandomNum(int lower, int upper) {
    return rand()%(upper-lower+1)+lower;
}