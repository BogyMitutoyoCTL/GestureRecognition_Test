import numpy as np
from collections import deque

points = deque(maxlen=20)

for i in range(1, 11):
    points.appendleft((i, i+3))
    
x=[]
y=[]

for i in np.arange(1,11):
    if points[-i] is not None:
        x +=[points[-i][0]]
        y +=[points[-i][1]]
    else:
        print('test')


m,b = np.polyfit(x,y,1)

print(str(m) + "x + " + str(b)) 
