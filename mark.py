from selenium import webdriver
import os
import re

def open_user_page(id):
    options = webdriver.EdgeOptions()
    options.add_experimental_option('detach', True)
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0')
    driver=webdriver.Edge(options)
    driver.get(f"https://www.toutiao.com/c/user/{id}/")
    flag=int(input().replace("\n",''))
    driver.quit()
    return flag

def mark_file(file,id):
    index=0
    if os.path.exists(f"./{id}finalsindex.txt"):
        with open(f"./{id}finalsindex.txt",mode='r',encoding='utf-8') as f:
            index=int(f.read())
    count=0
    start=0
    set_list=[]
    try:
        with open(file,mode='r',encoding='utf-8') as f:
            for line in f:
                if start<index:
                    start+=1
                    continue
                line=line.strip()
                l=line.split(" ")
                print("评论："+l[-1]+"\nIP："+l[-2]+"\n是否有合集："+l[-7]+"\nhot比例："+l[-8]+"\n互动比例："+l[-10]+"\n原创比例："+l[-11]+"\n全部发布数："+l[4])
                l.append(open_user_page(l[2]))
                set_list.append(l)
                count+=1
    finally:
        with open("./finalset.txt",mode='a+',encoding='utf-8') as f:
            for l in set_list:
                f.write(" ".join(str(i) for i in l)+'\n')
        with open(f"./{id}finalsindex.txt",mode='w',encoding='utf-8') as f:
            f.write(str(index+count))




def mark_all():
    base_dir = ".\\"
    files = [os.path.join(base_dir, file) for file in os.listdir(base_dir)]
    for file in files:
        file_extension = os.path.splitext(file)[1]
        if file_extension == '.txt':
            id = file.split("\\")[1]
            id = re.search("\d+", id).group()
            mark_file(file,id)







if __name__ == "__main__":
    mark_all()
    # open_user_page(1138700707168683)