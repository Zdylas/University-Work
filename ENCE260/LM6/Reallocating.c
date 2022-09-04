#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>


int main(void)
{
    int16_t number;
    size_t length = 10;
    int16_t* ptr = calloc(length, sizeof(int16_t));
    size_t index = 0;
    scanf("%hd", &number);
    while (number != -10000) {
        if (index+1 < length) {
            ptr[index] = number;
        } else {
            length += 10;
            ptr = realloc(ptr, length*sizeof(int16_t));
            ptr[index] = number;
        }
        index++;
        scanf("%hd", &number);
    };
    printf("Numbers read = %ld\n", index);
    free(ptr);
}