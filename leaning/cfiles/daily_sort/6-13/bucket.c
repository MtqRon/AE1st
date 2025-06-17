#include <stdlib.h>
#include <string.h>

static void swap(int *x, int *y){int tmp = *x; *x = *y; *y = tmp;}

static void insertion_sort(int *a, size_t n){
    for(size_t i = 1; i < n; i++){
        int key = a[i];
        size_t j = i;
        while(j && a[j - 1] > key){
            a[j] = a[j - 1];
            j--;
        }
    }
}

void bucket_sort(int *a, size_t n, int k){
    if(n < 2) return;

    size_t B = n / 16 + 1;
    int **bucket = calloc(B, sizeof(*bucket));
    size_t *cnt = calloc(B, sizeof(*cnt));
    if(!bucket || !cnt){return;}

    for(size_t i = 0; i < n; i++){
        size_t id = (size_t)((long long)a[i] * B / k);
        if(id >= B) id = B - 1;
        size_t c = cnt[id]++;

        if(c & (c + 1)){
            bucket[id][c] = a[i];
        }else{
            size_t newcap = (c ? (c + 1) * 2 : 4);
            bucket[id] = realloc(bucket[id], newcap * sizeof(**bucket));
            if(!bucket[id]) return;
            bucket[id][c] = a[i];
        }
    }

    size_t idx = 0;
    for(size_t b = 0; b < B; b++){
        if(cnt[b]){
            insertion_sort(bucket[b], cnt[b]);
            memcpy(&a[idx], bucket[b], cnt[b] * sizeof(*a));
            idx += cnt[b];
        }
        free(bucket[b]);
    }
    free(bucket); free(cnt);
}