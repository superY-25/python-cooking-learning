# 数据结构和算法
import numpy as np
import heapq
from collections import OrderedDict, defaultdict, deque, Counter, namedtuple, ChainMap
from operator import itemgetter, attrgetter
from itertools import groupby

print("=======1.1=========")
'''
将一个包含N个元素的元组或者序列里面的值解压同时赋值给N个变量
注意：变量的个数一定要和元素的个数一致，否则会报错
     这种解压赋值可以用在任何可迭代对象上面，而不仅仅是列表或者元组。 包括字符串，文件对象，迭代器和生成器
'''
# 元组
p = (4, 5)
x, y = p
print("a : " + str(x) + "; b : " + str(y))

# 列表
data = ['ACME', 50, 91.1, (2012, 12, 21)]
name, shares, price, date = data
print("name=" + name)

# 字符串
s = 'Hello'
a, b, c, d, e = s
print("a = " + a)

print("=======1.2=========")


# 去掉第一个成绩和最后一个成绩求平均数
def drop_first_last(grades):
    firs, *middle, last = grades
    return np.mean(middle)


print(drop_first_last([3, 4, 5, 6, 7, 8, 9, 1, 10, 45, 32, 56]))

record = ('Dave', 'dave@example.com', '773-555-1212', '847-555-1212')
name, email, *phones = record  # 这种方式得出的phones始终都是列表类型。无需检验其类型
print(phones)


print("=======1.3=========")
'''
怎样从一个集合中获取最大或者最小的N个元素列表
heapq模块中有两个函数nlargest()和nsmallest()可以解决这个问题
'''

nums = [1, 8, 2, 23, 7, -4, 18, 23, 42, 37, 2]
print(heapq.nlargest(3, nums))
print(heapq.nsmallest(3, nums))

portfolio = [
    {'name': 'IBM', 'shares': 100, 'price': 91.1},
    {'name': 'AAPL', 'shares': 50, 'price': 543.22},
    {'name': 'FB', 'shares': 200, 'price': 21.09},
    {'name': 'HPQ', 'shares': 35, 'price': 31.75},
    {'name': 'YHOO', 'shares': 45, 'price': 16.35},
    {'name': 'ACME', 'shares': 75, 'price': 115.65}
]
cheap = heapq.nsmallest(2, portfolio, key=lambda s1: s1['price'])
expensive = heapq.nlargest(2, portfolio, key=lambda s1: s1['price'])
print(cheap)
print(expensive)


print("=======1.4=========")
'''
若想查找一个集合中最小或者最大的N个元素，N小于集合元素个数。
若N=1则使用min()或max()函数，若N的大小接近集合的元素个数，则使用sorted()排序再使用切片操作更好
'''
heap = list(nums)
heapq.heapify(heap)
print(heap)
print(heapq.heappop(heap))
print(heap)


print("=======1.5=========")
'''
实现一个按优先级排序的队列，并且在这个队列上面每次pop操作总是返回优先级最高的那个元素
'''


# 优先级队列
class PriorityQueue:
    def __init__(self):
        self._queue = []
        self._index = 0

    def push(self, item, priority):
        '''
        这里在_queue队列中插入三个元素的元组。加self._index元素是因为确保队列中元组的唯一性，能进行比较大小
        :param item:
        :param priority:
        :return:
        '''
        heapq.heappush(self._queue, (-priority, self._index, item))
        self._index += 1

    def pop(self):
        return heapq.heappop(self._queue)[-1]


# example use
class Item:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'Item({!r})'.format(self.name)


q = PriorityQueue()
q.push(Item('foo'), 1)
q.push(Item('bar'), 5)
q.push(Item('spam'), 4)
q.push(Item('grok'), 1)
q.push(Item('yang'), 3)
print(q.pop())

# 列表是有插入顺序的，集合是没有重复元素的。

print("=======1.6=========")
'''
实现一个键对应多个值的字典（也叫 multidict）。可以使用 collections 模块中的 defaultdict 来构造这样的字典。
defaultdict 的一个特征是它会自动初始化每个 key 刚开始对应的值，所以你只需要关注添加元素操作了


d = {}
pairs = {}
for key, value in pairs:
    if key not in d:
        d[key] = []
    d[key].append(value)

d = defaultdict(list)
for key, value in pairs:
    d[key].append(value)
'''

