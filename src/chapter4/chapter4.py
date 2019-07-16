# 迭代器和生成器迭代是Python最强大的功能之一，
from collections import deque
from collections.abc import Iterable
from itertools import islice, permutations, combinations, combinations_with_replacement, zip_longest, chain
from heapq import merge

print('======4.1========')
'''
遍历一个可迭代对象中的所有元素，但是不用for循环，
使用next()函数并在代码中捕获StopIteration异常。
'''


def manual_iter():
    with open('/etc/passwd') as f:
        try:
            while True:
                line = next(f)
                print(line, end='')
        except StopIteration:
            pass


# 通常来说StopIteration用来指示迭代的结尾。但是如果你手动使用上面的演示的next()函数的话，你还可以通过返回一个指定值来标记结尾。比如 None
def manual_iter1():
    with open('/etc/passwd') as f:
        while True:
            line = next(f)
            if line is None:
                break
            print(line, end='')


items = [1, 2, 3]
it = iter(items)
print(next(it))
print(next(it))
print(next(it))
# print(next(it))  # 迭代已结束，此行代码异常


print('======4.2========')
'''
自定义的一个容器对象，里面包含列表、元组或其他可迭代对象，若要使这个自定义容器对象可以进行迭代操作，只需要定义一个__iter__()方法。
'''


class Node:
    def __init__(self, value):
        self._value = value
        self._children = []

    def __repr__(self):
        return 'Node({!r})'.format(self._value)

    def add_child(self, node):
        self._children.append(node)

    def __iter__(self):
        return iter(self._children)


root = Node(0)
child1 = Node(1)
child2 = Node(2)
root.add_child(child1)
root.add_child(child2)
# for循环
for n in root:
    print(n)
# 迭代器
node = iter(root)
print(next(node))
print(next(node))

print('======4.3========')
"""
使用生成器来创建新的迭代模式
一个函数中需要有一个 yield 语句即可将其转换为一个生成器
一个生成器函数主要特征是它只会回应在迭代中使用到的 next 操作
一旦生成器函数返回退出，迭代终止
"""


def frange(start, stop, increment):
    """
    使用这个函数， 你可以用for循环迭代它或者使用其他接受一个可迭代对象的函数(比如 sum() , list() 等)
    :param start:
    :param stop:
    :param increment:
    :return:
    """
    x = start
    while x < stop:
        yield x
        x += increment


print(list(frange(0, 1, 0.125)))
for n in frange(0, 2, 0.5):
    print(n)


class Node1:
    def __init__(self, value):
        self._value = value
        self._children = []

    def __repr__(self):
        return 'Node({!r})'.format(self._value)

    def add_child(self, node):
        self._children.append(node)

    def __iter__(self):
        return iter(self._children)

    def depth_first(self):
        """
        深度优先遍历
        :return:
        """
        yield self
        for c in self:
            yield from c.depth_first()


root = Node1(0)
child1 = Node1(1)
child2 = Node1(2)
root.add_child(child1)
root.add_child(child2)
child1.add_child(Node1(3))
child1.add_child(Node1(4))
child2.add_child(Node1(5))
for ch in root.depth_first():
    print(ch)

'''
Python的迭代协议要求一个__iter__()方法返回一个特殊的迭代器对象，
这个迭代器对象实现了__next__()方法并通过StopIteration异常标识迭代的完成。
但是实现这些通常会比较繁琐
'''


class Node2:
    def __init__(self, value):
        self._value = value
        self._children = []

    def __repr__(self):
        return 'Node({!r})'.format(self._value)

    def add_child(self, node):
        self._children.append(node)

    def __iter__(self):
        return iter(self._children)

    def depth_first(self):
        return DepthFirstIterator(self)


class DepthFirstIterator:
    """
    Depth-first traversal
    """
    def __init__(self, start_node):
        self._node = start_node
        self._children_iter = None
        self._child_iter = None

    def __iter__(self):
        return self

    def __next__(self):
        # Return myself if just started; create an iterator for children
        if self._children_iter is None:
            self._children_iter = iter(self._node)
            return self._node
        # If processing a child, return its next item
        elif self._child_iter:
            try:
                nextchild = next(self._child_iter)
                return nextchild
            except StopIteration:
                self._child_iter = None
                return next(self)
        # Advance to the next child and start its iteration
        else:
            self._child_iter = next(self._children_iter).depth_first()
            return next(self)


'''
DepthFirstIterator类和上面的使用生成器的版本工作原理类似，但是它写起来很繁琐，因为迭代器必须在迭代处理过程中维护大量的状态信息
'''

print('======4.5========')
'''
反向迭代
内置的函数 reversed()
'''
a = [1, 2, 3, 4]
for i in reversed(a):
    print(i)
