from datetime import datetime,date
#he ain't the youngest, he is the second  不是最年轻的 说明是倒数 第二个
#todo: buy flowers for tomorrow 明天所以结果是 1756-01-27
for i in range(1006,2006,10):
    if i % 4 == 0:
        dayOfWeek = datetime.strptime(str(i)+'0126',"%Y%m%d").weekday()
        if dayOfWeek == 0:
            print(i)