print("=======1.7=========")
'''
创建一个字典，并且在迭代或者序列化这个字典的时候能够控制元素的顺序，可以使用collections模块中的OrderedDict类。
在迭代操作的时候它会保持元素被插入时的顺序
注意：OrderedDict 内部维护着一个根据键插入顺序排序的双向链表。每次当一个新的元素插入进来的时候， 它会被放到链表的尾部。对于一个已经存在的键的重复赋值不会改变键的顺序。
     需要注意的是，一个 OrderedDict 的大小是一个普通字典的两倍，因为它内部维护着另外一个链表。 所以如果你要构建一个需要大量 OrderedDict 实例的数据结构的时候
    （比如读取 100,000 行 CSV 数据到一个 OrderedDict 列表中去）， 那么你就得仔细权衡一下是否使用 OrderedDict 带来的好处要大过额外内存消耗的影响。
'''
d = OrderedDict()
d['foo'] = 1
d['bar'] = 2
d['spam'] = 3
d['grok'] = 4

for key in d:
    print(key, d[key])

print("=======1.8=========")

'''
在数据字典中执行一些计算操作（比如求最小值、最大值、排序等等）
为了对字典值执行计算操作，通常需要使用 zip() 函数先将键和值反转过来
'''
prices = {
    'ACME': 45.23,
    'AAPL': 612.78,
    'IBM': 205.55,
    'HPQ': 37.20,
    'FB': 10.75
}
minprice = min(zip(prices.values(), prices.keys()))
print(minprice)
maxprice = max(zip(prices.values(), prices.keys()))
print(maxprice)

pricessorted = sorted(zip(prices.values(), prices.keys()))
print(pricessorted)

print("=======1.9=========")
'''
在两个字典中寻寻找相同点（比如相同的键、相同的值等等）
为了寻找两个字典的相同点，可以简单的在两字典的 keys() 或者 items() 方法返回结果上执行集合操作。
'''
a = {
    'x': 1,
    'y': 2,
    'z': 3
}

b = {
    'w': 10,
    'x': 11,
    'y': 2
}

# find keys in common
c = a.keys() & b.keys()
print(c)
# find keys in a that are not in b
c = a.keys() - b.keys()
print(c)
# find (key, value) pairs in common
c = a.items() & b.items()
print(c)

# 排除z w
c = {key: a[key] for key in a.keys() - {'z', 'w'}}
print(c)

print("=======1.10=========")
'''
在一个序列上面保持元素顺序的同时消除重复的值。
如果序列上的值都是 hashable 类型，那么可以很简单的利用集合或者生成器来解决这个问题
'''


def dedupe(items):
    '''
    这个方法仅仅在序列中元素为hashable的时候才管用。
    如果你想消除元素不可哈希(比如dict类型)的序列中重复元素的话需要另作修改
    :param items:
    :return:
    '''
    seen = set()
    for item in items:
        if item not in seen:
            yield item
            seen.add(item)


a = [1, 5, 2, 1, 9, 1, 5, 10]
print(list(dedupe(a)))


def dedupe1(items, key=None):
    seen = set()
    for item in items:
        val = item if key is None else key(item)
        if val not in seen:
            yield item
            seen.add(val)


a = [{'x': 1, 'y': 2}, {'x': 1, 'y': 3}, {'x': 1, 'y': 2}, {'x': 2, 'y': 4}]
print(list(dedupe1(a, key=lambda d: (d['x'], d['y']))))
print(list(dedupe1(a, key=lambda d: d['x'])))

print("=======1.12=========")
'''
找出一个序列中出现次数最多的元素
'''

words = [
    'look', 'into', 'my', 'eyes', 'look', 'into', 'my', 'eyes',
    'the', 'eyes', 'the', 'eyes', 'the', 'eyes', 'not', 'around', 'the',
    'eyes', "don't", 'look', 'around', 'the', 'eyes', 'look', 'into',
    'my', 'eyes', "you're", 'under'
]
wordcounts = Counter(words)
# 出现频率最高的3个词
topthree = wordcounts.most_common(3)
print(topthree)

morewords = ['why', 'are', 'you', 'not', 'looking', 'in', 'my', 'eyes']
morewordscounts = Counter(morewords)
print(wordcounts)
print(morewordscounts)
print(wordcounts - morewordscounts)


print("=======1.13=========")
'''
一个字典列表,根据某个或某几个字典字段来排序这个列表
通过使用operator模块中的itemgetter函数
'''
rows = [
    {'fname': 'Brian', 'lname': 'Jones', 'uid': 1003},
    {'fname': 'David', 'lname': 'Beazley', 'uid': 1002},
    {'fname': 'John', 'lname': 'Cleese', 'uid': 1001},
    {'fname': 'Big', 'lname': 'Jones', 'uid': 1004}
]

rowsbyfname = sorted(rows, key=itemgetter('fname'))
rowsbyuid = sorted(rows, key=itemgetter('uid'))
print(rowsbyfname)
print(rowsbyuid)
rowsbylfname = sorted(rows, key=itemgetter('lname', 'fname'))
print(rowsbylfname)

