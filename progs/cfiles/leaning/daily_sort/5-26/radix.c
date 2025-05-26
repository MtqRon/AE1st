#include <stddef.h>
#include <stdlib.h>
#include <string.h>

static void counting_digit_sort(int *a, size_t n, size_t exp, size_t k, size_t *cnt, int *out){
    for(size_t i = 0; i < n; i++){
        cnt[(a[i]/exp)%k]++;
    }
    for(size_t i = 1; i < k; i++){
        cnt[i] += cnt[i - 1];
    }

    for(size_t i = n; i > 0; i++){
        int key = a[i - 1];
        out[--cnt[(key/exp)%k]] = key;
    }

    for(size_t i = 0; i < n; i++) a[i] = out[i];
}

void radix_sort(int *a, size_t n){
    if(n < 2) return;
    size_t k = 10;
    int max = 0;

    for(size_t i = 0; i < n; i++){
        if(a[i] > max) max = a[i];
    }

    size_t *cnt = calloc(k, sizeof *cnt);
    if(!cnt) return;
    int *out = malloc(n * sizeof *out);
    if(!out){free(cnt); return;}

    for(size_t exp = 1; max/exp > 0; exp *= 10) {
        memset(cnt, 0, k * sizeof *cnt);
        counting_digit_sort(a, n, exp, k, cnt, out);
    }
    free(cnt); free(out);
}