#include <stddef.h>

// Using 'restrict' promises the compiler that arr doesn't alias other pointers,
// unlocking SIMD auto-vectorization and register promotion at -O3.
double sum_array(const double *restrict arr, size_t n) {
    double total = 0.0;
    for (size_t i = 0; i < n; i++) {
        total += arr[i];
    }
    return total;
}