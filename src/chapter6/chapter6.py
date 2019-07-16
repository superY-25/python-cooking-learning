import csv
from collections import namedtuple, OrderedDict, Counter
import json
from pprint import pprint
from urllib.request import urlopen
from xml.etree.ElementTree import parse, iterparse, Element, tostring
import ssl
import binascii
import base64
from struct import Struct
filedir = '/Users/yangchao/Python/testdata/'
print('=====6.1 读写CSV数据=====')
# 下面返回的是列表，获取相应的字段数据需要通过下标获取
with open(filedir + 'test.csv') as f:
    f_csv = csv.reader(f)
    headers = next(f_csv)
    print(headers)
    for row in f_csv:
        print(row)

# 使用命名元组来获取相应的字段数据, 通过row.Change
with open(filedir + 'test.csv') as f:
    f_csv = csv.reader(f)
    headings = next(f_csv)
    Row = namedtuple('Row', headings)
    for r in f_csv:
        row = Row(*r)
        print(row)

# 将数据读取到一个字典序列中去 row['Change']
with open(filedir + 'test.csv') as f:
    f_csv = csv.DictReader(f)
    for row in f_csv:
        print(row)

# 写入数据 csv文件
headers = ['Symbol', 'Price', 'Date', 'Time', 'Change', 'Volume']
rows = [('AA', 39.48, '6/11/2007', '9:36am', -0.18, 181800),
        ('AIG', 71.38, '6/11/2007', '9:36am', -0.15, 195500),
        ('AXP', 62.58, '6/11/2007', '9:36am', -0.46, 935000)]
with open(filedir + 'test.csv', 'w') as f:
    f_csv = csv.writer(f)  # 创建一个writer对象 操作元组列表
    f_csv.writerow(headers)
    f_csv.writerow(rows)


rows = [{'Symbol': 'AA', 'Price': 39.48, 'Date': '6/11/2007',
        'Time': '9:36am', 'Change': -0.18, 'Volume': 181800},
        {'Symbol': 'AIG', 'Price': 71.38, 'Date': '6/11/2007',
        'Time': '9:36am', 'Change': -0.15, 'Volume': 195500},
        {'Symbol': 'AXP', 'Price': 62.58, 'Date': '6/11/2007',
        'Time': '9:36am', 'Change': -0.46, 'Volume': 935000}]
with open(filedir + 'test.csv', 'w') as f:
    f_csv = csv.DictWriter(f, headers)  # 操作字典列表数据
    f_csv.writeheader()
    f_csv.writerows(rows)

'''
如果你读取CSV数据的目的是做数据分析和统计的话， 你可能需要看一看 Pandas 包。Pandas 包含了一个非常方便的函数叫 pandas.read_csv()，
它可以加载CSV数据到一个 DataFrame 对象中去。 然后利用这个对象你就可以生成各种形式的统计、过滤数据以及执行其他高级操作了。
'''

print('=====6.2 读写JSON数据=====')
data = {
    'name': 'ACME',
    'shares': 100,
    'price': 542.23
}
# 字典转换成json字符串
json_str = json.dumps(data)
print(json_str)

# json字符串转换成Python数据结构
data = json.loads(json_str)
pprint(data)

# writing JSON data
with open(filedir + 'data.json', 'w') as f:
    json.dump(data, f)

# reading JSON data
with open(filedir + 'data.json', 'r') as f:
    data = json.load(f)
    print(data)

s = '{"name": "ACME", "shares": 50, "price": 490.1}'
data = json.loads(s, object_pairs_hook=OrderedDict)
print(data)


print('=====6.3 解析简单的XML数据=====')

# download the rss feed and parse it
ssl._create_default_https_context = ssl._create_unverified_context
u = urlopen('http://planet.python.org/rss20.xml')
doc = parse(u)  # <xml.etree.ElementTree.ElementTree object at 0x10ed47c18>

# extract and output tags of interest
for item in doc.iterfind('channel/item'):
    titile = item.findtext('title')
    date = item.findtext('pubDate')
    link = item.findtext('link')
    print(titile)
    print(date)
    print(link)
    print()

'''
有一点要强调的是 xml.etree.ElementTree 并不是XML解析的唯一方法。 对于更高级的应用程序，你需要考虑使用 lxml 。 
它使用了和ElementTree同样的编程接口，因此上面的例子同样也适用于lxml。 你只需要将刚开始的import语句换成 from lxml.etree import parse 就行了。 
lxml 完全遵循XML标准，并且速度也非常快，同时还支持验证，XSLT，和XPath等特性
'''

print('=====6.4 增量式解析大型XML文件=====')
'''
任何时候只要是遇到增量式的数据处理，第一时间应该想到迭代器和生成器
'''
# 使用少量的内存来增量式的处理一个大型XML文件


