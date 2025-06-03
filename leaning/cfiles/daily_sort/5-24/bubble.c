#include <stddef.h>
#include <stdbool.h>
#define SWAP(x,y,s) do{int _t = (x); (x) = (y); (y) = _t; (s) = true;}while(0)

void bubble_sort(int *a, size_t n){
    bool swapped;
    if(n < 2) return;
    for(size_t i = 1; i < n; i++){
        swapped = false;
        for(size_t j = n - 1; j > 0; j--){
            if(a[j] < a[j - 1]) SWAP(a[j - 1], a[j], swapped);
        }
        if(!swapped) break;
    }
}