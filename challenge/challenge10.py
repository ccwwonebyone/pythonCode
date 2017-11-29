a = []
def nextNum(num):
    j = 0
    k = 0
    re = ''
    num = str(num)
    for i in range(len(num)):
        if k == 0:
            k = int(num[i])
            j += 1
        elif k == int(num[i]):
            j += 1
        else:
            re += str(j)+str(k)
            k = int(num[i])
            j = 1
        if i == len(num)-1:
            re += str(j)+str(k)
    return int(re)
info = 1
for i in range(30):
    info = nextNum(info)
    if i == 29:
        print(len(str(info)))