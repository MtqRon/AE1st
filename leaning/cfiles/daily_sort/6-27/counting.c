#include <stddef.h>
#include <stdlib.h>

void counting_sort(int *a, size_t n, int k){
    if(n < 2) return;

    size_t *cnt = calloc(k, sizeof(*cnt));
    if(!cnt) return;

    size_t i;
    
    for(i = 0; i < n; i++){
        if(a[i] < 0 || a[i] >= k){
            free(cnt);
            return;
        }
        cnt[a[i]]++;
    }

    for(i = 1; i < k; i++) cnt[i] += cnt[i - 1];

    int *out = malloc(n * sizeof(*out));
    if(!out){
        free(cnt);
        return;
    }

    for(i = n; i > 0; i--){
        int key = a[i - 1];
        out[--cnt[key]] = key;
    }

    for(i = 0; i < n; i++){
        a[i] = out[i];
    }

    free(cnt); free(out);
}