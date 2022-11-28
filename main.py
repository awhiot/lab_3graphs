from datetime import datetime
import tracemalloc
import numpy as np


def parse_matrix(name):
    with open(name, 'r') as f:
        lst = f.readlines()
    m = [[int(i) for i in k.split()] for k in lst]
    return m


def to_np(m, _lines, _cols):
    m_new = np.arange(_lines * _cols).reshape(_lines, _cols)
    for i in range(0, _cols):
        for j in range(0, _lines):
            m_new[i][j] = m[i][j]
    return m_new


def get_diagonals(m, _lines, _cols, _default_val):
    d_rd = {}
    d_ld = {}
    d_lu = {}
    d_ru = {}
    if m[0][0] != _default_val:
        d_rd[0] = m.diagonal()
    if m[_cols-1][0] != _default_val:
        d_ru[0] = np.fliplr(m).diagonal()
    for i in range(1, _cols-1):
        is_diagonal = True
        j = 0
        k = i
        while k < _cols and j < _lines:
            if m[j][k] == _default_val:
                is_diagonal = False
                break
            else:
                pass
            k += 1
            j += 1
        if is_diagonal:
            d_rd[i] = m.diagonal(i)
        else:
            is_diagonal = True
            k = i
            j = 0
            while k >= 0 and j < _lines:
                if m[j][k] == _default_val:
                    is_diagonal = False
                    break
                k -= 1
                j += 1
            if is_diagonal:
                d_ld[i] = np.fliplr(m).diagonal(_cols-1-i)
    for i in range(1, _cols-1):
        is_diagonal = True
        j = _lines-1
        k = i
        while k < _cols and j >= 0:
            if m[j][k] == _default_val:
                is_diagonal = False
                break
            k += 1
            j -= 1
        if is_diagonal:
            d_ru[i] = np.fliplr(m).diagonal(-i)
        else:
            is_diagonal = True
            k = i
            j = _lines-1
            while k >= 0 and j >= 0:
                if m[j][k] == _default_val:
                    is_diagonal = False
                    break
                k -= 1
                j -= 1
            if is_diagonal:
                temp = np.fliplr(np.flipud(m)).diagonal(_cols-i-1)
                temp2 = []
                for k in range(len(temp)):
                    temp2.append(temp[len(temp)-k-1])
                d_lu[i] = temp2
    return d_rd, d_ld, d_ru, d_lu


def move_diagonals(diagonal):
    temp = diagonal[0]
    temp_ar = []
    for i in range(1, len(diagonal)):
        temp_ar.append(diagonal[i])
    temp_ar.append(temp)
    new_diagonal = np.array(temp_ar)
    return new_diagonal


def create_matrix(_lines, _cols, d_rd, d_ld, d_ru, d_lu):
    new_matrix = np.zeros(_lines*_cols).reshape(_lines, _cols)
    for key in d_rd:
        if len(d_rd[key]) == 0:
            break
        j = 0
        i = key
        k = 0
        while i < _cols and j < _lines:
            new_matrix[j][i] = d_rd[key][k]
            i += 1
            j += 1
            k += 1
    for key in d_ld:
        if len(d_ld[key]) == 0:
            break
        j = 0
        i = key
        k = 0
        while i >= 0 and j < _lines:
            new_matrix[j][i] = d_ld[key][k]
            i -= 1
            j += 1
            k += 1
    for key in d_ru:
        if len(d_ru[key]) == 0:
            break
        j = _lines-1
        i = key
        k = 0
        while i < _cols and j >= 0:
            new_matrix[j][i] = d_ru[key][len(d_ru[key])-k-1]
            i += 1
            j -= 1
            k += 1
    for key in d_lu:
        if len(d_lu[key]) == 0:
            break
        j = _lines-1
        i = key
        k = 0
        while i >= 0 and j >= 0:
            new_matrix[j][i] = d_lu[key][len(d_lu[key])-k-1]
            i -= 1
            j -= 1
            k += 1
    return new_matrix


def print_matrix(m):
    print("Matrix:")
    for i in range(0, len(m)):
        print(m[i])


file_name = 'matrix10k.txt'
default_val = 0
start_time = datetime.now()
matrix = parse_matrix(file_name)
lines = len(matrix)
cols = len(matrix[lines - 1])
matrix = to_np(matrix, lines, cols)
#print_matrix(matrix)
tracemalloc.start(1)
d_rd, d_ld, d_ru, d_lu = get_diagonals(matrix, lines, cols, default_val)
for key in d_rd:
    d_rd[key] = move_diagonals(d_rd[key])
for key in d_ld:
    d_ld[key] = move_diagonals(d_ld[key])
for key in d_ru:
    d_ru[key] = move_diagonals(d_ru[key])
for key in d_lu:
    d_lu[key] = move_diagonals(d_lu[key])
print('Mem: ', round(tracemalloc.get_traced_memory()[1] / 1024 / 1024, 2), 'MB')
new_matrix = create_matrix(lines, cols, d_rd, d_ld, d_ru, d_lu)
final_time = datetime.now()-start_time
#print_matrix(new_matrix)