'''
反向迭代仅仅当对象的大小可预先确定或者对象实现了__reversed__()的特殊方法时才生效。
如果两者都不符合，则需要先将对象转换为一个列表才行，但要注意，如果迭代的元素很多的话，
将其预先转换为一个列表要消耗大量的内存
'''


class Countdown:
    """
    自定义反向迭代，实现__reversed__()方法
    """
    def __init__(self, start):
        self.start = start

    def __iter__(self):
        n = self.start
        while n > 0:
            yield n
            n -= 1

    def __reversed__(self):
        n = 1
        while n <= self.start:
            yield n
            n += 1


for rr in reversed(Countdown(4)):
    print("reversed countdown: ", rr)
for rr in Countdown(4):
    print("countdown: ", rr)

print('======4.6========')
"""
带有外部状态的生成器函数
如果你想让你的生成器暴露外部状态给用户， 别忘了你可以简单的将它实现为一个类，然后把生成器函数放到 __iter__() 方法中过去。
"""


class linehistory:
    def __init__(self, lines, histlen=3):
        self.lines = lines
        self.history = deque(maxlen=histlen)

    def __iter__(self):
        for lineno, line in enumerate(self.lines, 1):
            self.history.append((lineno, line))
            yield line

    def clear(self):
        self.history.clear()

"""
with open('somefile.txt') as f:
    lines = linehistory(f)
    for line in lines:
        if 'python' in line:
            for lineno, hline in lines.history:
                print('{}:{}'.format(lineno, line), end='')"""


print('======4.7========')
'''
迭代器切片 itertools.islice()
'''


def count(n):
    while True:
        yield n
        n += 1


c = count(0)
# using islice() function
for x in islice(c, 10, 20):
    print(x)

print('======4.8========')
'''
跳过可迭代对象的开始部分


with open('/etc/passwd') as f:
    for line in f:
        print(line, end='')

假设上面的代码打印出来的结果是：
# User Database
#
# Note that this file is consulted directly only when the system is running
# in single-user mode. At other times, this information is provided by
# Open Directory.
nobody:*:-2:-2:Unprivileged User:/var/empty:/usr/bin/false
root:*:0:0:System Administrator:/var/root:/bin/sh
如果想要跳过开始部分的注释，代码改成如下：

with open('etc/passwd') as f:
    for line in dropwhile(lambda line: line.startswith('#'), f):
        print(line, end='')
'''

print('======4.9========')
'''
排列组合的迭代
'''
items = ['a', 'b', 'c']
# 排列迭代
for item in permutations(items):
    print('三元素排列', item)

for item in permutations(items, 2):
    print('两元素排列',  item)

# 组合迭代    combinations的两个参数必传
for item in combinations(items, 3):
    print('三元素组合', item)

for item in combinations(items, 2):
    print('两元素组合', item)

# 元素有重复组合迭代 combinations_with_replacement
for item in combinations_with_replacement(items, 3):
    print('combinations_with_replacement:', item)


print('======4.10========')
'''
序列上索引值迭代
在迭代一个序列的同时跟踪正在被处理的元素索引
'''
mylist = ['a', 'b', 'c']
for idx, val in enumerate(mylist):
    print('索引={};值={}'.format(idx, val))

# 若是按序号算从1开始
for idx, val in enumerate(mylist, 1):
    print('第{}个值是{}'.format(idx, val))


# 遍历文件时，错误信息定位行号
def parse_data(filename):
    with open(filename, 'rt') as f:
        for lineno, line in enumerate(f, 1):
            fields = line.split()
            try:
                pass
            except ValueError as e:
                print('Line:{},parse error:{}'.format(lineno, e))
               

'''
统计文本中单词出现在的行号和次数

word_summary = defaultdict(list)
with open('filename.txt', 'r') as f:
    lines = f.readlines()
for idx, line in enumerate(lines, 1):
    # create a list of words in current line
    words = [w.strip().lower() for w in line.split()]
    for word in words:
        word_summary[word].append(idx)
'''

print('======4.11========')
'''
同时迭代多个序列 使用zip()函数
zip(a, b) 会生成一个可返回元组 (x, y) 的迭代器，其中x来自a，y来自b。 一旦其中某个序列到底结尾，迭代宣告结束
如果想以最长的列表结束可以使用itertools.zip_longest()函数
'''
xpts = [1, 5, 4, 2, 10, 7]
ypts = [101, 78, 37, 15, 62, 99, 54, 76]
for x, y in zip(xpts, ypts):
    print(x, y)

for x, y in zip_longest(xpts, ypts):
    print(x, y)

for i in zip_longest(xpts, ypts, fillvalue=0):
    print(i)

print('======4.12========')
'''
不同集合上元素的迭代
'''
a = [1, 2, 3, 4]
b = ['x', 'y', 'z']
for i in chain(a, b):
    print(i)
