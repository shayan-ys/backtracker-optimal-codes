import numpy as np
import itertools
from datetime import datetime

PRINT_BENCHMARKS = True

"""
Version 2.1
Instead of writing the Hamming distance in the table, just a boolean which says it's >= d or not.
Benchmark:
n=8,  d=4: 0:00:00.050291 - correct answer: 16
n=9,  d=4: 0:01:16.085821 - correct answer: 20
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

    if PRINT_BENCHMARKS:
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


def backtrack(code: list, candidates: list, level: int=0) -> (int, list):
    global hamming_distance_table, codes_list, promised_M, leading_bit_non_zero, q

    for lexi_index, word in enumerate(candidates[level]):

        hamming_distance_list_for_word = hamming_distance_table[word]

        if level == 0:
            code = [word]
        else:
            if len(code) <= level:
                code.append(word)
            else:
                code[level] = word

        if not leading_bit_non_zero[word] and level >= (promised_M / q):
            codes_list.append(code)
            return level + 1, code

        if level + 1 >= promised_M:
            codes_list.append(code)
            return level + 1, code

        if len(candidates) <= level + 1:
            candidates.append([])
        else:
            candidates[level + 1] = []

        for candidate_for_word in candidates[level][lexi_index:]:

            if hamming_distance_list_for_word[candidate_for_word]:
                candidates[level + 1].append(candidate_for_word)

        if level + 1 + len(candidates[level + 1]) < promised_M:
            codes_list.append(code)
            return level + 1, code

        found_level, found_code = backtrack(code, candidates, level+1)

        if found_level >= promised_M:
            return found_level, found_code

    return level


timer = datetime.now()
q = 2

n = 9
d = 3
promised_M = 40

"""
Generates all vectors and sort them by their weight -> all possible binary numbers in lexicographical order
"""
vectors = sorted(generate_all_vectors(n, q), key=np.count_nonzero)

leading_bit_non_zero = {lexi_index: (vector[0] != 0) for lexi_index, vector in enumerate(vectors)}
# print(leading_bit_non_zero)

print([str(i) + ': ' + ''.join(map(str, vector)) for i, vector in enumerate(vectors)])

"""
Pre-Computing hamming distance satisfaction table, just store if two vectors have a distance more than d or not.
"""
hamming_distance_table = generate_hamming_distance_table(vectors, d)

codes_list = []
init_candidates = list(range(len(vectors)))     # list of vectors indexes from 'vectors' lexi-sorted list.

max_found_M, best_code_vector_indexes = backtrack([], [init_candidates])

# max_found_M = 0
# best_code_vector_indexes = []
# for found_code in codes_list:
#
#     if len(found_code) > max_found_M:
#         best_code_vector_indexes = found_code
#         max_found_M = len(best_code_vector_indexes)
print('=== For n=' + str(n) + ' and d=' + str(d) + ' in GF(' + str(q) + '):')
print('max found M is: ' + str(max_found_M))
print('code is: ' + str([''.join(map(str, vectors[i])) for i in best_code_vector_indexes]))

if PRINT_BENCHMARKS:
    print('----------------------- process took: ' + str(datetime.now() - timer) + ' time ----')
