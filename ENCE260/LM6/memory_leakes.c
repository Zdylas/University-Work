#include <stdlib.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

typedef struct {
    char* name;
    int age;
    double height;
} Person_t;


Person_t* newPerson(const char* name, int age, double height)
{
    Person_t* person = calloc(1, sizeof(Person_t));
    char* heap_name = calloc(strlen(name)+1, sizeof(char));
    size_t n = strlen(name);
    Person_t spare_variable = {
        .name = strncpy(heap_name, name, n),
        .age = age,
        .height = height
    };

    *person = spare_variable;

    return person;
}

void freePerson(Person_t* person)
{
    free(person->name);
    free(person);
}


int main(void)
{
    
    Person_t* employee = newPerson("156", 30, 1.68);
    printf("%s is age %d and is %.2f m tall\n", employee->name, employee->age, employee->height);
    freePerson(employee);
}
