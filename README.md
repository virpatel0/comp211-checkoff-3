# How Python Libraries Are Implemented in C (COMP 211 Checkoff 3)

## Overview
An exploration into how CPython represents dynamic objects under the hood and how high-performance Python libraries (like NumPy) achieve near-native C execution speed.

## Key Discoveries
1. **Everything is a `PyObject*`:** Every Python object lives on the heap as a C struct starting with a reference count (`ob_refcnt`) and a type pointer (`ob_type`). Specific types embed `PyObject` at byte offset 0 to simulate inheritance in C.
2. **Pointer Chasing vs. Contiguous Buffers:** A Python `list` is an array of `PyObject*` pointers scattered across the heap, causing CPU cache misses and per-element type checks. NumPy wraps one `PyObject` header around a raw C pointer (`char *data`) to a contiguous block of unboxed primitives.
3. **Dynamic Linking via `ctypes`:** Standard C code compiled into a position-independent shared library (`-fPIC -shared`) can be loaded into Python's address space via `dlopen()` (`ctypes.CDLL`).
4. **The Golden Rule of FFI (Amortize the Crossing):** Calling a tiny C function inside a Python loop is *slower* than pure Python due to `libffi` stack-building and type-marshaling overhead (~150–400 ns per call). High performance requires pushing the loop into C.

## How to Run the Code
Requires `gcc` (or `clang`) and Python 3 with `numpy` installed (`pip install numpy`).

```bash
cd code

# Compile the C shared library:
# Linux:
gcc -O3 -fPIC -shared mathlib.c -o libmathlib.so
# macOS:
clang -O3 -fPIC -shared mathlib.c -o libmathlib.dylib
# Windows (MinGW):
gcc -O3 -shared mathlib.c -o mathlib.dll

# Run the basic ctypes example and performance benchmarks:
python3 run_ctypes.py
python3 benchmark.py
