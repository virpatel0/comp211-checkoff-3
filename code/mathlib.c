#include <stddef.h>
#include <stdint.h>

// 1. Simple pass-by-value function
int32_t add_ints(int32_t a, int32_t b) {
    return a + b;
}

// 2. Pointer-based function: doubles every element in a contiguous C array in-place
void double_array(int32_t *arr, size_t len) {
    for (size_t i = 0; i < len; i++) {
        arr[i] *= 2;
    }
}
