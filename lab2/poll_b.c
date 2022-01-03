#include <poll.h>
#include <fcntl.h>
#include <sys/types.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <time.h>

#define errExit(msg) do { perror(msg); exit(EXIT_FAILURE); } while (0)
#define NUM_DEVICES 6

int generateRandomNum(int lower, int upper);

int main(int argc, char *argv[]) {
    int nfds, num_open_fds, count = 0;
    struct pollfd *pfds, *tmp;

    srand(time(NULL));

    char devices[6][13] = {
        "/dev/shofer0",
        "/dev/shofer1",
        "/dev/shofer2",
        "/dev/shofer3",
        "/dev/shofer4",
        "/dev/shofer5",
    };

    if(argc < 1) {
        fprintf(stderr, "Usage: %s\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    num_open_fds = nfds = NUM_DEVICES;
    pfds = calloc(nfds, sizeof(struct pollfd));
    tmp = calloc(nfds, sizeof(struct pollfd));
    if (pfds == NULL || tmp == NULL)
        errExit("malloc");


    /* Open each file on command line, and add it 'pfds' array. */
    for (int j = 0; j < nfds; j++) {
        pfds[j].fd = open(devices[j], O_WRONLY);
        if (pfds[j].fd == -1)
            errExit("open");

        printf("Opened \"%s\" on fd %d\n", devices[j], pfds[j].fd);

        pfds[j].events = POLLOUT;
    }

    /* Keep calling poll() as long as at least one file descriptor is
        open. */

    while (num_open_fds > 0) {
        int ready;

        printf("About to poll()\n");
        ready = poll(pfds, nfds, -1);
        if (ready == -1)
            errExit("poll");

        printf("Ready: %d\n", ready);

        /* Deal with array returned by poll(). */

        for (int j = 0; j < nfds; j++) {

            if (pfds[j].revents != 0) {
                printf("  fd=%d; events: %s%s%s%s\n", pfds[j].fd,
                        (pfds[j].revents & POLLOUT) ? "POLLOUT"  : "",
                        (pfds[j].revents & POLLIN)  ? "POLLIN "  : "",
                        (pfds[j].revents & POLLHUP) ? "POLLHUP " : "",
                        (pfds[j].revents & POLLERR) ? "POLLERR " : "");

                if (pfds[j].revents & POLLOUT) {
                    tmp[count] = pfds[j];
                    count++;
                }
                    
            }
        }

        int x = generateRandomNum(0, count);
        char data = (char)generateRandomNum(65, 122);

        ssize_t s = write(tmp[x].fd, &data, 1);
        if (s == -1)
            errExit("write");
        printf("    written byte '%c' to %d\n", (char)data, tmp[x].fd);
        count = 0;
        sleep(5);
        
    }

    printf("All file descriptors closed; bye\n");
    exit(EXIT_SUCCESS);
}

int generateRandomNum(int lower, int upper) {
    return rand()%(upper - lower + 1) + lower;
}