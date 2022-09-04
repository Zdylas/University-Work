#ifndef LINKEDLIST_H
#define LINKEDLIST_H

#include <stdint.h>

struct linkedlistelement_s {
    char data;
    struct linkedlistelement_s* next;
};
typedef struct linkedlistelement_s LinkedListElement_t;

typedef struct {
    LinkedListElement_t* head;
    LinkedListElement_t* tail;
} LinkedList_t;

void addElement(LinkedList_t* list, char data);
LinkedListElement_t* findElement(LinkedList_t* list, char data);
void deleteElement(LinkedList_t* list, LinkedListElement_t* element);

#endif
