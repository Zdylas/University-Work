#include <stdint.h>
#include <stdio.h>
#include <limits.h>
#include <math.h>
#include <ctype.h>
#include <stdbool.h>
#include <stdlib.h>

#include "float24.h"

Float24_t float24_init(int16_t mantissa, int8_t exponent)
{
    Float24_t temporary = {
        .mantissa = mantissa,
        .exponent = exponent
    };
    return temporary;
}

void float24_print(Float24_t value)
{
    printf("%d * 2 ^ %d\n", value.mantissa, value.exponent);
}

Float24_t float24_normalise(int32_t oversizeMantissa, int8_t exponent)
{
    if (oversizeMantissa > INT16_MAX || oversizeMantissa < -INT16_MAX) {
        oversizeMantissa /= 2;
        if (exponent == INT8_MAX) {
            ;
        } else {
            exponent += 1;
        }
        
        return float24_normalise(oversizeMantissa, exponent);
    } else {
        return float24_init(oversizeMantissa, exponent);
    }
}

Float24_t float24_multiply(Float24_t num1, Float24_t num2) 
{
    int32_t mantissa = num1.mantissa * num2.mantissa;
    int8_t exponent = num1.exponent + num2.exponent;
    return float24_normalise(mantissa, exponent);
}

Float24_t float24_add(Float24_t num1, Float24_t num2)
{

    int8_t exponent;
    int32_t mantissa;

    if (num1.exponent > num2.exponent) {
        exponent = num1.exponent;
    } else {
        exponent = num2.exponent;
    }
    int32_t num1_prime = num1.mantissa * pow(2, num1.exponent) / pow(2, exponent);
    int32_t num2_prime = num2.mantissa * pow(2, num2.exponent) / pow(2, exponent);
    mantissa = num1_prime+num2_prime;
    return float24_normalise(mantissa, exponent);
}

Float24_t readHelper(int32_t mantissa, int16_t exponent, bool malformed, bool negative_exponent, bool negative_mantissa)
{
    if (negative_exponent) {
        exponent = -exponent;
    }

    if (negative_mantissa) {
        mantissa = -mantissa;
    }

    if (malformed) {
        return float24_normalise(0, -128);
    } else {
        if (exponent < -127) {
            exponent = -127;
        }
        if (exponent > 127) {
            exponent = 127;
        }
        return float24_normalise(mantissa, exponent);
    }
    
}

Float24_t float24_read(void)
{
    bool malformed = true;
    bool negative_mantissa = false;
    bool negative_exponent = false;
    char chr;
    int32_t mantissa = 0;
    int16_t exponent = 0;
    chr = getchar();
    if (chr == '-') {
        negative_mantissa = true;
        chr = getchar();
    }
    while (isdigit(chr)) {
        mantissa = (mantissa * 10) + (chr - '0');
        chr = getchar();
    }
    if (chr != 'b') {
        return float24_normalise(0, -128);
    }
    chr = getchar();
    if (chr == '-') {
        negative_exponent = true;
        chr = getchar();
    }
    while (isdigit(chr)) {
        malformed = false;
        exponent = (exponent * 10) + (chr-'0');
        chr = getchar();
    } 
    return readHelper(mantissa, exponent, malformed, negative_exponent, negative_mantissa);
}

void float24_max(Float24_t* num1, Float24_t* num2, Float24_t** max)
{
    Float24_t difference = float24_add(*num1, float24_multiply(*num2, float24_init(-1,0)));;
    if (difference.mantissa == 0) {
        if (num1->exponent >= num2->exponent) {
            *max = num1;
            return;
        } else {
            *max = num2;
            return;
        }
    } 
    if (difference.mantissa > 0) {
        *max = num1;
    } else {
        *max = num2;
    }
}

Float24_t* float24_arrayMax(Float24_t* array, size_t size, void (*func)(Float24_t*, Float24_t*, Float24_t**))
{
    Float24_t* max = &array[0];
    for (size_t i = 1; i < size; i++) {
        func(max, &array[i], &max);
    }
    return max;
}
