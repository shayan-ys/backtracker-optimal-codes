# Backtracker-Optimal-Codes
Finding **Optimal Codes** using **Backtracking** algorithm

## Goal
To find the best code (hopefully the optimal code) for the given n (as length of codewords) and d (as the minimum distance of codewords)

## Approach
- Starting from null codeword, and all q^n (all possible vectors in GF(q)).
- The recursive function `backtrack()` iterates over each candidate (in level i) and find candidates (in next level=i+1) for each word in level i.
- If terminating conditions doesn't apply, call `backtrack()` for the new candidates (level i+1).
- Return value of the `backtrack()` function is the max number of codes found in this branch and the code (list of codewords) of that code.
    - Therefor the return value of `backtrack()` in level=0 will be the found result which is the best code among all possible combination of vectors.
### Terminating conditions:
assuming level starts from 1:
- Level number (starting from 1) is the number of codewords found so far, so if level >= promised_M it means it already found a code with promised number of codewords.
- Number of codewords found so far, plus number of next level candidates is less than promised_M. This means even if all candidates have minimum distance of d with each other (i.e. all candidates are actually codewords for the current code) still this branch won't reach the promised_M number of codewords.
- If current word is **starting with non-zero bit**, and current level (i.e. number of codewords found so far) is greater or equal to (M / q) + 1.
     `level >= (promised_M / q) + 1`

## Structure
- Each vector with length n in GF(q) universe is an np_array of length n.
- All vectors is stored in a list sorted based on lexicographical order (vectors with less weight comes first)
- A 2-D list, stores the Hamming distance of each pair of vectors.
- But instead of storing the Hamming distance number, a boolean is saved showing if two vectors Hamming distance is greater than 'd' or not.
    - Reason is, we only wants to know if two vectors are far away enough or not (based on their Hamming distance)
    - It doesn't seem to be an noticeable improvement, but for lengthy codes the number of recursive calls and number of comparison is astronomical.
- In the backtracking method, instead of using the actual vectors (as np_arrays or bit-strings), their index in lexicographical sorted list is used.
    - Reason is searching through a list (by index) is much faster than searching through a key-value dictionary by key.
    - The order of search in list by index is **O(log(n))** (i.e. n is length of the list) but key-value dictionary with string keys is **O(n)**.

## Benchmarks:
Check [Latest Release](https://github.com/shayan-ys/backtracker-optimal-codes/releases) for up-to-date benchmarks.

# Copyright
Author: Shayan Yousefian - sy17sq@brocku.ca
For the: "Coding Theory" 1P02 Course Assignment - by Prof. Sheridan Houghten - Brock University, Ontario, Canada
