#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <ctype.h>

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

size_t readFile(FILE* file)
{
    size_t i = 0;
    char chr = getchar();
    char letter;
	while (fscanf(file, "%c", &letter) != EOF) {
        if (letter == chr) {
            i++;
            
        }
    }

    return i;
}

FILE* openInputFile(char* filename)
{
    FILE* aFile;
    char mode[] = "r";
    aFile = fopen(filename, mode);
    if (aFile == NULL) {
        printf("Input file can't be opened\n");
        exit(0);
    }
    return aFile;
}



int main(void)
{
    char string[81];

    readString(string, 80);
    FILE* Input_File = openInputFile(string);
    size_t tally = readFile(File);
    fclose(File);
    printf("%ld", tally);
}