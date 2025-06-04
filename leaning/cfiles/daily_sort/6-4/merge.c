#include <stddef.h>
#include <stdlib.h>

void merge_sort_rec(int *a, int *out, size_t left, size_t right){
    if(right - left < 2) return;
    
    size_t mid = (right - left) / 2 + left;

    merge_sort_rec(a, out, left, mid);
    merge_sort_rec(a, out, mid, right);

    size_t i = left, j = mid, k = left;

    while(i < mid && j < right) out[k++] = (a[i] < a[j]) ? a[i++] : a[j++];
    while(i < mid) out[k++] = a[i++];
    while(j < right) out[k++] = a[j++];

    for(i = left; i < right; i++){
        a[i] = out[i];
    }
}

void merge_sort(int *a, size_t n){
    if(n < 2) return;

    int *out = malloc(n * sizeof(*out));
    if(!out) return;

    merge_sort_rec(a, out, 0, n);

    free(out);
}