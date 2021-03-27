# history.txt  ->  history.html


# <p>
#     <div style="display:inline;color: darkgray;">
#         行号&nbsp;&nbsp;
#     </div>
#     <div style="display:inline;">
#         文字
#     </div>
# </p>

# <p><div style="display:inline;color: darkgray;">行号&nbsp;&nbsp;</div><div style="display:inline;">文字</div></p>

# 定义格式
str1 = "<p><div style=\"display:inline;color: darkgray;\">"
str2 = "&nbsp;&nbsp;</div><div style=\"display:inline;\">"
str3 = "</div></p>"

#读取
with open("history.txt",'r',encoding='utf-8') as f:
    h_raw = f.readlines()

# 转换
no = 1
h = []
for line in h_raw:
    line = line[:-1]
    h.append(''.join([str1,str(no),str2,line,str3]))
    no += 1

# 写入
with open("history.html","w+",encoding='utf-8') as f:
    for i in h:
        f.write(i)