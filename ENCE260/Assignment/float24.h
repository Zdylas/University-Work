#ifndef FLOAT24_H
#define FLOAT24_H

#include <stdint.h>
#include <stdio.h>
#include <limits.h>
#include <math.h>
#include <ctype.h>
#include <stdbool.h>
#include <stdlib.h>

typedef struct {
    int16_t mantissa;
    int8_t exponent;

} Float24_t; 

float float24_asIEEE(Float24_t x);
Float24_t float24_init(int16_t mantissa, int8_t exponent);
void float24_print(Float24_t value);
Float24_t float24_multiply(Float24_t num1, Float24_t num2);
Float24_t float24_add(Float24_t num1, Float24_t num2);
Float24_t readHelper(int32_t mantissa, int16_t exponent, bool malformed, bool negative_exponent, bool negative_mantissa);
Float24_t float24_read(void);
void float24_max(Float24_t* num1, Float24_t* num2, Float24_t** max);
Float24_t* float24_arrayMax(Float24_t* array, size_t size, void (*func)(Float24_t*, Float24_t*, Float24_t**));

#endif