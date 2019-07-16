# 数字日期和时间
from decimal import Decimal, localcontext
import cmath
from fractions import Fraction
import numpy as np
import random
from datetime import timedelta, datetime
print('======3.1========')
'''
内置函数round(value, ndigits)对浮点数的四舍五入操作
ndigits 参数可以是负数，这种情况下， 舍入运算会作用在十位、百位、千位等上面
'''
a = 1627731
print(round(a, -1))
print(round(a, -2))
print(round(a, -3))

print('======3.2========')
'''
执行精确的浮点运算(并能容忍一定的性能损耗)，你可以使用 decimal 模块
普通的浮点运算能提供17位的精度，decimal模块主要还是用于金融领域的精度计算。
'''
a = 4.2
b = 2.1
print(a + b)
print((a + b) == 6.3)

a = Decimal('4.2')
b = Decimal('2.1')
print(a + b)
print((a + b) == Decimal('6.3'))

a = Decimal('1.3')
b = Decimal('1.7')
c = a / b
print(c)
with localcontext() as ctx:
    ctx.prec = 3
    print(a / b)
with localcontext() as ctx:
    ctx.prec = 50
    print(a / b)


print('======3.4========')
'''
二八十六进制整数互相转化
'''
x = 1234
# 带前缀的输出
print('binary = ', bin(x))
print('octonary = ', oct(x))
print('hexadecimal = ', hex(x))

# 不带前缀的输出
print('binary = ', format(x, 'b'))
print('octonary = ', format(x, 'o'))
print('hexadecimal = ', format(x, 'x'))

# 其他进制转换成十进制
print(int('4d2', 16))

print('======3.6========')
# 复数的运算 complex(real, imag)
a = complex(3, 5)
print(a)
b = 3 + 5j
print(b)

print('a + b = ', a + b)
print('a * b = ', a * b)
print('a / b = ', a / b)
print('abs(a) = ', abs(a))  # abs绝对值

'''
执行其他的复数函数 正弦 余弦  平方根使用cmath模块
'''
print(cmath.sin(30 * cmath.pi / 180))
print(cmath.cos(30 * cmath.pi / 180))
print(cmath.sqrt(-1))

# 分数运算
a = Fraction(1, 5)
b = Fraction(3, 5)
print(a + b)
print(a * b)
print('a 的分母: ', a.denominator)
print('a 的分子: ', a.numerator)
print(float(a))

print('======3.9========')
'''
大型数组运算 numpy
'''

x = [1, 2, 3, 4]
y = [5, 6, 7, 8]
print(x * 2)  # 并不是列表的数学运算
print(x + y)  # 并不是两个列表的数学运算

ax = np.array([1, 2, 3, 4])
ay = np.array([5, 6, 7, 8])
print(ax * 2)  # 数组的数学运算 [2, 4, 6, 8]
print(ax + ay)  # output: [ 6  8 10 12]
print(ax + 10)  # output: [11 12 13 14]


print('======3.10========')
'''
矩阵与线性代数运算
'''
m = np.array([[1, -2, 3], [0, 4, 5], [7, 8, -9]])
print(m)

print('======3.11========')
'''
随机选择
'''
values = [1, 2, 3, 4, 5, 6]
print(random.choice(values))  # 从序列中随机选择一个数

print(random.sample(values, 3))  # 从序列中随机抽样

random.shuffle(values)  # 打乱序列的顺序
print(values)

print(random.randint(0, 10))  # 生成随机整数

print(random.random())  # 生成0到1范围内均匀分布的浮点数

print(random.getrandbits(200))  # 获取N位随机位(二进制)的整数

'''
random模块还包含基于均匀分布、高斯分布和其他分布的随机数生成函数。 比如， random.uniform() 计算均匀分布随机数， random.gauss() 计算正态分布随机数
'''

print('======3.12========')
'''
基本的日期与时间转换
执行不同时间单位的转换和计算，请使用 datetime 模块
'''
a = timedelta(days=2, hours=6)
b = timedelta(hours=4.5)
c = a + b
print('days = ', c.days)
print('seconds = ', c.seconds)
print('hours = ', c.seconds / 3600)
print('total_hours = ', c.total_seconds() / 3600)


a = datetime(2019, 6, 24)
print(a + timedelta(days=10))

print(datetime.now())
