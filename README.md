# Compiler Optimizations & Why Python Libraries Are Written in C (COMP 211 Checkoff 3)

## Overview
For this project, I explored how C compiler optimizations (`-O0` vs. `-O2`/`-O3`) work under the hood and why high-performance Python libraries like NumPy and PyTorch implement their core math routines in C (the "two-language solution").

## Key Discoveries
1. **The "As-If" Rule & Compiler Passes:** Compilers like GCC translate C into an Intermediate Representation (IR) and aggressively rewrite code—using register allocation, loop-invariant code motion, strength reduction, and SIMD auto-vectorization—as long as the observable output remains identical.
2. **Pointer Aliasing & `restrict`:** Pointers can block optimizations if two pointers might reference the same memory address. Using C's `restrict` keyword guarantees non-overlapping memory, allowing `-O3` to vectorize loops.
3. **Why Pure Python Is Slow:** Python is *not* compiled with `-O0`; it is dynamically interpreted. A Python `list` is an array of heap pointers (`PyObject**`), meaning every loop iteration suffers from pointer chasing, runtime type checks, and 28-byte object overhead per integer.
4. **The Two-Language Solution (`ctypes` & Buffer Protocol):** Python acts as ergonomic "glue" at the top, while handing raw contiguous memory pointers (`double *`) to pre-compiled `-O2`/`-O3` C shared libraries for the heavy lifting.

## How to Run the Experiment
Compile the C code twice—once unoptimized (`-O0`) and once heavily optimized (`-O3`)—then run the Python benchmark:

```bash
gcc -O0 -shared -fPIC fast_math.c -o fast_math_O0.so
gcc -O3 -shared -fPIC fast_math.c -o fast_math_O3.so
python3 benchmark.py
