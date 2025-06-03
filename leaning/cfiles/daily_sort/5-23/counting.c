#include <stddef.h>
#include <stdlib.h>

void counting_sort(int *a, size_t n, int k){
    if(n < 2) return;

    int *cnt = calloc(k, sizeof(*cnt));
    if(!cnt) return;

    for(size_t i = 0; i < k; i++){
        cnt[a[i]]++;
    }


    for(size_t j = 0; j < k; j++){
        cnt[j] += cnt[j - 1];
    }

    int *out = malloc(n * sizeof(*out));
    if(!out){
        free(cnt);
        return;
    }

    for(size_t i = n; i > 0; i--){
        int key = a[i - 1];
        cnt[key]--;
        out[cnt[key]] = key;
    }

    for(size_t i = 0; i < n; i++){
        a[i] = out[i];
    }

    free(cnt);
    free(out);
}