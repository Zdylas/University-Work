#include <stdio.h>
#include <stdint.h>

/* 
Write a function that reads a string from standard input, storing it in a string
which is a character array that can store a string of lenght maxStringLength
The string must terminate and ignore either EOF or newline characters
*/    

size_t readString(char* string, size_t maxStringLength)
{
    size_t count = 0;
    char chr;
    do {
        chr = getchar();
        if (chr != EOF && chr != '\n') {
            *(string++) = chr;
            count++;
        }
    } while (chr != EOF && chr != '\n' && count < maxStringLength);
    *string = '\0';
    return count;
}

int main(void)
{
    size_t len=0;
    char string[11];
    len = readString(string, 10);
    printf("Read String (%s) of length (%zu)\n", string, len);
}