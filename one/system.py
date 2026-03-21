# 采用面向对象的编程思想，开发一个购物车管理系统，实现商品的添加、修改、删除、查询功能。
# 系统使用自定义对象存储商品数据，通过控制台菜单与用户交互。具体功能如下：
# 1.添加购物车：用户根据提示录入商品名称、以及该商品的价格、数量，保存该商品信息到购物车。
# 2.修改购物车：要求用户输入要修改的购物车商品名称，然后再提示输入该商品的价格、数量，输入完成后修改该商品信息。
# 3.删除购物车：要求用户输入要删除的购物车名称，根据名称删除购物车中的商品。
# 4.查询购物车：将购物车中的商品信息展示出来，格式为：“商品名称： xxx，商品价格： xxx，商品数量： xxx”。
# 5.退出购物车。
# from one.容器 import name


class Shop:
    def __init__(self, name, price, num):
        self.name = name
        self.price = price
        self.num = num

    def __str__(self):
        return f'商品名称：{self.name}, 商品价格：{self.price}, 商品数量：{self.num}'

    def modify(self, price, num):
        self.price = price
        self.num = num


class System:
    def __init__(self):
        self.shops: list[Shop] = []

    def add_shop(self):
        name = input("请输入要添加的商品名称：")
        for s in self.shops:
            if name == s.name:
                print("商品已存在，请重新操作！")
                return
        price = int(input("请输入要添加的价格："))
        num = int(input("请输入要添加的数量："))
        self.shops.append(Shop(name, price, num))

    def modify_shops(self):
        name = input("请输入要修改的商品名称：")
        for s in self.shops:
            if name == s.name:
                price = int(input("请输入要修改后的价格："))
                num = int(input("请输入要修改后的数量："))
                s.modify(price, num)
                return
        print("商品不存在，请重新操作！")

    def del_shop(self):
        name = input("请输入要删除的商品名称：")
        for s in self.shops:
            if name == s.name:
                self.shops.remove(s)
                return
        print("商品不存在，请重新操作！")

    def show_shops(self):
        for s in self.shops:
            print(s)

    def run(self):
        print("欢迎进入购物车操作系统！")
        while True:
            print("1.添加商品 2.修改商品 3.删除商品 4.查询商品 5.退出系统")
            opr = input("请输入你要进行的操作：")
            match opr:
                case "1":
                    self.add_shop()
                case "2":
                    self.modify_shops()
                case "3":
                    self.del_shop()
                case "4":
                    self.show_shops()
                case "5":
                    break
                case _:
                    print("非法输入！")

if __name__ == '__main__':
    system = System()
    system.run()

