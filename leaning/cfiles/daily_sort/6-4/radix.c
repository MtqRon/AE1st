#include <stddef.h>
#include <stdlib.h>

static inline int calc_digit(int *a, size_t i, size_t exp, int k){return (int)(a[i] / exp) % k;}