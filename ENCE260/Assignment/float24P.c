#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <limits.h>
#include <math.h>
#include <stdbool.h>
#include <ctype.h>
#include "float24.h"

Float24_t float24_init(int16_t mantissa, int8_t exponent) 
{
    Float24_t new_float;
    new_float.mantissa = mantissa;
    new_float.exponent = exponent;
    return new_float;
}

void float24_print(Float24_t float24) 
{
    printf("%d * 2 ^ %d\n", float24.mantissa, float24.exponent);
}

static Float24_t float24_normalise(int32_t oversizeMantissa, int8_t exponent) 
{
    while (oversizeMantissa > INT16_MAX || oversizeMantissa < -INT16_MAX) {
        exponent++;
        oversizeMantissa /= 2;
    }
    return float24_init(oversizeMantissa, exponent);
}

Float24_t float24_multiply(Float24_t num1, Float24_t num2)
{
    int32_t newMantissa = num1.mantissa * num2.mantissa;
    int8_t newExponent = num1.exponent + num2.exponent;
    return float24_normalise(newMantissa, newExponent);    
}

static int32_t powerOfTwo(int16_t exponent) 
{
    int32_t power = 1;
    for (int32_t i = 0; i < (exponent); i++) {
        power *= 2;
    }
    return power;
}


Float24_t float24_add(Float24_t num1, Float24_t num2)
{
    int16_t newExponent = (num1.exponent > num2.exponent) ? num1.exponent : num2.exponent;
    int32_t power1 = powerOfTwo(num1.exponent - newExponent);
    int32_t power2 = powerOfTwo(num2.exponent - newExponent);
    int32_t newMantissa = (num1.mantissa / power1 + num2.mantissa / power2);
    return float24_normalise(newMantissa, newExponent);
}


static int32_t charArrayToInt(char* buffer, uint8_t bufferLength)
{   
    int32_t integer = 0;
    for (uint8_t i = 0; i < bufferLength; i++) {
        if (buffer[i] != 0) {
            integer *= 10;
            integer += (buffer[i] - '0');
        }
    }
    return integer;
}


static void processChar(char character, char* strPtr, int8_t* signPtr, int8_t* index)
{
    if (*index == 0 && (character == '+' || character == '-')) {
        *signPtr = character == '+' ? 1 : -1;
        *index = -1;
    } else if (isdigit(character)) {
        *(strPtr + *index) = character;
    }
}


Float24_t float24_read(void)
{
    char mantissaStr[50] = {0};
    char exponentStr[50] = {0};
    int8_t mantissaSign = 1;
    int8_t exponentSign = 1;
    char character = 0;
    bool isMantissa = true;
    int8_t i = 0;
    character = getchar();
    while (character > 42) {
        if (isMantissa) {
            if (character == 'b') {
                isMantissa = false;
                i = -1;
            } else {
                processChar(character, mantissaStr, &mantissaSign, &i);
            }
        } else {
            processChar(character, exponentStr, &exponentSign, &i);
        }
        i++;
        character = getchar();
    }
    if (exponentStr[0] == 0) {
        return float24_init(0, -128);
    }
    int32_t mantissa = charArrayToInt(mantissaStr, 50) * mantissaSign;
    int32_t exponent = charArrayToInt(exponentStr, 50) * exponentSign;
    if (abs(exponent) > 127) {
        exponent = exponentSign * 127;
    }
    int8_t smaller_exponent = exponent;
    return float24_normalise(mantissa, smaller_exponent);
}

void float24_max(Float24_t* num1, Float24_t* num2, Float24_t** max) 
{
    int64_t num1_total = num1->mantissa * powerOfTwo(num1->exponent);
    int64_t num2_total = num2->mantissa * powerOfTwo(num2->exponent);
    *max = num2;
    if (num1_total > num2_total) {
        *max = num1;
    } else if (num1_total == num2_total) {
        if (num1->exponent >= num2->exponent) {
            *max = num1;
        }
    }
}


Float24_t* float24_arrayMax(Float24_t* array, size_t size, void (*func)(Float24_t*, Float24_t*, Float24_t**))
{
    Float24_t* max = &array[0];
    for (size_t i = 1; i < size; i++) {
        func(max, &array[i], &max);
    }
    return max;

    /*
    printf("%ld\n", size);
    Float24_t new_array[size-1];
    Float24_t* temp_pointer = NULL;
    if (size <= 1) {
        return &array[0];
    }
    if (size == 2) {
        func(&array[0], &array[1], &temp_pointer);
        return temp_pointer;
    } else {
        func(&array[0], &array[1], &temp_pointer);
        new_array[0] = *temp_pointer;
        for (int i = 2; i < size; i++) {
            new_array[i-1] = array[i];
        }
        size -= 1;
        return float24_arrayMax(new_array, size, func);
    }
    */
}

int main(void)
{
    Float24_t* max = NULL;
    for (int i = -127; i < 127; i++) {
        Float24_t b = float24_init(2, i);
        float24_max(NULL, &b, &max);
        float24_print(*max);

    }
    
}