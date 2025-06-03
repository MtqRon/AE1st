#include <stddef.h>
#include <stdlib.h>
#include <string.h>

int static set_digit(int *a, int i, size_t exp, int k){return (int)((a[i] / exp) % k);}

void counting_digit_sort(int *a, size_t n, size_t *cnt, int *out, size_t exp, int k){
    for(size_t i = 0; i < n; i++){
        cnt[set_digit(a, i, exp, k)]++;
    }
    for(size_t i = 1; i < k; i++){
        cnt[i] += cnt[i - 1];
    }
    for(size_t i = n; i > 0; i--){
        int digit = set_digit(a, i - 1, exp, k);
        out[--cnt[digit]] = a[i - 1];
    }
    for(size_t i = 0; i < n; i++) a[i] = out[i];
}

void radix_sort(int *a, size_t n){
    if(n < 2) return;
    
    int k = 10;
    size_t max = 0;
    
    for(size_t i = 0; i < n; i++){
        max = (max < a[i]) ? a[i] : max;
    }

    size_t *cnt = malloc(k * sizeof(*cnt));
    if(!cnt) return;
    int *out = malloc(n * sizeof(*out));
    if(!out){ free(cnt); return;}

    for(size_t exp = 1; max/exp > 0; exp *= 10){
        memset(cnt, 0, sizeof(*cnt));
        counting_digit_sort(a, n, cnt, out, exp, k);
    }

    free(cnt); free(out);
}