def parse_and_remove(filename, path):
    path_parts = path.split('/')
    doc = iterparse(filename, ('start', 'end'))
    # skip the root element
    next(doc)

    tag_stack = []
    elem_stack = []
    for event, elem in doc:
        if event == 'start':
            tag_stack.append(elem.tag)
            elem_stack.append(elem)
        elif event == 'end':
            if tag_stack == path_parts:
                yield elem
                elem_stack[-2].remove(elem)
            try:
                tag_stack.pop()
                elem_stack.pop()
            except IndexError:
                pass

# 测试上面函数需要有一个大型的XML文件


print('=====6.5 将字典转换为XML=====')
'''
使用一个Python字典存储数据，并将它转换成XML格式
'''


def dict_to_xml(tag, d):
    """
    Turn a simple dict of key/value pairs into XML
    :param tag:
    :param d:
    :return:
    """
    elem = Element(tag)
    for key, val in d.items():
        child = Element(key)
        child.text = str(val)
        elem.append(child)
    return elem


s = {'name': 'GOOG', 'shares': 100, 'price': 490.1}
e = dict_to_xml('stock', s)
print(tostring(e))


doc = parse('/Users/yangchao/Python/testdata/pre.xml')
root = doc.getroot()
print(tostring(root))
# remove a few elements
root.remove(root.find('sri'))
root.remove(root.find('cr'))

# insert a few element after <nm>...</nm>
root.getchildren().index(root.find('nm'))

e = Element('spam')
e.text = 'This is a test'
root.insert(2, e)

doc.write('newpred.xml', xml_declaration=True)


print('=====6.7 利用命名空间解析XML文档=====')

author = parse('/Users/yangchao/Python/testdata/author.xml')
'''
若是用普通的方法解析这个文档，会变得非常麻烦。
'''
# 需要将命名空间的地址完全匹配
author.find('content/{http://www.w3.org/1999/xhtml}html')

'''
对于这种命名空间完全匹配可以包装成一个工具类来简化这个过程
'''


class XMLNamespaces:
    def __init__(self, **kwargs):
        self.namespaces = {}
        for name, uri in kwargs.items():
            self.register(name, uri)

    def register(self, name, uri):
        self.namespaces[name] = '{' + uri + '}'

    def __call__(self, path):
        return path.format_map(self.namespaces)


ns = XMLNamespaces(html='http://www.w3.org/1999/xhtml')
author.find(ns('content/{html}html'))
author.findtext(ns('content/{html}html/{html}head/{html}title'))

'''
使用iterparse()函数可以获取更多关于命名空间处理范围的信息
'''

print('=====6.8 与关系型数据库的交互=====')
'''
在关系型数据库中查询、增加或删除记录
在Python中表示多行数据的标准方式是一个由元组构成的序列
依据PEP249，通过这种形式提供数据， 可以很容易的使用Python标准数据库API和关系型数据库进行交互。 
所有数据库上的操作都通过SQL查询语句来完成。每一行输入输出数据用一个元组来表示。
'''
stocks = [
    ('GOOG', 100, 490.1),
    ('AAPL', 50, 545.75),
    ('FB', 150, 7.45),
    ('HPQ', 75, 33.2)
]

'''
在Python标准库中sqlite3模块，也可以使用第三方模块来提供支持
'''


print('=====6.9 编码和解码十六进制数=====')

s = b'hello'
# encode as hex
h = binascii.b2a_hex(s)
print(h)
# decode back to bytes
print(binascii.a2b_hex(h))

# base64编码
h = base64.b16encode(s)
print(h)
# base64解码
print(base64.b16decode(h))

'''
大部分情况下，通过使用上述的函数来转换十六进制是很简单的。 上面两种技术的主要不同在于大小写的处理。 
函数 base64.b16decode() 和 base64.b16encode() 只能操作大写形式的十六进制字母， 而 binascii 模块中的函数大小写都能处理。
'''

print('=====6.11 读写二进制数组数据=====')


def write_records(records, format, f):
    """
    write a sequence of tuples to a binary file of structures
    :param records:
    :param format:
    :param f:
    :return:
    """
    record_struct = Struct(format)
    for r in records:
        f.write(record_struct.pack(*r))


records = [(1, 2.3, 4.5),
           (6, 7.8, 9.0),
           (12, 13.4, 56.7)
           ]
with open('data.b', 'wb') as f:
    write_records(records, '<idd', f)


# 读取二进制文件并返回一个元组列表
def read_records(format, f):
    record_struct = Struct(format)
    chunks = iter(lambda: f.read(record_struct.size), b'')
    return (record_struct.umpack(chunk) for chunk in chunks)


with open('data.b', 'rb') as f:
    for rec in read_records('<idd', f):
        # process rec
        pass

