# 教务系统开发

print("欢迎进入教务系统")

print("""
############################################################################################################
1.添加学生信息\t2.修改学生信息\t3.删除学生信息\t4.查询学生信息\t5.列出所有学生\t6.统计班级成绩\t7.退出系统
############################################################################################################
""")

op = int(input("请选择你要进行的操作:"))
students = {}

while True:
    match op:
        case 1:
            name = input("学生姓名:")
            if name not in students.keys():
                chinese = int(input("语文成绩:"))
                math = int(input("数学成绩:"))
                english = int(input("语文成绩:"))
                students[name] = {"chinese": chinese, "math": math, "english": english}
                print(f"{students[name]}")
            else:
                print("已存在该学生,请重新输入!")
        case 2:
            name = input("学生姓名:")
            if name in students.keys():
                chinese = int(input("语文成绩:"))
                math = int(input("语文成绩:"))
                english = int(input("语文成绩:"))
                students[name] = {"chinese": chinese, "math": math, "english": english}
            else:
                print("不存在该学生,请重新输入!")
        case 3:
            name = input("学生姓名:")
            if name in students.keys():
                del students[name]
            else:
                print("不存在该学生,请重新输入!")
        case 4:
            name = input("学生姓名:")
            if name in students.keys():
                student = students[name]
                print(f"学生姓名\t语文成绩\t数学成绩\t英语成绩\n{name}\t\t{student["chinese"]}\t\t{student["math"]}\t\t{student["english"]}")
            else:
                print("不存在该学生,请重新输入!")
        case 5:
            for name in students.keys():
                student = students[name]
                print(f"学生姓名\t语文成绩\t数学成绩\t英语成绩\n{name}\t\t{student["chinese"]}\t\t{student["math"]}\t\t{student["english"]}")
        case 6:
            pass
            # for name in students.keys():
        case 7:
            print("退出系统")
            break
        case _:
            print("非法输入!")
    print("""
############################################################################################################
1.添加学生信息\t2.修改学生信息\t3.删除学生信息\t4.查询学生信息\t5.列出所有学生\t6.统计班级成绩\t7.退出系统
############################################################################################################
    """)

    op = int(input("请选择你要进行的操作:"))
