#include <stddef.h>
#include <stdlib.h>

void counting_sort(int *a, size_t n, int k){
    if(n < 1) return;

    int *cnt = calloc(k, sizeof *cnt);
    if(!cnt) return;

    for(int i = 0; i < k; i++) cnt[i] = 0;

    for(size_t i = 0; i < n; i++){
        cnt[a[i]]++;
    }

    for(int i = 1; i < k; i++){
        cnt[i] += cnt[i - 1];
    }

    int *out = malloc(n * sizeof(*out));
    if (!out) { free(cnt); return; }

    for(size_t i = n; i > 0; i--){
        int v = a[i - 1];
        cnt[v]--;
        out[cnt[v]] = v;
    }

    for(size_t i = 0; i < n; i++){
        a[i] = out[i];
    }

    free(cnt);
    free(out);
}