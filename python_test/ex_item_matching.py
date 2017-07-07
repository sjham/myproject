
def return_test():
    a = [1,2,3,4,5,6,1,2,3,4,5,6,1,2,3,4,5,6]
    f =[]
    f.append(a[0])
    #print(a[0])
    for i in a[1:]:
        if i == a[0]:
            break
        else:
            f.append(i)
            #print(a[0])

    print(f)
    #
    # for t in i:
    #     print(t)
    #
#
#     b = [2,3,4,5,6,7,7,7,7,7]
#     c = []
#     d = []
#     for i in b:
#         c.append(i)
#     for i in a:
#         d.append(i)
#         if c[-1] == d[-1]:
#             break
#     print(d)
#
#
# t = [1,2,3,4,5,6,7,7,7,7]
# def unique(a):
#     list_iter = iter(a)
#     print(list_iter)
#     prev = list_iter.next()
#     print(prev)
#     for item in list_iter:
#         if item != prev:
#             yield prev
#             prev = item
#     yield prev
#
#     for i in prev:
#         print(i)

if __name__ == '__main__':
    #return_test()
    return_test()
