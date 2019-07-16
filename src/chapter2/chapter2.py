# 字符串
import re
from fnmatch import fnmatch, fnmatchcase
print('=======2.1=========')
'''
使用多个界定符分割字符串
string 对象的 split() 方法只适应于非常简单的字符串分割情形， 它并不允许有多个分隔符或者是分隔符周围不确定的空格。 当你需要更加灵活的切割字符串的时候，最好使用 re.split()
'''

line = 'asdf fjdk; afed, fjek,asdf, foo'
lines = re.split(r'[;,\s]\s*', line)
print(lines)

print('=======2.3=========')
'''
字符串的匹配：简单的开头结尾的验证str.startwith()和str.endwith()函数。
用Shell通配符匹配字符串，fnmatch模块提供了两个函数 --fnmatch()和fnmatchcase()，fnmatch()函数大小写敏感
'''
ismatch = fnmatch('foo.txt', '*.txt')
print(ismatch)

print(fnmatch('Dat45.csv', 'Dat[0-9]*'))

'''
fnmatch() 函数匹配能力介于简单的字符串方法和强大的正则表达式之间。 如果在数据处理操作中只需要简单的通配符就能完成的时候，这通常是一个比较合理的方案
'''
text = 'yeah, but no, but yeah, but no, but yeah'
print(text.find('no'))
text1 = '11/27/2012'
text2 = 'Nov 27, 2012'
# Simple matching: \d+ means match one or more digits
# 此处的字符串 r'\d+/\d+/\d+' 为什么以r开头，表示原始字符串，不会去解析反斜杠，否则需要写成'(\\d+)/(\\d+)/(\\d+)'
if re.match(r'\d+/\d+/\d+', text1):
    print('yes')
else:
    print('no')

if re.match(r'\d+/\d+/\d+', text2):
    print('yes')
else:
    print('no')

# 也可以生成一个模式对象去匹配
datepat = re.compile(r'\d+/\d+/\d+')
if datepat.match(text1):
    print('yes')
else:
    print('no')
if datepat.match(text2):
    print('yes')
else:
    print('no')

'''
字符串的替换 str.replace()替换str中的所有匹配字符, re模块中sub()函数
'''
text = 'yeah, but no, but yeah, but no, but yeah'
print(text.replace('yeah', 'yep'))

text = 'Today is 11/27/2012. PyCon starts 3/13/2013.'
# sub() 函数中的第一个参数是被匹配的模式，第二个参数是替换模式。反斜杠数字比如 \3 指向前面模式的捕获组号
text = re.sub(r'(\d+)/(\d+)/(\d+)', r'\3-\1-\2', text)
print(text)

# re.IGNORECASE忽略大小写标识
text = 'UPPER PYTHON, lower python, Mixed Python'
print(re.findall('python', text, flags=re.IGNORECASE))

# text = re.sub('python', 'snake', text, flags=re.IGNORECASE)
# print(text)


# 忽略的大小写的替换，并没有按照原来的规则替换，下面的函数则是修复这个问题
def matchcase(word):
    def replace(m):
        t = m.group()
        if t.isupper():
            return word.upper()
        elif t.islower():
            return word.lower()
        elif t[0].isupper():
            return word.capitalize()
        else:
            return word
    return replace


print(re.sub('python', matchcase('snake'), text, flags=re.IGNORECASE))

print('=======2.11=========')
'''
删除字符串中不需要的字符，strip()方法能用于删除开始或者结尾的字符，lstrip()和rstrip()分别从左和从右执行删除操作。
'''
s = ' hello world \n'
print(s.strip())
print(s.lstrip())
print(s.rstrip())

t = '-----hello====='
print(t.lstrip('-'))
print(t.rstrip('='))
print(t.strip('-='))

'''
format()函数字符串的格式化

字符串令牌解析的作用是什么？？？
'''

print('=======2.20=========')
'''
字节字符串上的字符串操作
'''
a = 'Hello World'  # Text string
print(a[0])

b = b'Hello World'  # binary string
print(b[0])
