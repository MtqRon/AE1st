#include <stddef.h>
#include <stdlib.h>
#include <string.h>

static inline int calc_digit(int *a, size_t i, size_t exp, int k){return (a[i] / exp)%k;}
static void counting_digit_sort(int *a, size_t *cnt, int *out, size_t exp, int k){
    size_t i;
    for(i = 0; i < n; i++){
        cnt[calc_digit(a, i, exp, k)]++;
    }

    for(i = 1; i < k; i++) cnt[i] += cnt[i - 1];

    for(i = n - 1; i > 0; i--){
        int key = a[i];
        out[--cnt[calc_digit(a, i, exp, k)]] = key;
    }

    for(i = 0; i < n; i++) a[i] = out[i];
}

void radix_sort(int *a, size_t n){
    if(n < 2) return;

    size_t max = 0; 
    size_t i;
    int k = 10;

    size_t *cnt = calloc(k, sizeof(*cnt));
    if(!cnt) return;

    int *out = malloc(n * sizeof(*out));
    if(!out){
        free(cnt);
        return;
    }


    for(i = 0; i < n; i++){
        if(max < a[i]) max = a[i];
    }

    for(exp = 1; max / exp > 0; exp *= k){
        memset(cnt, 0, k * sizeof(*cnt));
        counting_digit_sort(a, cnt, out, exp, k);
    }

    free(cnt); free(out);
}