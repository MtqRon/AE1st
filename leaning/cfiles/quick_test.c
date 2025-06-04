#include <stdio.h>

/* ---------- ユーティリティ ---------- */
static int step = 0;              /* 何ステップ目かカウント */

void print_array(const int *a, int n,
                 int low, int high, int mid)
{
    printf("step %2d  [low=%d,high=%d]  mid=%d : ",
           step++, low, high, mid);
    for (int i = 0; i < n; ++i) {
        if (i == low)  printf("|");      /* 区間の左端 */
        if (i == mid)  printf("*");      /* ↑ pivot 以下/超の境界 */
        printf("%d", a[i]);
        if (i == mid)  printf("*");
        if (i == high) printf("|");      /* 区間の右端 */
        if (i != n - 1) printf(" ");
    }
    putchar('\n');
}

/* ---------- Hoare パーティション ---------- */
int partition(int a[], int low, int high)
{
    int pivot = a[(low + high) / 2];
    int i = low - 1, j = high + 1;

    while (1) {
        do { ++i; } while (a[i] < pivot);
        do { --j; } while (a[j] > pivot);
        if (i >= j) return j;     /* ← “境界” を返す */
        int tmp = a[i]; a[i] = a[j]; a[j] = tmp;
    }
}

/* ---------- 手動スタック版クイックソート（可視化付き） ---------- */
void quicksort(int a[], int n)
{
    int stack[32];
    int top = -1;

    int low = 0, high = n - 1;
    stack[++top] = low;
    stack[++top] = high;

    while (top >= 0) {
        high = stack[top--];
        low  = stack[top--];

        while (low < high) {
            int mid = partition(a, low, high);
            print_array(a, n, low, high, mid);   /* ←★ここで状態を表示 */

            /* ― 小さい側をループ、大きい側を push ― */
            if (mid - low < high - mid) {        /* 左が小さい？ */
                if (mid + 1 < high) {            /* 右“大きい”側を push */
                    stack[++top] = mid + 1;
                    stack[++top] = high;
                }
                high = mid;                      /* 左“小さい”側を続行 */
            } else {                             /* 右が小さい */
                if (low < mid) {                 /* 左“大きい”側を push */
                    stack[++top] = low;
                    stack[++top] = mid;
                }
                low = mid + 1;                   /* 右“小さい”側を続行 */
            }
        }
    }
}

/* ---------- デモ用 main ---------- */
int main(void)
{
    int a[] = {8, 3, 1, 7, 0, 10, 2, 11, 23, 2, 9, 0, 41, 33, 83, 63, 3, 18};
    int n = sizeof a / sizeof a[0];

    puts("=== 初期配列 ===");
    print_array(a, n, 0, n - 1, -1);

    quicksort(a, n);

    puts("\n=== 完全に整列後 ===");
    print_array(a, n, 0, n - 1, -1);
    return 0;
}
