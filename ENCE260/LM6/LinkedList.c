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

void deleteHelper(LinkedListElement_t* Node, char data, LinkedListElement_t* prevNode)
{
    if (Node == NULL) {
        return;
    }
    if (Node->data == data) {
        prevNode->next = Node->next;
        free(Node);
        
    } else {
        deleteHelper(Node->next, data, Node);
    }
}

void deleteElement(LinkedList_t* list, LinkedListElement_t* element)
{
    if (element == NULL) {
        return;
    } 
    if (findElement(list, element->data) == NULL) {
        free(element);
        return;
    }
    if (list->head == element && list->tail == element) {
        list->head = NULL;
        list->tail = NULL;
        free(element);
        return;
    }
    if (list->head == element) {
        list->head = element->next;
        free(element);
    } else {
        deleteHelper(list->head, element->data, NULL);
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
    deleteElement(&alist, element);
    for (LinkedListElement_t* elem=alist.head; elem != NULL; elem = elem->next) {
        printf("%c", elem->data);
    }
    //Clean up
    while (alist.head != NULL) {
        deleteElement(&alist, alist.head);
    }
}
