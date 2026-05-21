import numpy as np
# arr = np.linspace(-6, 21, 60, endpoint=False)
# step = arr[1] - arr[0]
# # Округление до двух знаков после точки
# step_rounded = round(step, 2)
# print(arr)
# print(step_rounded)

import numpy as np
# mystery = np.array([[-13586,  15203,  28445, -27117,  -1781, -17182, -18049],
#        [ 25936, -30968,  -1297,  -4593,   6451,  15790,   7181],
#        [ 13348,  28049,  28655,  -6012,  21762,  25397,   8225],
#        [ 13240,   7994,  32592,  20149,  13754,  11795,   -564],
#        [-21725,  -8681,  30305,  22260, -17918,  12578,  29943],
#        [-16841, -25392, -17278,  11740,   5916,    -47, -32037]],
#       dtype=np.int16)
# elem_5_3 = mystery[5,3]
# print(elem_5_3)

# # 2. Элемент из последней строки последнего столбца
# last = mystery[-1, -1]
# print(last)

# # 3. Строка 4 (индекс 4)
# line_4 = mystery[4]
# print(line_4)

# # 4. Предпоследний столбец (индекс -2)
# col_2 = mystery[:, -2]
# print(col_2)

# # 5. Из строк 2-4 (включительно) получить столбцы 3-5 (включительно)
# # Строки: индексы 2, 3, 4; Столбцы: индексы 3, 4, 5
# part = mystery[2:5, 3:6]
# print(part)

# # 6. Последний столбец в обратном порядке
# rev = mystery[:, -1][::-1]
# print(rev)

# # 7. Транспонированный массив
# trans = mystery.T
# print(trans)

# a = np.array([23, 34, 27])
# b = np.array([-54, 1, 46])
# c = np.array([46, 68, 54])

# print(a, b, c)
# print(a+b, b+c, a+c)

# k = c / a  # [2. 2. 2.]
# print(f"Коэффициент: {k}")
# if np.all(k == k[0]) and k[0] > 0:
#     print("Векторы a и c сонаправлены")
# print()    
# dist_ab = np.linalg.norm(a - b)
# dist_ac = np.linalg.norm(a - c)
# dist_bc = np.linalg.norm(b - c)

# print(f"Расстояние a-b: {dist_ab:.2f}")  # 85.90
# print(f"Расстояние a-c: {dist_ac:.2f}")  # 49.13
# print(f"Расстояние b-c: {dist_bc:.2f}")  # 120.64
# print()
# dot_ab = np.dot(a, b)  # 34
# dot_ac = np.dot(a, c)  # 4828
# dot_bc = np.dot(b, c)  # 68

# print(f"a·b = {dot_ab}")
# print(f"a·c = {dot_ac}")
# print(f"b·c = {dot_bc}")

# Проверка на ноль
# if dot_ab == 0:
#     print("a и b")
# elif dot_ac == 0:
#     print("a и c")
# elif dot_bc == 0:
#     print("b и c")
# else:
#     print("Нет перпендикулярных векторов среди заданных")
# array = np.random.randint(6, 12, size=(3,3))
# print(array)

# np.random.seed(100)
# print(np.random.randint(10, size=3))
# # [8 8 3]
# print(np.random.randint(10, size=3))
# # [7 7 0]
# print(np.random.randint(10, size=3))
# # [4 2 5]

import pandas as pd
pd.__version__
