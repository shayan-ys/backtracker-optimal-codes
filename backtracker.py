import numpy as np
import itertools
from datetime import datetime


"""
Version 2.0
Pre-computing a hamming distance table, and work with integer indexes of the table instead of actual words.
Instead of calculating the hamming distance for each word during backtracking, simply looking in the 2D table.
Benchmark:
n=10, d=4: 0:00:04.071968 - with wrong result: 36, correct is 40
n=11, d=4: 0:00:31.644406 - correct answer: 72
n=12, d=4: 0:05:14.170399 - correct answer: 144
"""


def hamming_distance(vector_1: np.array, vector_2: np.array) -> int:
    return np.count_nonzero(vector_1 != vector_2)


def generate_all_vectors(length: int) -> list:
    """
    Creates all possible binary numbers with length n, and casts them to np.array
    :param length: n
    :return: list of np.arrays representing all possible binary numbers of length n
    """
    return list(map(np.array, itertools.product([0, 1], repeat=length)))


def generate_hamming_distance_table(vector_list: list) -> list:
    """
    Generate a hamming distance table with integer indexes as in the input vectors list
    :param vector_list: List of vectors
    :return: Hamming distance of vectors (in order with integer indexes)
    """
    distance_table = []

    for needle_index, vector_needle in enumerate(vector_list):

        distance_table.append([])
        for in_stack_index, vector_in_stack in enumerate(vector_list):

            if needle_index == in_stack_index:
                distance = 0
            elif needle_index > in_stack_index:
                distance = distance_table[in_stack_index][needle_index]
            else:
                distance = hamming_distance(vector_needle, vector_in_stack)

            distance_table[needle_index].append(distance)

    return distance_table


def backtrack(code: list, candidates: list, level: int=1) -> list:
    global hamming_distance_table

    for lexi_index, word in enumerate(candidates):

        hamming_distance_list_for_word = hamming_distance_table[word]

        if level == 1:
            code = [word]
        else:
            word_satisfy_minimum_distance_of_code = True
            for codeword in reversed(code):
                if hamming_distance_list_for_word[codeword] < d:
                    word_satisfy_minimum_distance_of_code = False
                    break
            if not word_satisfy_minimum_distance_of_code:
                continue
            code.append(word)

        candidates_for_current_word = []
        for candidate_for_word in candidates[lexi_index:]:

            if hamming_distance_list_for_word[candidate_for_word] >= d:
                candidates_for_current_word.append(candidate_for_word)

        if not candidates_for_current_word:
            continue

        backtrack(code, candidates_for_current_word, level+1)

        if level == 1:
            codes_list.append(code)

    if level == 1 and not codes_list:
        codes_list.append(code)

    return code


timer = datetime.now()

n = 9
d = 4

"""
Generates all vectors and sort them by their weight -> all possible binary numbers in lexicographical order
"""
vectors = sorted(generate_all_vectors(n), key=np.count_nonzero)

# print(vectors)

distance_table_timer = datetime.now()
hamming_distance_table = generate_hamming_distance_table(vectors)
print('distance table pre-computation time: ' + str(datetime.now() - distance_table_timer))

# for row in hamming_distance_table:
#     print(row)

codes_list = []

backtrack([], list(range(len(vectors))))

max_found_M = 0

for found_code in codes_list:
    # print('M=' + str(len(found_code)) + ' -- ' + ', '.join(list(map(str, found_code))))
    max_found_M = max(len(found_code), max_found_M)

print('----------------------- process took: ' + str(datetime.now() - timer) + ' time ----')
print('max found M is: ' + str(max_found_M))
