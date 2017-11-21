import numpy as np
import itertools
import sys
from datetime import datetime

PRINT_BENCHMARKS = True
PRINT_OUTPUT = True
FILE_OUTPUT = False

"""
Version 2.1
Instead of writing the Hamming distance in the table, just a boolean which says it's >= d or not.
Benchmark:
n=8,  d=4: 0:00:00.050291 - correct answer: 16
n=9,  d=4: 0:01:07.503750 - correct answer: 20
"""


def hamming_distance(vector_1: np.array, vector_2: np.array) -> int:
    return np.count_nonzero(vector_1 != vector_2)


def generate_all_vectors(length: int, q: int=2) -> list:
    """
    Creates all possible binary numbers with length n, and casts them to np.array
    :param length: n
    :param q: value for GF, if 2 binary codes only 0 or 1 are valid bits
    :return: list of np.arrays representing all possible binary numbers of length n
    """
    return list(map(np.array, itertools.product(list(range(q)), repeat=length)))


def generate_hamming_distance_table(vector_list: list, minimum_distance: int, print_result: bool=False) -> list:
    """
    Generate a hamming distance table with integer indexes as in the input vectors list, and a Boolean value
    Based on if they satisfy the given minimum distance or not.
    :param vector_list: List of vectors
    :param minimum_distance: Each two vectors that are 'minimum_distance' away from each other will be flagged as 'True'
    :param print_result: Print the table in the end.
    :return: Hamming distance of vectors (in order with integer indexes)
    """
    global PRINT_BENCHMARKS
    distance_table_timer = datetime.now()

    distance_table = []

    for needle_index, vector_needle in enumerate(vector_list):

        distance_table.append([])
        for in_stack_index, vector_in_stack in enumerate(vector_list):

            if needle_index == in_stack_index:
                is_distance = False
            elif needle_index > in_stack_index:
                is_distance = distance_table[in_stack_index][needle_index]
            else:
                is_distance = hamming_distance(vector_needle, vector_in_stack) >= minimum_distance

            distance_table[needle_index].append(is_distance)

    if PRINT_BENCHMARKS and PRINT_OUTPUT:
        print('--- distance table pre-computation time: ' + str(datetime.now() - distance_table_timer))

    if print_result:
        for row in distance_table:
            print(row)

    return distance_table


def lexi_sorter(vectors_list: list) -> list:
    return sorted(vectors_list, key=np.count_nonzero)


def is_word_satisfy_minimum_distance_of_code(code: list, hamming_distance_list_for_word: list) -> bool:
    for codeword in reversed(code):
        if not hamming_distance_list_for_word[codeword]:
            return False
    return True


def backtrack(level: int=0) -> (int, list):
    global code, candidates, hamming_distance_table, codes_list, promised_M, leading_bit_non_zero, q

    for lexi_index, word in enumerate(candidates[level]):

        hamming_distance_list_for_word = hamming_distance_table[word]

        if len(code) <= level:
            code.append(word)
        else:
            code[level] = word

        if not leading_bit_non_zero[word] and level >= (promised_M / q):
            codes_list.append(code)
            return level, code

        if level + 1 >= promised_M:
            codes_list.append(code)
            return level, code

        if len(candidates) <= level + 1:
            candidates.append([])
        else:
            candidates[level + 1] = []

        for candidate_for_word in candidates[level][lexi_index:]:

            if hamming_distance_list_for_word[candidate_for_word]:
                candidates[level + 1].append(candidate_for_word)

        if level + 1 + len(candidates[level + 1]) < promised_M:
            codes_list.append(code)
            return level, code

        found_level, found_code = backtrack(level+1)

        if found_level + 1 >= promised_M:
            return found_level, found_code

    return level


timer = datetime.now()
q = 2

n = 8
d = 4
promised_M = 16

try:
    n = int(sys.argv[1])
except:
    pass
try:
    d = int(sys.argv[2])
except:
    pass
try:
    promised_M = int(sys.argv[3])
except:
    pass

"""
Generates all vectors and sort them by their weight -> all possible binary numbers in lexicographical order
"""
vectors = sorted(generate_all_vectors(n, q), key=np.count_nonzero)

leading_bit_non_zero = {lexi_index: (vector[0] != 0) for lexi_index, vector in enumerate(vectors)}
# print(leading_bit_non_zero)

detailed_outputs = []
critical_outputs = []
if PRINT_OUTPUT:
    print(str([str(i) + ': ' + ''.join(map(str, vector)) for i, vector in enumerate(vectors)]))

"""
Pre-Computing hamming distance satisfaction table, just store if two vectors have a distance more than d or not.
"""
hamming_distance_table = generate_hamming_distance_table(vectors, d)

init_candidates = list(range(len(vectors)))     # list of vectors indexes from 'vectors' lexi-sorted list.

codes_list = []
code = []
candidates = [init_candidates]

max_found_M, best_code_vector_indexes = backtrack()

critical_outputs.append('=== For n=' + str(n) + ' and d=' + str(d) + ' in GF(' + str(q) + '):')
detailed_outputs.append(critical_outputs[-1])
critical_outputs.append('max found M is: ' + str(max_found_M + 1))
detailed_outputs.append(critical_outputs[-1])
detailed_outputs.append('code is: ' + str([''.join(map(str, vectors[i])) for i in best_code_vector_indexes]))

if PRINT_BENCHMARKS:
    critical_outputs.append('----------------------- process took: ' + str(datetime.now() - timer) + ' time ----')
    detailed_outputs.append(critical_outputs[-1])

file = None
if FILE_OUTPUT:
    file = open("output_backtracker.txt", "w")
for line in detailed_outputs:
    if PRINT_OUTPUT:
        print(line)
    if FILE_OUTPUT:
        file.write(line)
        file.write('\n')
if not PRINT_OUTPUT:
    for line in critical_outputs:
        print(line)
if FILE_OUTPUT:
    file.close()
