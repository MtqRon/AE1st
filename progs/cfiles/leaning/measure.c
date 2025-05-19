/* measure.c : 汎用ベンチマークフレーム */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <assert.h>
#define _POSIX_C_SOURCE 199309L

typedef void (*sort_fn)(int*, size_t);
extern void bubble_sort(int*, size_t);
extern void insertion_sort(int*, size_t);
extern void shell_sort(int*, size_t);
//extern void quick_sort(int*, size_t);

void fill_random(int *a, size_t n) {
    for (size_t i = 0; i < n; ++i) a[i] = rand();
}
int is_sorted(const int *a, size_t n) {
    for (size_t i = 1; i < n; ++i) if (a[i-1] > a[i]) return 0;
    return 1;
}

/* Windows でも動くよう clock() を使用（精度は ms 程度） */
double bench(sort_fn f,size_t n){
    int *a=malloc(sizeof(int)*n);
    fill_random(a,n);

    clock_t st = clock();
    f(a,n);
    clock_t ed = clock();

    assert(is_sorted(a,n));
    free(a);
    return (double)(ed - st) / CLOCKS_PER_SEC;
}

int main(int argc,char**argv){
    if(argc!=3){
        fprintf(stderr,"usage: %s <bubble|insertion|quick> <size>\n",argv[0]);return 1;}
    size_t n=strtoul(argv[2],NULL,10);
    sort_fn f;
    if(!strcmp(argv[1],"bubble")) f = bubble_sort;
    else if(!strcmp(argv[1],"insertion")) f = insertion_sort;
    else if(!strcmp(argv[1],"shell")) f = shell_sort;
    //else if(!strcmp(argv[1],"quick")) f = quick_sort;
    else {
        fprintf(stderr,"Unknown sort: %s\n",argv[1]);
        return 1;
    }
    printf("%zu,%f\n",n,bench(f,n));
    return 0;
}
