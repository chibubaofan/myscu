import csv
import os
import re
def idandcom(file,id):
    item_list=[]
    with open(file, mode='r',encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)#跳过首行
        for row in csv_reader:

            if len(row)==5:
                item=[row[0],row[1]]
                item_list.append(item)
                r_data=row[4]
                r_data =r_data.replace(" ", "")
                r_list=r_data.split("],[")


                for reply in r_list:
                    reply=reply.replace('[','')
                    reply = reply.replace(']', '')
                    reply=reply.split(",")

                    item=[reply[0],reply[1]]
                    item_list.append(item)



            elif len(row)==4:
                item=[row[0],row[1]]
                item_list.append(item)
            else:
                continue
    loc=f"./commentstwo/simplify/{id}.txt"
    with open(loc,mode='w',encoding='utf-8') as f:
        for item in item_list:
            f.write(" ".join(item)+"\n")

    print(f"处理完了{file}")


def all(file,id):
    item_list=[]
    title=None
    flag=1
    with open(file, mode='r',encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            title=row
            break
        next(csv_reader)
        for row in csv_reader:

            if len(row)==5:
                item=row[0:4]
                item_list.append(item)
                r_data=row[4]
                r_data =r_data.replace(" ", "")
                r_list=r_data.split("],[")


                for reply in r_list:

                    reply=reply.replace('[','')
                    reply = reply.replace(']', '')
                    reply=reply.split(",")

                    item=reply[0:4]
                    item_list.append(item)



            elif len(row)==4:
                item=row[0:4]
                item_list.append(item)
            else:
                continue
    loc=f"./commentstwo/simplify_all/{id}.txt"
    with open(loc,mode='w',encoding='utf-8') as f:
        f.write(str(title[0]).replace("\'",'')+'\n')
        for item in item_list:
            item[-1]=item[-1].replace(" ","")
            f.write(" ".join(item).replace("\'","")+"\n")

    print(f"处理完了{file}")

def user_all(file,id):
    dict={}
    with open(file, mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            item_list = row[1:]
            if len(row)<4:
                print("数据错误，跳过一个")
                continue
            if row[3] not in dict:
                newdata={f"{row[3]}":item_list}
                dict.update(newdata)

    return dict





def merge(file,id):
    userdict=user_all(file,id)
    file2=f".\\commentstwo\\simplify_all\\{id}.txt"
    with open(file2,mode='r',encoding='utf-8') as f:
        next(f)
        for line in f:
            line=line.strip()
            line=line.split(" ")
            if len(line)<3:
                print("没东西下一个")
                continue
            if len(line)>4:
                com="，".join([line[i] for i in range(len(line)-3)])
                line=[line[i] for i in range(len(line)-3,len(line))]
                line.insert(0,com)
            uid=line[1]
            ulist=None
            try:
                ulist=userdict[f"{uid}"]
            except KeyError as ex:
                print(str(line))
                print("出现错误，放弃一个")
                continue
            if len(ulist)==20:
                if len(line)<4:
                    line.append("未知")
                userdict[f"{uid}"].append(line[2])
                userdict[f"{uid}"].append(line[3])
                userdict[f"{uid}"].append(line[0])
            else:
                com="".join([userdict[f"{uid}"][-1],line[0]])
                userdict[f"{uid}"][-1]=com
        values=userdict.values()
        with open(f"./{id}finals.txt",mode='w',encoding='utf-8') as f:
            for l in values:
                newl=["empty" if x=="" else x for x in l]
                f.write(" ".join(newl)+"\n")
            print("finish1!"*10)
def final():
    base_dir = ".\\userstwo\\userid_with_info"
    files = [os.path.join(base_dir, file) for file in os.listdir(base_dir)]
    for file in files:
        if os.path.isfile(file):
            id = file.split("\\")[3]
            id = re.search("\d+", id).group()
            merge(file, id)

def detect():
    total_list=[]
    with open("total.txt",mode='r',encoding='utf-8')as f:
        for line in f:
            line = line.strip()
            line = line.split("\t")
            if len(line)==2:
                s=''.join(line)
                item=[]
                if not s.isdigit():
                    continue
                label=s[-1]
                s=s[:-1]
                id=re.search('\d+',s)
                s=s.replace(id.group(),'')
                item.append(id.group())
                item.append(s)
                item.append(label)
                total_list.append(item)
                # print(str(line[0]))
                # print(str(line[1])+'\n')
            elif len(line)==3:
                total_list.append(line)
            else:
                s=''
                for i in range(1,len(line)-1):
                    s+=line[i]
                item=[line[0],s.replace("	",''),line[-1]]
                total_list.append(item)


        with open("total2.txt",mode='w',encoding='utf-8') as f:
            for item in total_list:
                f.write("	".join(item)+'\n')

def detect2():
    with open("total2.txt", mode='r', encoding='utf-8') as f:
        for line in f:
            s=line.split("	")
            if len(s)!=3:
                print("error")
if __name__ =="__main__":
    detect2()
    # final()
    # base_dir = ".\\userstwo\\userid_with_info"
    # files = [os.path.join(base_dir, file) for file in os.listdir(base_dir)]
    # for file in files:
    #     if os.path.isfile(file):
    #         id = file.split("\\")[3]
    #         id = re.search("\d+", id).group()