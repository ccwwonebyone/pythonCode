import pickle
pkl_file = open('banner.p', 'rb')
data = pickle.load(pkl_file)
str = '\n'.join([''.join([p[0] * p[1] for p in row]) for row in data])
f = open('banner.txt','w+')
f.write(str)
f.close()