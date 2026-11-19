import ctypes
import os
import platform
import time
import numpy as np

ext = ".dylib" if platform.system() == "Darwin" else ".dll" if platform.system() == "Windows" else ".so"
lib = ctypes.CDLL(os.path.abspath(f"./libmathlib{ext}"))

lib.add_ints.argtypes = [ctypes.c_int32, ctypes.c_int32]
lib.add_ints.restype = ctypes.c_int32
lib.double_array.argtypes = [ctypes.POINTER(ctypes.c_int32), ctypes.c_size_t]
lib.double_array.restype = None

print("--- PART 1: Batch Array Doubling (N = 10,000,000) ---")
N_BATCH = 10_000_000

py_list = list(range(N_BATCH))
t0 = time.perf_counter()
py_list = [x * 2 for x in py_list]
py_batch = time.perf_counter() - t0

np_arr = np.arange(N_BATCH, dtype=np.int32)
c_ptr = np_arr.ctypes.data_as(ctypes.POINTER(ctypes.c_int32))
t0 = time.perf_counter()
lib.double_array(c_ptr, N_BATCH)
ctypes_batch = time.perf_counter() - t0

np_arr2 = np.arange(N_BATCH, dtype=np.int32)
t0 = time.perf_counter()
np_arr2 *= 2
numpy_batch = time.perf_counter() - t0

print(f"Pure Python loop : {py_batch * 1000:8.2f} ms")
print(f"ctypes C loop    : {ctypes_batch * 1000:8.2f} ms ({py_batch / ctypes_batch:.1f}x faster)")
print(f"NumPy in-place   : {numpy_batch * 1000:8.2f} ms ({py_batch / numpy_batch:.1f}x faster)\n")

print("--- PART 2: FFI Boundary Overhead (N = 1,000,000 small calls) ---")
N_CALLS = 1_000_000

t0 = time.perf_counter()
total = 0
for i in range(N_CALLS):
    total += i + 1
py_loop = time.perf_counter() - t0

t0 = time.perf_counter()
total = 0
for i in range(N_CALLS):
    total = lib.add_ints(total, 1)
ctypes_loop = time.perf_counter() - t0

print(f"Pure Python loop   : {py_loop * 1000:8.2f} ms")
print(f"ctypes inside loop : {ctypes_loop * 1000:8.2f} ms ({ctypes_loop / py_loop:.1f}x SLOWER)")
