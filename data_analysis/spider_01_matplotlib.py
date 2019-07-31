# coding:utf-8
import numpy as np
import matplotlib.pyplot as plt
from pylab import *
import tensorflow as tf

# # 直线图
# x = [0, 1]  # x轴
# y = [0, 1]  # y轴
# plt.figure()  # 创建绘图对象
# plt.ylabel('ACC@1', size=20)  # y轴的坐标 size为字体大小
# plt.xlabel('Iters', size=20)  # x轴的坐标
# plt.title('line', size=30)  # 标题
# plt.plot(x, y, linewidth=3, c='r')  # 在当前对象进行绘图,c为颜色,linewidth为线的宽度
# plt.savefig("1.png")  # 将图像保存下来 ==> savefig()和save()先后顺序
# plt.show()  # 将当先图像显示出来

# # 折线图
# x = [0, 1, 2, 3, 4, 5, 7]
# y = [0.3, 0.4, 5, 5, 3, 4.5, 4]
# plt.figure(figsize=(8, 4))  # 创建绘图对象
# plt.plot(x, y, "b--", linewidth=1)  # 在当前绘图对象绘图（X轴，Y轴，蓝色虚线，线宽度）
# plt.xlabel("Time(s)")  # X轴标签
# plt.ylabel("Volt")  # Y轴标签
# plt.title("Line plot")  # 图标题
# plt.savefig("折线图.png")  # 保存图
# plt.show()  # 显示图

# # 画两条线
# # mpl.rcParams['font.sans-serif'] = ['SimHei']
# plt.rcParams['xtick.direction'] = 'in'#刻度在象限内部
# plt.rcParams['ytick.direction'] = 'in'
# names = [0.1,0.2,0.3,0.5,0.8,1]
# x = range(len(names))
# y =  [0.476, 0.475, 0.475,0.474,0.473, 0.468]
# y1 = [0.674, 0.671, 0.682,0.681,0.684,0.686]
#
# #plt.plot(x, y, 'ro-')
# #plt.plot(x, y1, 'bo-')
# #pl.xlim(-1, 11)  # 限定横轴的范围
# plt.ylim(0.45, 0.7)  # 限定纵轴的范围
# plt.tick_params(labelsize=13)
#
# plt.plot(names, y, 'r--',linewidth = 3,label='ACC@1')
# plt.plot(names, y1, 'b--',linewidth = 3,label='ACC@5')
#
# plt.legend(loc=0, numpoints=1)
# leg = plt.gca().get_legend()
# ltext = leg.get_texts()
# plt.setp(ltext, fontsize=15)   # 让图例生效，fontsize的含义是坐标刻度字体的大小
# # plt.xticks(x, names, rotation=100)#rotation在此处是说左边刻度的倾斜程度
# plt.margins(0)
# plt.subplots_adjust(bottom=0.15)
# plt.xlabel("$\\alpha$",size=18) #X轴标签，希腊字母的表示方式要加\\
# plt.ylabel("ACC",size=18) #Y轴标签
# # plt.title("A simple plot") #标题
# plt.savefig('alpha.eps')
# plt.show()

# # 柱状图
# name_list = ['1', '2', '3'] # 表示一共有几个柱
# num_list = [574.0, 320.0, 400]  # 每一个柱体的高度(Y轴自动分配)
# plt.bar(range(len(num_list)), num_list, color='rgb',width=0.2, tick_label=name_list) #width来调整柱的宽度 color来设置颜色
# plt.savefig('柱状图.png')
# plt.show()

# data = np.array([1, 2, 3, 4, 5, 6, 7])
# index = [1, 2, 3, 4, 5, 6, 7]
# plt.barh(y=index, height=0.5, width=data)
# plt.savefig('weight.png')

# # 散点图
# x_values = [1, 2, 3, 4, 5]
# y_values = [1, 4, 9, 16, 25]
#
# plt.scatter(x_values, y_values, s=100)  # s为点的大小
# plt.title("Scatter pic", fontsize=24)  # 设置图表标题并给坐标轴加上标签
# plt.xlabel("Value", fontsize=14)
# plt.ylabel("Scatter of Value", fontsize=14)
# plt.tick_params(axis='both', which='major', labelsize=14)  # 设置刻度标记的大小
# plt.savefig('散点图.png')
# plt.show()

# 饼图
"""
labels：设置每一块的标签； 必须一一对应，不能是中文
labeldistance：设置标签距离圆心的距离（0为 圆饼中心数 1为圆饼边缘）
autopct：设置比例值的显示格式(%1.1f%%)保留一位小数的百分比；
pctdistance：设置比例值文字距离圆心的距离（浮点值）
explode：设置每一块顶点距圆心的长度（比例值,列表）；
colors：设置每一块的颜色（列表）；最好一一对应
shadow：设置是否绘制阴影，默认为False
startangle：设置饼图起始角度 正右方为0度
"""
# x = [89, 45, 32, 16]
# plt.pie(x)
# plt.savefig('饼图')
# plt.show()

# x = [89, 45, 32, 16]
# plt.pie(x,
#         labels=['A', 'B', 'C', 'D'],
#         labeldistance=1.2,
#         autopct="%1.1f%%",  # 1.1f% 保留一位小数的百分比
#         pctdistance=0.5,  # 比例值文字距离圆心的距离
#         explode=[0, 0.2, 0, 0],  # 每一块顶点距圆形的长度
#         colors=["red", "blue", "yellow", "green"],  # 最好一一对应
#         shadow=True,  # 是否有阴影
#         startangle=60  # 第一块开始的角度
#         )
# plt.savefig('饼图参数')
# plt.show()