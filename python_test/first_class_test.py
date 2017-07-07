
def square(x):
    return x * x

def my_map(func, arg_list):
    result = []
    for i in arg_list:
        result.append(func(i))
    return result

num_list = [1, 2, 3, 4, 5]

squares = my_map(square, num_list)

print(squares)
