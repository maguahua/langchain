# 装饰器基本语法
# def decorator(func):  # 1
#     def wrapper(*args, **kwargs):  # 2
#         # 在这里添加额外的功能
#         print("Before calling the function")  # 5
#         result = func(*args, **kwargs)  # 6
#         print("After calling the function")  # 8
#         return result  # 9
#
#     return wrapper  # 3
#
#
# @decorator  # 4
# def my_function():  # 6
#     print("Hello, this is my function.")  # 7
#
#
# # 调用my_function时，实际上调用的是wrapper函数
# my_function()  # 10


# 带参数的装饰器
# def decorator(func):
#     def wrapper(*args, **kwargs):
#         print("Function is called with arguments:", args, kwargs)
#         result = func(*args, **kwargs)
#         return result
#
#     return wrapper
#
#
# @decorator
# def my_function(x, y):
#     return x + y
#
#
# print(my_function(3, 4))

# 装饰器带参数
# def repeat(num_times):
#     def decorator(func):
#         def wrapper(*args, **kwargs):
#             for _ in range(num_times):
#                 result = func(*args, **kwargs)
#             return result
#
#         return wrapper
#
#     return decorator
#
#
# @repeat(3)
# def say_hello():
#     print("Hello!")
#
#
# say_hello()  # 输出三次Hello!

# 使用functools.wraps保留原函数信息
# from functools import wraps
#
#
# def my_decorator(func):#1
#     @wraps(func)#5、7
#     def wrapper(*args, **kwargs):#6、8
#         print("Something is happening before the function is called.")
#         result = func(*args, **kwargs)
#         print("Something is happening after the function is called.")
#         return result
#
#     return wrapper#9
#
#
# @my_decorator#2、4、10
# def example():#3、11
#     """This is an example function."""
#     print("Hello from a function.")
#
#
# print(example.__doc__)  # 12
