#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#include "linkedlist.h"

LinkedListElement_t* findHelper(LinkedListElement_t* Node, char data)
{
    if (Node == NULL) {
        return NULL;
    }
    if (Node->data == data) {
        return Node;
    } else {
        return findHelper(Node->next, data);
    }
}

void addElement(LinkedList_t* list, char data)
{
    LinkedListElement_t* element = calloc(1, sizeof(LinkedListElement_t));
    element->data = data;
    element->next = NULL;
    
    if (list->tail == NULL) {
        list->head = list->tail = element;
    } else {
        list->tail->next = element;
        list->tail = element;
    }
    
}

LinkedListElement_t* findElement(LinkedList_t* list, char data)
{
    if (list == NULL) {
        return NULL;
    } else {
        LinkedListElement_t* ptr = findHelper(list->head, data);
        return ptr;
    }
    
}
void deleteElement(LinkedList_t* list, LinkedListElement_t* element)
{
    if (element == NULL) {
        return
    } 
    if (findElement(list, element->data) = NULL) {
        return
    } else {
        
    }



}

int main(void)
{
    LinkedList_t alist = {.head = NULL, .tail = NULL};
    LinkedListElement_t* element;
    addElement(&alist, 'a');
    addElement(&alist, 'b');
    addElement(&alist, 'c');
    element = findElement(&alist, 'b');
    addElement(&alist, 'd');
    printf("Found element: %c\n", element->data);
    element = findElement(&alist, 'd');
    printf("Found element: %c\n", element->data);
    element = findElement(&alist, 'f');
    if (element == NULL) {
        printf("NULL");
    } else {
        printf("Found element: %c\n", element->data);
    }
    
}