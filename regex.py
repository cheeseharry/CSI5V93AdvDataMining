import re

key = r"javapythonhtmlvhpythondl"#这是源文本
p1 = r"python"#这是我们写的正则表达式
pattern1 = re.compile(p1)#同样是编译
matcher1 = re.search(pattern1,key)#同样是查询
#print(matcher1.group(0))

BP_Flag = False
print(BP_Flag)