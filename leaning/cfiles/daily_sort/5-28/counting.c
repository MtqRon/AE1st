#include <stddef.h>
#include <stdlib.h>

void counting_sort(int *a, size_t n, int k){
    if(n < 2 || k <= 0) return;  // 入力検証を追加
      size_t *cnt = calloc((size_t)k, sizeof(*cnt));  // 型キャストを追加
    if(!cnt) return;
    
    size_t i;
    // 範囲チェックを追加
    for(i = 0; i < n; i++){
        if(a[i] < 0 || a[i] >= k){
            free(cnt);
            return;  // 範囲外の値がある場合は処理を中止
        }
        cnt[a[i]]++;
    }

    for(i = 1; i < (size_t)k; i++) cnt[i] += cnt[i - 1];  // 型キャストを追加

    int *tmp = malloc(n * sizeof(*tmp));
    if(!tmp){free(cnt); return;}

    for(i = n; i > 0; i--){
        int key = a[i - 1];
        tmp[--cnt[key]] = key;
    }

    for(i = 0; i < n; i++) a[i] = tmp[i];

    free(cnt); free(tmp);
}