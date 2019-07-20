import html
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
