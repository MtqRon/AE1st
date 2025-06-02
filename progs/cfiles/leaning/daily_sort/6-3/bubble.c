#include <stddef.h>
#include <stdbool.h>

static void bubble_swap(int *x, int *y, bool *s){int tmp = *x; *x = *y; *y = tmp; *s = true;}

void bubble_sort(int *a, size_t n){
    if(n < 2) return;

    bool swapped;

    for(size_t i = 0; i < n; i++){
        swapped = false;
        for(size_t j = n - 1; j > i; j--){
            if(a[j - 1] > a[j]) bubble_swap(&a[j - 1], &a[j], &swapped);
        }
        if(!swapped) break;
    }
}