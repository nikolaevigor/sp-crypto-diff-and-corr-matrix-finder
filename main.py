"""
using lists of tuples instead of dicts to preserve order
"""

from functools import reduce

from example_data import *


def convert_int_to_bin(num):
    """
    e.g.: return 5 as 0101
    """
    return bin(num)[2:].zfill(4)


def create_bin_list(range_start, range_end):
    """
    list of strings of all bins len 4
    """
    return [convert_int_to_bin(x) for x in range(range_start, range_end)]


def generate_y_vectors_combinations(y_vectors):
    """
    [('y1y2y3', [[111..01], [111..01], [111..01]]), ...]
    """
    vectors = create_bin_list(0, 16)
    output = []
    for vector in vectors:
        combination = []
        label = ''
        for i in range(0, len(vector)):
            if vector[i] == '1':
                label += 'y{}'.format(i+1)
                combination.append(y_vectors[i])
        if not label:
            label = '0'
        output.append((label, combination))
    return output


def summarize_combinations(y_vectors):
    output = []
    for label, combination in generate_y_vectors_combinations(y_vectors):
        sum_vector = [0 for _ in range(0, 16)]
        for y_vector in combination:
            sum_vector = [sum(x) % 2 for x in zip(y_vector, sum_vector)]
        output.append((label, sum_vector))
    return output


def transform_summarized(y_vectors):
    return [(label, transform_vector(vector)) for label, vector in summarize_combinations(y_vectors)]


def corr_matrix(y_set, v=False):
    output = []
    for label, vector in transform_summarized(y_set):
        res_4 = process_vector_recursively(vector)
        label = label if label else '0'
        if v:
            res_4.append(label)
        output.append(res_4)
    return output


def transform_vector(vector):
    """
    0 -> 1
    1 -> -1
    [0, 1, 0, 0, 1] -> [1, -1, 1, 1, -1]
    """
    return list(map(lambda x: 1 if x == 0 else -1, vector))


def process_vector(vector):
    """
    returns list
    first half is input vector divided by 2 and respectively summarized (1st half with 2nd)
    second half is same, but subtracted
    """
    output = []
    half_len = int(len(vector) / 2)
    for i in range(0, half_len):
        output.append(vector[i] + vector[i + half_len])
    for i in range(half_len, len(vector)):
        output.append(vector[i - half_len] - vector[i])
    return output


def process_vector_recursively(vector):
    """
    divide vector (by 1, 2, 4, 8, ... len(vector)/2), apply run function on all parts, concatenate
    repeat with next divisor until no all divisors processed
    """
    result = vector
    intervals_sequence_set = list(compose_intervals_sequence_set(len(vector)))[::-1]
    for intervals_sequence in intervals_sequence_set:
        local_result = [process_vector(result[interval[0]: interval[1]]) for interval in intervals_sequence]
        result = list(reduce(lambda x, y: x + y, local_result))
    return result


def compose_intervals_sequence_set(vector_len):
    """
    16 -> [2, 4, 8, 16] -> [ [(0, 2), ..., (14, 16)], [(0, 4), ..., (12, 16)], [(0, 8), (8, 16)], [(0, 16)] ]
    """
    interval_lengths = [x for x in range(2, vector_len + 1) if vector_len % x == 0]
    for x in interval_lengths:
        yield [(i, i + x) for i in range(0, vector_len, x)]


def diff_matrix(s_block):
    """
    a - offset
    b - mod
    """
    matrix = [[0 for _ in range(0, 16)] for _ in range(0, 16)]
    for a in range(0, 16):
        for b in range(0, 16):
            counter = 0
            for n in range(0, len(s_block)):
                p1 = s_block[n]
                p2 = s_block[n ^ a]
                if p1 ^ p2 == b:
                    counter += 1
            matrix[a][b] = counter
    return matrix

if __name__ == '__main__':
    print('\n<<< Разностная матрица / Diff matrix >>>\n')
    print(diff_matrix(s_block_1))
    print('\n<<< Корреляционная матрица / Correlation matrix >>>\n')
    print(corr_matrix(y_set_1))
