#include <stddef.h>
#include <stdbool.h>
#define SWAP(x,y,s) do{int _t = (x); (x) = (y); (y) = _t; (s) = true;}while(0)

void bubble_sort(int *a, size_t n){
    if(n < 2) return;
    bool swapped;
    for(size_t i = 0; i < n - 1; i++){
        swapped = false;
        for(size_t j = n - 1 - i; j > 0; j--){
            if(a[j - 1] > a[j]) SWAP(a[j], a[j - 1], swapped);
        }
        if(!swapped) break;
    }
}