'''
在函数添加一个包装器，增加额外的操作处理（比如：日志、计时等）
'''


import time
import logging
from functools import wraps, partial


# 定义一个装饰器函数
def timethis(func):

    '''
    Decorator that reports the execution time
    '''

    @wraps(func)  # 这个注解是为了保存函数的重要元信息
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(func.__name__, end - start)
        return result
    return wrapper


@timethis
def countdown(n):
    while n > 0:
        n -= 1
    print("计算结束")


countdown(10000000)

print("---分界线----")

# 直接访问原始未包装的函数 __wrapped__
origin_countdown = countdown.__wrapped__
origin_countdown(10000000)

'''
上面使用 __wrapped__ 直接访问未包装的原始函数在调试、内省、和其他函数操作使有用，
但并不是所有的都有用，因为不是所有的装饰器都使用了@wraps
'''



'''
一个可以给函数添加日志功能的装饰器，同时允许用户指定日志级别和其他选项。
'''


def logged(level, name=None, message=None):
    ''''
    Add logging to a function. level is the logging level,
    name is the logger name, and message is the log message.
    If name and message aren't specified, they default to the
    function's module and name
    '''

    def decorate(func):
        logname = name if name else func.__module__
        log = logging.getLogger(logname)
        logmsg = message if message else func.__name__

        @wraps(func)
        def wrapper(*args, **kwargs):
            log.log(level, logmsg)
            return func(*args, **kwargs)
        return wrapper
    return decorate


@logged(logging.DEBUG)
def add(x, y):
    return x + y


@logged(logging.CRITICAL, 'example')
def spam():
    print("Spam !!!")


print(add(3, 4))


'''
9.5 允许用户提供参数在运行时控制装饰器行为，
    方法：引入一个访问函数，使用nonlocal来修改内部变量，然后这个访问函数被作为一个属性赋值给包装函数
'''


# Utility decorator to attach a function as an attribute of obj
def attach_wrapper(obj, func=None):
    if func is None:
        return partial(attach_wrapper, obj)
    setattr(obj, func.__name__, func)
    return func


def logged1(level, name=None, message=None):
    def decorator(func):
        logname = name if name else func.__module__
        log = logging.getLogger(logname)
        logmsg = message if message else func.__name__

        @wraps(func)
        def wrapper(*args, **kwargs):
            log.log(level,logmsg)
            return func(*args, **kwargs)

        # Attach setter functions
        @attach_wrapper(wrapper)
        def set_level(newlevel):
            nonlocal level
            level = newlevel

        @attach_wrapper(wrapper)
        def set_msg(newmsg):
            nonlocal logmsg
            logmsg = newmsg

        return wrapper
    return decorator


@logged1(logging.DEBUG)
def add1(x, y):
    return x + y


logging.basicConfig(level=logging.DEBUG)
add1.set_msg("求和")
add1(2, 3)


'''
9.6 写一个装饰器，既可以不传参数给它，比如：@decorator，也可以传递可选参数给它，比如：@decorator(x, y, z)
'''


def logged2(func=None, *, level=logging.DEBUG, name=None, message=None):
    if func is None:
        return partial(logged, level=level, name=name, message=message)

    logname = name if name else func.__module__
    log = logging.getLogger(logname)
    logmsg = message if message else func.__name__

    @wraps(func)
    def wrapper(*args, **kwargs):
        log.log(level, logmsg)
        return func(*args, **kwargs)
    return wrapper


@logged2
def add2(x, y):
    return x + y
