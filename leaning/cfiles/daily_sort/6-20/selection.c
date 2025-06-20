#include <stddef.h>

static void swap(int *x, int *y){int tmp = *x; *x = *y; *y = tmp;}

void selection_sort(int *a, size_t n){
    if(n < 2) return;

    for(size_t i = 0; i < n; i++){
        int min = i;
        for(size_t j = n - 1; j > i; j--){
            if(a[min] > a[j]) min = j;
        }
        if(i != min) swap(&a[min], &a[i]);
    }
}