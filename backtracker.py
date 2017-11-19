import numpy as np
import itertools
from datetime import datetime


"""
Version 1.0
In this version, all vectors created and sorted by their lexicographical order, then backtracking algorithm 
runs over the first generation (which is all the vectors) and all possible codes will be created.
Benchmark:
n=10, d=4: 0:01:06.279316 - with wrong result: 36, correct is 40
n=11, d=4: around 7 minutes - correct answer: 72
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


def is_np_array_satisfy_distance_in_list(needle: np.array, list_arrays: list, required_distance: int,
                                         reversed_search=False) -> bool:
    """
    Search through the list of words and check if the needle has minimum distance of d from all of them
    :param needle: given vector we want to check if has minimum distance with all members of the list
    :param list_arrays: given list of vectors
    :param required_distance: d
    :param reversed_search: if True, search from end of the list
    :return:
    """
    needle_weight = np.count_nonzero(needle)
    if reversed_search:
        list_arrays_iterator = reversed(list_arrays)
    else:
        list_arrays_iterator = list_arrays

    for word in list_arrays_iterator:
        word_weight = np.count_nonzero(word)
        if abs(word_weight - needle_weight) <= required_distance:
            # if larger no need for calculating Hamming distance, definitely satisfies
            if word_weight == needle_weight and np.array_equal(word, needle):
                return False
            if hamming_distance(word, needle) < required_distance:
                return False
    return True


def backtrack(code: list, candidates: list, level: int=1) -> list:
    for lexi_index, word in enumerate(candidates):

        if level == 1:
            code = [word]
        else:
            if not is_np_array_satisfy_distance_in_list(word, code, required_distance=d, reversed_search=True):
                continue
            code.append(word)

        candidates_for_current_word = []
        for candidate_for_word in candidates[lexi_index:]:

            if hamming_distance(word, candidate_for_word) >= d:
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

n = 10
d = 4

"""
Generates all vectors and sort them by their weight -> all possible binary numbers in lexicographical order
"""
vectors = sorted(generate_all_vectors(n), key=np.count_nonzero)

# print(vectors)

codes_list = []

backtrack([], vectors)

max_found_M = 0

for found_code in codes_list:
    # print('M=' + str(len(found_code)) + ' -- ' + ', '.join(list(map(str, found_code))))
    max_found_M = max(len(found_code), max_found_M)

print('----------------------- process took: ' + str(datetime.now() - timer) + ' time ----')
print('max found M is: ' + str(max_found_M))
