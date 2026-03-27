# # 输出hello world
# print("Hello World")
# print("hello") # python")
# a = 10
# b = 20
# c = 30
# a,b,c = b,c,a
#
# print("zhiwei:",a,b,c)

# d = 1
# print(isinstance(d,int))
# print(isinstance(d,bool))

# age = 18
# name = input("请输入你的名字:")
# print(f"我的年龄是{age},我叫{name}")
#
# num = 0
# print(bool(num) == True)

# num1 = int(input("请输入第一个数:"))
# num2 = int(input("请输入第二个数:"))
# print("两数之和为:",num1+num2)
# print("两数之差为:",num1-num2)

# 判断输入的数是否在10-20之间
# n = int(input("请输入一个数:"))
# print(f"数字{n}在10-20之间?", 10<=n<=20)

# score = int(input("请输入你的分数:"))
# if score >= 680:
#     print("欢迎加入北大")
# else:
#     print("回去作田吧")

# username = input("Enter your username: ")
# password = input("Enter your password: ")
# if username == "zzc" and password == "770215":
#     print("欢迎登录")

# 非百年能被4整除,百年能被400整除
# year = int(input())
# if year % 4 == 0 and year % 100 != 0 or year % 400 == 0:
#     print("是闰年")

# 查看输入的星期
# day = int(input("请输入你的星期:"))
# match day :
#     case 1:
#         print("星期一")
#     ......
#     case 6 | 7:
#         print("周末")
#     case 7:
#         print("星期七")
#     case _:
#         print("输入错误")

# total = 0
# num = 1
# while num <= 100:
#     total += num
#     num += 1
# print("1-100的和为:", total)

# import time
#
# for i in range(101):
#     print(f"\r进度: {i}%", end='')   # \r 回到行首重写
#     time.sleep(0.05)
# print("\n完成！"

# height = int(input("输入长方形的宽:"))
# weight = int(input("输入长方形的长:"))
#
# for h in range(height):
#     for w in range(weight):
#         print("*",end=" ")
#     print()

# 打印九九乘法表
# for i in range(1,10):
#     for j in range(1,10):
#         if i>=j:
#             print(f"{j} * {i} = {j * i}",end="\t")
#     print()

# 随机数小游戏
# import random
# num = random.randint(1,100)
# cheat = int(input("请输入你想要猜的数:"))
# while cheat != num:
#     if cheat > num:
#         print("太大了")
#     else:
#         print("太小了")
#     cheat = int(input("请输入你想要猜的数:"))
# else:
#     print("有点东西,这都被你猜到了")

# # 打印九九乘法表
# for i in range(1, 10):
#     for j in range(1, i + 1):
#         print(f"{j} x {i} = {i * j}", end = "\t")
#     print()
# 输入十个数并进行排序,输出最大最小平均值
# s = []
# total = 0
# print("请输入十个数")
# for i in range(10):
#     str = int(input(f"第{i + 1}个数:"))
#     s.append(str)
#     total += str
# s.sort()
# print("按大小排序:",s)
#
# print("最小数:",s[0])
# print("最大数:",s[-1])
# print("平均数:",total/len(s))

# s1 = [1, 2, 3]
# s2 = [4, 5, 6]
# s3 = s1 + s2
# s4 = "12345"
# s5 = [*s4]
# s6 = s5.reverse()
# print(s6 == s5)
# print(s3)
#
# # 列表推导式
# # 1-20的平方列表
# list = [i**2 for i in range(1, 21)]
# # print(list)
#
# print(s4.find('6'))

# t1 = (1,2,3,4,5)
# s1, s2, *s3 = t1
# print(s1)
# print(s2)
# print(s3)