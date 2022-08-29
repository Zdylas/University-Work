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

void writeFile(FILE* Input_File, FILE* Output_File)
{

    char letter;
    char prev_letter = ' ';
    char new_letter;
    while (fscanf(Input_File, "%c", &letter) != EOF) {
        if (isalpha(letter) && isspace(prev_letter)) {
            new_letter = toupper(letter);
            fprintf(Output_File, "%c", new_letter);
        } else {
            new_letter = tolower(letter);
            fprintf(Output_File, "%c", new_letter);
        }
        prev_letter = letter;
    }
}

FILE* openInputFile(char* filename)
{
    FILE* aFile;
    char mode[] = "r";
    aFile = fopen(filename, mode);
    if (aFile == NULL) {
        printf("Input file can't be opened\n");
    }
    return aFile;
}

FILE* openOutputFile(char* filename)
{
    FILE* aFile;
    char mode[] = "w";
    aFile = fopen(filename, mode);
    if (aFile == NULL) {
        printf("Output file can't be opened\n");
    }
    return aFile;
}

int main(void)
{
    char string[81];

    readString(string, 80);
    FILE* Input_File = openInputFile(string);

    readString(string, 80);
    FILE* Output_File = openOutputFile(string);

    if (Input_File == NULL || Output_File == NULL) {
        if (Output_File != NULL) {
            fclose(Output_File);
        }

        if (Input_File != NULL) {
            fclose(Input_File);
        }
        exit(0);
    }
    writeFile(Input_File, Output_File);
    fclose(Input_File);
    fclose(Output_File);

}


