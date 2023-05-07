# 获取中位数    
def median(x):
    length = len(x)
    x.sort()
    if (length % 2)== 1:
        z=length // 2
        y = x[z]
    else:
        y = (x[length//2]+x[length//2-1])/2
    return y


l = '17000.0,13500.0,9000.0,12500.0,15000.0,20000.0,11500.0,17000.0,22500.0,15000.0,9000.0,12500.0,'
z = list(eval(l))
print(median(z))
