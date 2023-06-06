import matplotlib.pyplot as plt

# 数据
labels = ['A', 'B', 'C', 'D']
sizes1 = [25, 30, 20, 15]  # 第一层的大小（总和为100%）
sizes2 = [10, 15, 5, 20]   # 第二层的大小（相对于第一层的比例）

# 绘图
fig, ax = plt.subplots()

# 第一层饼状图
wedges1, _ = ax.pie(sizes1, labels=labels, startangle=90)

# 第二层饼状图
wedges2, _ = ax.pie(sizes2, colors=['lightgray', 'lightblue', 'lightgreen', 'lightyellow'],
                    radius=0.7, startangle=90, labeldistance=0.7)

# 添加图例（显示第一层的标签）
ax.legend(wedges1, labels, loc='upper right')

# 设置图形的纵横比为相等，使饼状图成为一个圆形
ax.axis('equal')

# 显示图形
plt.show()
