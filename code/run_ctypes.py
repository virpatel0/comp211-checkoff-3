import ctypes
import os
import platform

# Load the compiled shared library based on OS
ext = ".dylib" if platform.system() == "Darwin" else ".dll" if platform.system() == "Windows" else ".so"
lib = ctypes.CDLL(os.path.abspath(f"./libmathlib{ext}"))

# 1. Simple integer addition
lib.add_ints.argtypes = [ctypes.c_int32, ctypes.c_int32]
lib.add_ints.restype = ctypes.c_int32
print("15 + 27 =", lib.add_ints(15, 27))

# 2. Mutating a contiguous C array in-place via pointer
lib.double_array.argtypes = [ctypes.POINTER(ctypes.c_int32), ctypes.c_size_t]
lib.double_array.restype = None

IntArray4 = ctypes.c_int32 * 4
c_arr = IntArray4(1, 2, 3, 4)
lib.double_array(c_arr, len(c_arr))
print("Doubled array:", list(c_arr))
