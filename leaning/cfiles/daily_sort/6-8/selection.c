#include <stddef.h>

static void swap(int *x, int *y){int tmp = *x; *x = *y; *y = tmp;}

void selection_sort(int *a, size_t n){
    if(n < 2) return;

    for(size_t i = 0; i < n - 1; i++){
        size_t min = i;
        for(size_t j = i + 1; j < n; j++) if(a[j] < a[min]) min = j;
        if(i != min) swap(&a[min], &a[i]);
    }
}