import pickle, os, const, sys, io, logging
from tkinter import filedialog, messagebox

# 创建一个io.StringIO对象来保存标准错误输出
error_output = io.StringIO()
# 重定向标准错误输出到error_output对象
sys.stderr = error_output
# 在这里执行你的代码，任何错误信息都会被保存到error_output中

if os.path.exists("班级学员名单.csv"):
    with open("班级学员名单.csv", "r", encoding='utf-8') as f:
        raw_data = f.readlines()
        
    class_dict = {}
    for i in raw_data:
        data = [i for i in i.replace("\n", "").replace(" ", "").replace("：", ":").split(",") if i!=""]
        cname = data.pop(0)
        class_dict[cname] = data



# class_list = [
#     51830: ["史锦曦", "奚子洋", "孙尚璟", "王振豪", "杨曦文"]),
#     61045: ["沈亦瑈", "姚梓芃", "徐志轩", "倪佳诚", "enzo", "费熙宸"]),
#     61300: ["陈祺然", "许家豪", "张霆琛", "计莹宸", "李晨瑶"]),
#     61445: ["金智轩", "傅宇阳", "曹韵泽", "许明浩", "朱苗荻"]),
#     61630: ["王子轩", "杨思涵", "金玮", "钟行易", "徐思齐", "赵千博", "王子敬"]),
#     70900: ["陈亦坤", "沈彦儒", "沈炜翔", "高涵宇", "张隽巍", "李致远"]),
#     71045: ["刘昊宸", "蔡秉桓", "庄子霄", "别家旭", "彭木铎", "陈梓萱", "周晟朗", "王楷煊"]),
#     71300: ["coco", "尹硕辰"]),
#     71630: ["孙慕丰", "孙子轩", "王子熠", "费毅浩", "姚诗茜", "jerry", "董亦宇"])
# ]

# class_dict = {
#     51830: ["史锦曦", "奚子洋", "孙尚璟", "王振豪", "杨曦文"],
#     61045: ["沈亦瑈", "姚梓芃", "徐志轩", "倪佳诚", "enzo", "费熙宸"],
#     61300: ["陈祺然", "许家豪", "张霆琛", "计莹宸", "李晨瑶"],
#     61445: ["金智轩", "傅宇阳", "曹韵泽", "许明浩", "朱苗荻"],
#     61630: ["王子轩", "杨思涵", "金玮", "钟行易", "徐思齐", "赵千博", "王子敬"],
#     70900: ["陈亦坤", "沈彦儒", "沈炜翔", "高涵宇", "张隽巍", "李致远"],
#     71045: ["刘昊宸", "蔡秉桓", "庄子霄", "别家旭", "彭木铎", "陈梓萱", "周晟朗", "王楷煊"],
#     71300: ["coco", "尹硕辰"],
#     71630: ["孙慕丰", "孙子轩", "王子熠", "费毅浩", "姚诗茜", "jerry", "董亦宇"]
# }

with open("class_data.dat", "wb") as f:
    pickle.dump(class_dict, f)
    
random_data = {}

with open("random_data.dat", "wb") as f:
    pickle.dump(random_data, f)

messagebox.showinfo("成功", "更改成功！")

# 恢复标准错误输出
sys.stderr = sys.__stderr__
# 获取保存的错误信息
error_message = error_output.getvalue()
# 打印错误信息
logging.error(error_message)


