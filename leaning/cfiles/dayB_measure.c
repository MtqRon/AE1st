#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include <time.h>
#include <stdbool.h>

typedef void (*sort_fn)(int*, size_t);
extern void insertion_sort(int*, size_t);
extern void shell_sort(int*, size_t);
extern void heap_sort(int*, size_t);
extern void radix_sort(int*, size_t);
extern void bucket_sort(int*, size_t, int);

void fill_random(int *a, size_t n) {
    for (size_t i = 0; i < n; ++i) {
        a[i] = rand();
    }
}

void fill_random_range(int *a, size_t n, int k) {
    for (size_t i = 0; i < n; ++i) {
        a[i] = rand() % k;  // 0からk-1の範囲の値を生成
    }
}

bool is_sorted(int *a, size_t n) {
    for (size_t i = 1; i < n; ++i) {
        if (a[i - 1] > a[i]) {
            return false;
        }
    }
    return true;
}

double bench(sort_fn f, size_t n){
    int *a = malloc(sizeof *a * n);
    if (!a) {
        perror("malloc");
        exit(EXIT_FAILURE);
    }
    fill_random(a, n);

    clock_t st = clock();
    f(a, n);
    clock_t ed = clock();

    if (!is_sorted(a, n)) {
        fprintf(stderr, "Error: Array is not sorted after sorting\n");
        free(a);
        exit(EXIT_FAILURE);
    }
    free(a);
    return (double)(ed - st) / CLOCKS_PER_SEC;
}

double bench_bucket(void (*f)(int*, size_t, int), size_t n, int k){
    int *a = malloc(sizeof *a * n);
    if (!a) {
        perror("malloc");
        exit(EXIT_FAILURE);
    }
    fill_random_range(a, n, k);  // 範囲指定のランダム生成を使用

    clock_t st = clock();
    f(a, n, k);
    clock_t ed = clock();

    if (!is_sorted(a, n)) {
        fprintf(stderr, "Error: Array is not sorted after bucket sort\n");
        free(a);
        exit(EXIT_FAILURE);
    }
    free(a);
    return (double)(ed - st) / CLOCKS_PER_SEC;
}

int main(int argc, char **argv){
    srand((unsigned int)time(NULL));  // シードを設定
    
    if (argc < 3) {
        fprintf(stderr,
                "usage: %s <insertion|shell|heap|radix|bucket> <size> [k]\n",
                argv[0]);
        return 1;
    }

    size_t n = strtoul(argv[2], NULL, 10);
    double elapsed;

    if (!strcmp(argv[1], "insertion")) {
        elapsed = bench(insertion_sort, n);
    } else if (!strcmp(argv[1], "shell")){
        elapsed = bench(shell_sort, n);
    } else if (!strcmp(argv[1], "heap")) {
        elapsed = bench(heap_sort, n);
    } else if(!strcmp(argv[1], "radix")){
        elapsed = bench(radix_sort, n);
    } else if(!strcmp(argv[1], "bucket")){
        if(argc != 4){
            fprintf(stderr,"usage: %s bucket <size> <k>\n", argv[0]);
            return 1;
        }
        int k = atoi(argv[3]);
        elapsed = bench_bucket(bucket_sort, n, k);
    } else {
        fprintf(stderr, "Unknown sort: %s\n", argv[1]);
        return 1;
    }

    printf("%zu,%f\n", n, elapsed);
    return 0;
}
