#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>


    void im_cool(int16_t index, size_t n, int16_t* ptr)
    {
        if (index >= n) {
            return;
        };
        *(ptr+index) = index+1;  
        index++;
        im_cool(index, n, ptr);

    }

    void fillRamp(int16_t* data, size_t n)
    {
        im_cool(0, n, data);
    }

int main(void) 
{
    int16_t* data = calloc(4, sizeof(int16_t));
    fillRamp(data, 4);
    for (size_t i = 0; i < 4; i++) {
        printf("data[%zu] = %d\n", i, data[i]);
    }
    free(data);
}