'''
当两个列表的类型相同的情况下也可以使用 for i in a+b进行迭代，但是这样会生成一个和a、b类型一样的全新列表
然而chain()函数并不会，所以如果列表很大的情况下使用chain()函数可以省很大内存并且当迭代的列表类型不一致的情况下也能很好的工作
'''

print('======4.13========')
'''
创建数据处理管道
以数据管道(类似Unix管道)的方式迭代处理数据。 比如，你有个大量的数据需要处理，但是不能将它们一次性放入内存中。
生成器函数是一个实现管道机制的好办法
'''

"""
假定你要处理一个非常大的日志文件目录:
foo/
    access-log-012007.gz
    access-log-022007.gz
    access-log-032007.gz
    ...
    access-log-012008.gz
bar/
    access-log-092007.bz2
    ...
    access-log-022008.bz2
假设每个日志文件包含这样的数据:
124.115.6.12 - - [10/Jul/2012:00:18:50 -0500] "GET /robots.txt ..." 200 71
210.212.209.67 - - [10/Jul/2012:00:18:51 -0500] "GET /ply/ ..." 200 11875
210.212.209.67 - - [10/Jul/2012:00:18:51 -0500] "GET /favicon.ico ..." 404 369
61.135.216.105 - - [10/Jul/2012:00:20:04 -0500] "GET /blog/atom.xml ..." 304 -
为了处理这些文件，你可以定义一个由多个执行特定任务独立任务的简单生成器函数组成的容器。

import os
import fnmatch
import gzip
import bz2
import re


def gen_find(filepat, top):
    '''
    Find all filenames in a directory tree that match a shell wildcard pattern
    :param filepat:
    :param top:
    :return:
    '''
    for path, dirlist, filelist in os.walk(top):
        for name in fnmatch.filter(filelist, filepat):
            yield os.path.join(path, name)


def gen_opener(filenames):
    '''
    Open a sequence of filenames one at a time producing a file object.
    The file is closed imeediately when proceeding to the next iteration.
    :param filenames:
    :return:
    '''
    for filename in filenames:
        if filename.endswith('.gz'):
            f = gzip.open(filename, 'rt')
        elif filename.endswith('bz2'):
            f = bz2.open(filename, 'rt')
        else:
            f = open(filename, 'rt')
        yield f
        f.close()


def gen_concatenate(iterators):
    '''
    Chain a sequence of iterators together into a single sequence.
    :param iterators:
    :return:
    '''
    for it in iterators:
        yield from it


def gen_grep(pattern, lines):
    '''
    Look for a regex pattern in a sequence of lines
    :param pattern:
    :param lines:
    :return:
    '''
    pat = re.compile(pattern)
    for line in lines:
        if pat.search(line):
            yield line


# 现在你可以很容易的将这些函数连起来创建一个处理管道。 比如，为了查找包含单词python的所有日志行
lognames = gen_find('access-log*', 'www')
files = gen_opener(lognames)
lines = gen_concatenate(files)
pylines = gen_grep('(?i)python', lines)
for line in pylines:
    print(line)

"""

'''
展开嵌套的序列
将一个多层嵌套的序列展开成一个单层列表
可以写一个 yield from 语句的递归生成器来解决这个问题
'''


def flatten(items, ignore_types=(str, bytes)):
    """
    isinstance(x, Iterable)检查某个元素是否可迭代的，如果是的话，yield from 就会返回所有子例程的值，
    额外的参数ignore_types和检测语句isinstance(x, ignore_types)用来将字符串和字节排除在可迭代对象之外，防止将它们再展开成单个字符
    :param items:
    :param ignore_types:
    :return:
    """
    for x in items:
        if isinstance(x, Iterable) and not isinstance(x, ignore_types):
            yield from flatten(x)
        else:
            yield x


items = [1, 2, [3, 4, [5, 6], 7], 8]
# produces 1 2 3 4 5 6 7 8
for x in flatten(items):
    print(x)

items = ['Dave', 'Paula', ['Thomas', 'Lewis']]
for x in flatten(items):
    print(x)


print('======4.14========')
'''
顺序迭代合并后的排序迭代对象
h
'''
a = [1, 4, 7, 10]
b = [2, 5, 6, 11]
for c in merge(a, b):
    print(c)

'''
heapq.merge()可迭代特性意味着它不会立马读取所有序列。这意味着你可以在非常长的列表中使用它，而不会有太大的开销
with open('sorted_file1', 'rt') as file1, open('sorted_file2', 'rt') as file2, open('merged_file', 'wt') as outf:
for line in heapq.merge(file1, file2):
    outf.write(line)
注意：heapq.merge()需要所有输入序列必须是排过序的，它并不会预先读取所有数据到堆栈中或者预先排序，也不会对输入做任何的排序检测，它仅仅是检查所有序列的开始部分并返回最小的那个，
这个过程一直会持续到所有输入序列中的元素都被遍历完。
'''






















