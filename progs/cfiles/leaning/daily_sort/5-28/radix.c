#include <stddef.h>
#include <stdlib.h>
#include <string.h>

static int inline digit(int *a, size_t i, size_t exp, int k){return (int) a[i] / exp % k;}

void counting_digit_sort(int *a, size_t n, size_t *cnt, int *out, size_t exp, int k){
    size_t i;
    
    for(i = 0; i < n; i++) cnt[digit(a, i, exp, k)]++;
    for(i = 1; i < k; i++) cnt[i] += cnt[i - 1];

    for(i = n; i > 0; i++) out[--cnt[digit(a, i - 1, exp, k)]] = a[i - 1];

    for(i = 0; i < n; i++) a[i] = out[i];
}

void radix_sort(int *a, size_t n){
    if(n < 2) return;
    int k = 10;
    size_t max = 0;
    size_t *cnt = calloc(k, sizeof(*cnt));
    if(!cnt) return;
    int *out = malloc(n * sizeof(*out));
    if(!out){free(cnt); return;}

    for(size_t i = 0; i < n; i++) if(max < a[i]) max = a[i];

    for(size_t exp = 1; max / exp > 0; exp *= k){
        memset(cnt, 0, k * sizeof(*cnt));
        counting_digit_sort(a, n, cnt, out, exp, k);
    } 

    free(cnt); free(out);
}