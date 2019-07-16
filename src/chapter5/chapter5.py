import time
import os
import io

filename = '/Users/yangchao/Python/testdata/test.txt'


def progressbar():
    """
    打印进度条
    :return:
    """
    scale = 50
    print("执行开始".center(scale//2, "-"))
    start = time.perf_counter()
    for i in range(scale+1):
        a = "*" * i
        b = "." * (scale-i)
        c = (i/scale)*100
        dur = time.perf_counter() - start
        # 注意 \r转义符 需要在运行环境中运行才能显示效果，开发环境会自动屏蔽掉\r转义符
        print("\r{:^3.0f}%[{}->{}]{:.2f}s".format(c, a, b, dur), end="")
        time.sleep(0.1)
    print("\n" + "执行结束".center(scale//2, "-"))


print('=====5.1 读写文本数据=====')
'''
本节讲了python文本的读写，rt模式的open，wt模式的open以及at模式的open，
open()函数的几个参数：
'''
# Read the entire file as a single string
with open(filename, 'rt') as f:
    data = f.read()
print(data)

# Iterate over the lines of the file
with open(filename, 'rt') as f:
    for line in f:
        print(line)

with open(filename, 'at') as f:
    print('hello world', file=f)

print('ACME', 50, 91.5)
# sep 参数分隔符
print('ACME', 50, 91.5, sep=',')
# end 参数表示输出中禁止换行
print('ACME', 50, 91.5, sep=',', end='!!')
print('ACME', 50, 91.5)

row = ('ACME', 50, 91.5, 'yangchao')
print(*row, sep=',')

'''
读写字节数据，二进制文件，比如图片、声音文件等

with open('/Users/yangchao/Python/testdata/test.bin', 'wb') as f:
    f.write(b'Hello World')

with open('/Users/yangchao/Python/testdata/test.bin', 'rb') as f:
    for i in f:
        for c in i:
            print(c)

# xb 模式会检测文件是否存在
with open('/Users/yangchao/Python/testdata/test.bin', 'xb') as f:
    f.write(b'Hello World')

if not os.path.exists('/Users/yangchao/Python/testdata/test.bin'):
    with open('/Users/yangchao/Python/testdata/test.bin', 'wb') as f:
        f.write(b'Hello World')
else:
    print('File already exists !')
'''

print('=====5.6 字符串的I/O操作=====')
'''
使用操作类文件对象的程序来操作文本或二进制字符串
字符串 io.StringIO()和 io.BytesIO()
'''
s = io.StringIO()
s.write('Hello World\n')
print(s)


print("===== 5.9 读取二进制数据到可变缓冲区中 =====")
'''
直接读取二进制数据到一个可变缓冲区中，而不需要做任何的中间复制操作
或者原地修改数据并将它写回到一个文件中去。
'''


def read_into_buffer(fname):
    buf = bytearray(os.path.getsize(fname))
    with open(fname, 'rb') as fi:
        fi.readinto(buf)
    return buf


'''
文件对象的readinto()方法能被用来为预先分配内存的数组填充数据，甚至包括由array模块或numpy模块库创建的数组。
和普通read()方法不同的是，readinto()填充已存在的缓冲区而不是为新对象重新分配内存再返回它们，因此可以使用它来避免大量的内存分配操作。
record_size = 32  # size of each record (adjust value)
buf = bytearray(record_size)
with open('somefile', 'rb') as f:
    while True:
        n = f.readinto(buf)
        if n < record_size:
            break
        # use the contents of buf
'''


def bad_filename(fname):
    """
    打印不合法的文件名
    :param fname:
    :return:
    """
    return repr(fname)[1:-1]


files = ['spam.py', 'b\udce4d.txt', 'foo.txt']
for name in files:
    try:
        print(name)
    except UnicodeEncodeError:
        print(bad_filename(name))


