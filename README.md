# backtracker-optimal-codes
Finding Optimal Codes using Backtracking algorithm

## Goal
To find the best code (hopefully the optimal code) for the given n (as length of codewords) and d (as the minimum distance of codewords)

## Aproach
Backtracking algorithm find candidates for a given codeword, and add candidates which satisfies the minimum distance to the code
And goes on as a ++recursive++ algorithm.

## Structure
Each vector in GF(2) universe is a np_array of length n.