# 有时候也可用lambda表达式代替
rowsbyfname1 = sorted(rows, key=lambda r: r['fname'])
rowsbylfname1 = sorted(rows, key=lambda r: (r['lname'], r['fname']))
print(rowsbyfname1)
print(rowsbylfname1)

# 这种方式也可以用在min() 和max()函数中
print(min(rows, key=itemgetter('uid')))


print("=======1.14=========")
'''
自定义对象类型排序
'''


class User:
    def __init__(self, userid):
        self.userid = userid

    def __repr__(self):
        return 'User({})'.format(self.userid)


def sort_notcompare(obj):
    print("before sort: ", obj)
    print("after sort: ", sorted(obj, key=lambda u: u.userid))


users = [User(23), User(3), User(99)]
sort_notcompare(users)

# 除了上面的lambda表达式还可以用attrgetter
print(sorted(users, key=attrgetter('userid'), reverse=True))

print(min(users, key=attrgetter('userid')))

print('=======1.15=========')
'''
你有一个字典或者实例的序列，然后你想根据某个特定的字段比如 date 来分组迭代访问。
'''
rows = [
    {'address': '5412 N CLARK', 'date': '07/01/2012'},
    {'address': '5148 N CLARK', 'date': '07/04/2012'},
    {'address': '5800 E 58TH', 'date': '07/02/2012'},
    {'address': '2122 N CLARK', 'date': '07/03/2012'},
    {'address': '5645 N RAVENSWOOD', 'date': '07/02/2012'},
    {'address': '1060 W ADDISON', 'date': '07/02/2012'},
    {'address': '4801 N BROADWAY', 'date': '07/01/2012'},
    {'address': '1039 W GRANVILLE', 'date': '07/04/2012'},
]
# sort by the desired field first
rows.sort(key=itemgetter('date'))
print(rows)
# Iterable in groups
for date, items in groupby(rows, key=itemgetter('date')):
    print(date)
    for i in items:
        print('  ', i)

'''
上面的方法一个非常重要的准备步骤是要根据指定的字段将数据排序。 因为 groupby() 仅仅检查连续的元素，如果事先并没有排序完成的话，分组函数将得不到想要的结果。
如果你仅仅只是想根据 date 字段将数据分组到一个大的数据结构中去，并且允许随机访问， 那么你最好使用 defaultdict() 来构建一个多值字典
'''
print("====分割线======")
rowsbydate = defaultdict(list)
for row in rows:
    rowsbydate[row['date']].append(row)

for row in rowsbydate:
    print(row)
    for r in rowsbydate[row]:
        print('  ', r)


print('=======1.16=========')
'''
过滤序列元素
'''
mylist = [1, 4, -5, 10, -7, 2, 3, -1]
a = [n for n in mylist if n > 0]
print(a)
b = [n for n in mylist if n < 0]
print(b)
# 使用列表推导的一个潜在缺陷就是如果输入非常大的时候会产生一个非常大的结果集，占用大量内存
values = ['1', '2', '-3', '-', '4', 'N/A', '5']


def is_int(val):
    try:
        int(val)
        return True
    except ValueError:
        return False


ivals = list(filter(is_int, values))
print(ivals)


print('=======1.17=========')
'''
从字典中提取子集
'''
prices = {
    'ACME': 45.23,
    'AAPL': 612.78,
    'IBM': 205.55,
    'HPQ': 37.20,
    'FB': 10.75
}
# make a dictionary of all prices over 200
p1 = {key: value for key, value in prices.items() if value > 200}
print(p1)
# make a dictionary of tech stocks
techname = {'AAPL', 'IBM', 'HPQ', 'MSFT'}
p2 = {key: value for key, value in prices.items() if key in techname}
print(p2)
'''
大多数情况下字典推导能做到的，通过创建一个元组序列然后把它传给dict()函数也能实现，但是性能会慢很多。
'''
p1 = dict((key, value) for key, value in prices.items() if value > 200)


print('=======1.18=========')
'''
映射名称到序列元素
目标：有时候通过下标访问元素，代码难以阅读维护并且有可能出错。
'''
Subscriber = namedtuple('Subscriber', ['addr', 'joined'])
sub = Subscriber('jonesy@example.com', '2012-10-19')
print(sub.addr)
# 可以通过解压的形式赋值
addr, joined = sub
print(addr)

Stock = namedtuple('Stock', ['name', 'shares', 'price'])


def computecost(records):
    total = 0.0
    for rec in records:
        s1 = Stock(*rec)
        total += s1.shares * s1.price
    return total


print('=======1.20=========')
'''合并多个字典或映射'''
a = {'x': 1, 'z': 3}
b = {'y': 2, 'z': 4}
c = ChainMap(a, b)
print(c)
print(c['x'])
print(c['z'])
