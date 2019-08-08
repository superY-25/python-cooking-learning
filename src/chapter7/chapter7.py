import html
from functools import partial
import math
print('=====7.1 可接受任意数量参数的函数=====')
'''
构造一个可接受任意数量参数的函数
为了能让一个函数接受任意数量的位置参数，可以使用一个 * 参数
为了接受任意数量的关键字参数，使用一个以 ** 开头的参数
'''


def avg(first, *rest):
    return (first + sum(rest)) / (1 + len(rest))


# rest是由所有其他位置参数组成的元组。然后我们在代码中把它当成了一个序列来进行后续的计算。
print(avg(1, 2, 3, 4, 5))


def make_element(name, value, **attrs):
    keyvals = ['%s="%s"' % item for item in attrs.items()]
    attr_str = ' '.join(keyvals)
    element = '<{name} {attrs}>{value}</{name}>'.format(
        name=name,
        attrs=attr_str,
        value=html.escape(value)
    )
    return element


# Creates '<item size="large" quantity="6">Albatross</item>'
print(make_element('item', 'Albatross', size='large', quantity=6))


# 如果你还希望某个函数能同时接受任意数量的位置参数和关键字参数，可以同时使用*和**
def anyargs(*args, **kwargs):
    print(args)  # a tuple
    print(kwargs)  # a dict


print('=====7.2 只接受关键字参数的函数=====')
"""
强制关键字参数放到某个*参数或者单个*后面就能达到这种效果
"""


def recv(maxsize, *, block):
    """Receives a message"""
    pass


# recv(1024, True)  # TypeError
recv(1024, block=True)  # Ok


def p():
    return 1, 2, 3


x, y, z = p()
print(x, y, z)

print('=====7.6 定义匿名或内联函数=====')

add = lambda x, y: x+y
print(add(2, 3))
# lambda表达式典型的使用场景是排序或数据reduce等
names = ['David Beazley', 'Brian Jones', 'Raymond Hettinger', 'Ned Batchelder']
print(sorted(names, key=lambda name: name.split()[-1].lower(), reverse=True))


print('=====7.7 匿名函数捕获变量值=====')
"""
用lambda定义了一个匿名函数，并想在定义时捕获到某些变量的值。
"""
x = 10
a = lambda y: x + y
x = 20
b = lambda y: x + y
print("a=", a(10), "b=", b(10))
"""
lambda表达式中x是自由变量，在运行时绑定值。所以x的值是以最后x的赋值进行计算。
若要捕获定义时的值，可以将参数定义成默认值
"""
x = 10
a = lambda y, x=x: x+y
x = 20
b = lambda y, x=x: x+y
print("a=", a(10), "b=", b(10))
# 还有一些常见的错误
funcs = [lambda x: x + n for n in range(5)]
for f in funcs:
    print(f(1))
"""
打印出来的值全部都是5
"""

funcs = [lambda x, n=n: x+n for n in range(5)]
for f in funcs:
    print(f(1))

print('=====7.8 减少可调用对象的参数个数=====')
"""
如果需要减少某个函数的参数个数，你可以使用 functools.partial()
"""


def spam(a1, b1, c1, d1):
    print(a1, b1, c1, d1)


s1 = partial(spam, d1=50)
s1(1, 3, 4)

points = [(1, 2), (3, 4), (5, 6), (7, 8), (4, 3)]


def distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return math.hypot(x2 - x1, y2 - y1)


pt = (4, 3)
points.sort(key=partial(distance, pt))
print(points)


def output_result(result, log=None):
    if log is not None:
        log.debug('Got: %r', result)


def add(x, y):
    return x + y


if __name__ == '__main__':
    import logging
    from multiprocessing import Pool
    from functools import partial

    logging.basicConfig(level=logging.DEBUG)
    log = logging.getLogger('test')

    p = Pool()
    p.apply_async(add, (3, 4), callback=partial(output_result, log=log))
    p.close()
    p.join()

