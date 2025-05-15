/* quick.c : クイックソートの実装 */
#include <stddef.h>

// クイックソートの補助関数（パーティション処理）
static int partition(int *a, int low, int high) {
    int pivot = a[high];  // 最後の要素をピボットとして選択
    int i = low - 1;      // 小さい要素のインデックス
    
    for (int j = low; j < high; j++) {
        // 現在の要素がピボット以下の場合
        if (a[j] <= pivot) {
            i++;
            // 要素を交換
            int temp = a[i];
            a[i] = a[j];
            a[j] = temp;
        }
    }
    
    // ピボットを正しい位置に配置
    int temp = a[i + 1];
    a[i + 1] = a[high];
    a[high] = temp;
    
    return i + 1;  // ピボットの位置を返す
}

// 再帰的なクイックソート実装
static void quick_sort_recursive(int *a, int low, int high) {
    if (low < high) {
        // 配列をパーティション分割し、ピボットの位置を取得
        int pi = partition(a, low, high);
        
        // ピボットの左側をソート
        quick_sort_recursive(a, low, pi - 1);
        // ピボットの右側をソート
        quick_sort_recursive(a, pi + 1, high);
    }
}

// measure.cから呼び出されるインターフェース関数
void quick_sort(int *a, size_t n) {
    if (n <= 1) return;  // 空配列または要素が1つの場合は何もしない
    quick_sort_recursive(a, 0, n - 1);
} 