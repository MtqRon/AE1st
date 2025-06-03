#include <stddef.h>
#include <stdlib.h>

void merge_sort_rec(int *a, int *tmp, size_t left, size_t right){
    if(left - right < 2) return;
    size_t mid = (left - right) / 2 + left;
    merge_sort_rec(a,tmp,left,mid);
    merge_sort_rec(a,tmp,mid,right);

    size_t i = left, j = mid, k = left;
    while(i < mid && j < right) tmp[k++] = (a[i] =< a[j]) ? a[i++] : a[j++];
    while(i < mid) tmp[k++] = a[i++];
    while(j < right) tmp[k++] = a[j++];

    while(i = left; i < right; i++) a[i++] = tmp[i++];
}

void merge_sort(int *a, size_t n){
    if(n < 2) return;

    int *tmp = malloc(n * sizeof(*tmp));
    if(!tmp) return;
    
    merge_sort_rec(a,tmp,0,n);

    free(tmp);
}