#include <stddef.h>

static void selection_swap(int *x, int *y){int tmp = *x; *x = *y; *y = tmp;}

void selection_sort(int *a, size_t n){
    if(n < 2) return;

    for(size_t i = 0; i < n; i++){
        size_t min = i;
        for(size_t j = i; j < n; j++){
            if(a[min] > a[j]) min = j;
        }
        if(min != i) selection_swap(&a[min], &a[i]);
    }
}