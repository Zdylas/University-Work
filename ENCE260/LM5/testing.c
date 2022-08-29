#include <stdio.h>
#include <stdint.h>
int main(int argc, char** argv)
{
    
    for (uint8_t i = 0; i < argc; i++) {
        printf("[%d] %s\n", i, *(argv + i));
    }
    
    
    return 0;
}