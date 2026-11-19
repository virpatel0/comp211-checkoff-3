import ctypes
import time

# 1. Load both -O0 and -O3 compiled shared libraries
lib_O0 = ctypes.CDLL("./fast_math_O0.so")
lib_O3 = ctypes.CDLL("./fast_math_O3.so")

for lib in (lib_O0, lib_O3):
    lib.sum_array.argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.c_size_t]
    lib.sum_array.restype = ctypes.c_double

# 2. Create 10 million numbers in both a Python list and a contiguous C array
N = 10_000_000
py_list = [1.5] * N
ArrayType = ctypes.c_double * N
c_arr = ArrayType(*py_list)

# Benchmark Pure Python
start = time.perf_counter()
py_total = 0.0
for x in py_list:
    py_total += x
py_time = time.perf_counter() - start

# Benchmark C (-O0)
start = time.perf_counter()
c_O0_total = lib_O0.sum_array(c_arr, N)
c_O0_time = time.perf_counter() - start

# Benchmark C (-O3)
start = time.perf_counter()
c_O3_total = lib_O3.sum_array(c_arr, N)
c_O3_time = time.perf_counter() - start

print(f"Pure Python loop:  {py_time:.4f}s (Result: {py_total})")
print(f"C via ctypes -O0:  {c_O0_time:.4f}s (Result: {c_O0_total}) -> {py_time/c_O0_time:.1f}x faster")
print(f"C via ctypes -O3:  {c_O3_time:.4f}s (Result: {c_O3_total}) -> {py_time/c_O3_time:.1f}x faster")