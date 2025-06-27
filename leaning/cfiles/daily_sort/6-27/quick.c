#include <stddef.h>

static void swap(int *x, int *y){int tmp = *x; *x = *y; *y = tmp;}

static int partition(int *a, size_t left, size_t right){
    size_t i, j, pivot, t;

    i = left - 1;
    j = right;

    pivot = a[right];

    for(;;){
        while(a[++i] < pivot);
        while(i < --j && a[j] > pivot);

        if(i >= j){
            break;
        }

        swap(&a[i], &a[j]);
    }
    swap(&a[i], &a[right]);
    return i;
}

static void quick_sort_rec(int *a, size_t left, size_t right){
    size_t v;

    if(right <= left) return;

    v = partition(a, left, right);

    if(v > left) quick_sort_rec(a, left, v - 1);
    if(v < right) quick_sort_rec(a, v + 1, right);
}

void quick_sort(int *a, size_t n){
    if(n < 2)return;

    quick_sort_rec(a, 0, n - 1);
}