#
# from datetime import datetime
# import time
#
#
# def date():
#     a = input("input: ")
#     b = time.strptime(a, "%Y,%m,%d")
#     print(b)
#
#
# date()
# #
# #
# # def square(x):
# #     return x * x
# #
# # def my_map(func, arg_list):
# #     result = []
# #     for i in arg_list:
# #         result.append(func(i))
# #     return result
#
def t(g=[]):
    num_list = [1, 2, 3, 4, 5]
    for i in num_list:
        g.append(i)
    return g

a = t([6,7,8,9])
print(a)
#
# squares = my_map(square, num_list)
#
# print(squares)
