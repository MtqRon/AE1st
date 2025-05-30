#include <stddef.h>
#include <stdlib.h>

void counting_sort(int *a, size_t n, int k){
    if(n < 2) return;

    int *cnt = calloc(k, sizeof(*cnt));
    if(!cnt) return;

    for(size_t i = 0; i < n; i++){
        cnt[a[i]]++;
    }

    for(size_t i = 1; i < k; i++){
        cnt[i] += cnt[i - 1];
    }

    int *out = malloc(n * sizeof(*out));
    if(!out) return;

    for(size_t i = n; i > 0; i--){
        int key = a[i - 1];
        out[--cnt[key]] = key;
    }

    for(size_t i = 0; i < n; i++){
        a[i] = out[i];
    }

    free(cnt); free(out);
}