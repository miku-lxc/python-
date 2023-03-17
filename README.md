# python-

重大说明

#此部分为python基础运维的部分 对一些基础运维做了一些实践 ，主要是远程paramio非常适用。

#代码中有wxpy 不建议大家去用wxpy因为微信web的登录方式被封了，这里只作为学习和记录吧，真的花了好长时间去做这个，结果发现该库64行代码报错：weixi关闭了web的登录方式

逻辑框架：

  1.code文件夹：
  
    分为三个部分：
    
    1.1 wxpy的实现代码（现已不能用） 
    
    1.2 远程连接.py 代码实现了隐藏用户信息的功能使用了configparser进行实现，并制作相应的方法函数。实现远程云主机的互联
    
    1.3 1.py里面主要是边学习和边实践，里面有讲到一些方法论。我觉得这是计算机人比较好的学习方法：所用即所查
    
    1.4 本次基础运维主要实现了其他几个库：subprocess psutil sys等 涉及文本处理、系统信息监控、日志记录、微信提醒
    
  
  2.详细代码见下
  
   主页面只作为展示，可能代码不整齐，详细请见code目录下的1.py
  
  
  
  
  
  
具体代码以及相应的笔记实现：



#此为文本处理的实践代码

import sys

#encoding=utf-8 
#注意事项：虽然python对单双引号 不敏感。但是作为接触到shell的来说，要特别注意了，shell里面单引是按str处理的，变量默认不生效，双引才生效
#这段代码放在开头，时刻提醒我这是python3 不是python2.7！！
#print("这是你的python版本：",sys.version)

#文件处理
#处理的流程，创建一个句柄，进行操作、关闭文件。三个步骤缺一不可，最后一项一定要关闭，不然会导致文件占用。
#open()函数的注意事项：mode参数可以接r读默认的 w写不建议用这个会清除。a追加可用。x以读和写进行更新可用。其余mode看看就行
'''
f = open('a.txt')
print(f.read())
f.close()
'''

#上面是使用的是open函数，接下来使用with 。。。as ,如果换mode为r则不能写，只有open中换对应的mode为a写才能进行write写入

'''
with open("a.txt",'r') as f1:
#    f1.write("this a new test")
    f1.close()
'''

##大文件读写，可以使用f。read（），读取所有，但是后果容易造成内存溢出，所以选择f.readline()读取一行 ，这里扩展下f.readlines() 在前者的基础上加入列表
##大文件最佳处理的方式：是利用读取一行进行迭代处理
import os
'''
with open('miku.txt','r') as read_f2,open('a.txt','a') as write_f2:
    for line in read_f2: 
        line = line.replace('str1','str2') ##不要少写代码的字母，否则呀会替换不生效
        write_f2.write(line) 
os.remove('miku.txt')
os.rename('a.txt','a.txt.bak') 
'''

#处理大数据还有readline方法，以及利用true往read里加一次读取指定的字符
'''
fb = open('b.txt') 
while True:
    block=fb.read(1)
    print(block)
    if not block:
        break

#很明显里面有空格也是算行的
fb = open('b.txt') 
while True:
    block=fb.readline()
    print(block)
    if not block:
        break
'''


'''
##对文件的函数说明：
file.close() 
file.next() 返回文件下一行
file.seek() 可以实现类似tail -f的功能
file.write('str') 写入字符串到文件 ，这几种都是在open下具柄的，记住模式的不同是非常重要的，否则影响这些命令的执行。
'''

'''
##读写配置文件,可以将文件隐藏，很适合读取加密隐藏信息的场景呀
'''
#内置代码 configparse 模块
import configparser
'''
#encoding=utf-8 此代码设置中文，有时候python不支持中文字符，需要加这个
#print("我是你吗?") 
import configparser
config = configparser.ConfigParser() #实例化方法
config.read(r'key.txt')
print('遍历信息')
for section in config.sections():
    print(f'section is [{section}]')  #这也是一种呢格式化的显示方式要常用
    for key in config[section]:
        print(f'key is [{key}],values is [{config[section][key]}]')
print('this is key.txt')
print(f'{config[section][key]}')
print(f'{section}')
###此处代码适用于后面的远程命令，可以一起搭配1的使用。
'''

###上面是读取，现在让我们来进行write吧
#上面有一些实列了。我们稍微1借用一下吧
config1 = configparser.ConfigParser()
config1["meassage"] = {
    "your_name" :"miku",
    "your_sex" : "feamle",
    "your_role" : "she is first in the word",
}
##此处是一处写入方式，其实已经满足了需求，下面是另外几种写入方式

config1["user_meassage"] = {}       ###等号后边加了一个{}代表的是一个tile 而充当vlaue时需要为str
config1["user_meassage"]["dsad"] = "vdas"
config1["user_meassage"]["port"] = "9000"
#这也是一种写法，先写tile，属于的就挨着tile写，下面是上面的变形，实际上只是将tile进行变量化而已，tile区分大小写注意了，而里面的不需要区分
miku0 = config1["user_miku"] = {}
miku0["name"] = "初音未来"
miku0["text"] = "她是二次元们宅宅的偶像，一个虚拟人物，在未来他是可以成为现实的，因为openAI发布的chatgpt"
'''文本处理中的mode强烈注意了，有些mode不能单独使用，但是+提供了多种联合，r w a “+” 是可以一起使用的，实现了既读取又是写入等的操作牛'''
with open("config.txt",'w+') as configfile:  
    config1.write(configfile)
    configfile.close()  
##自己测试了下，不能带w的mode下面进行显示读取，读取不来，只能用下面的代码
'''  
with open("config.txt",'r') as f1:
    print(f1.read())
    f1.close()    
'''

'''信息系统监控:可以看使用的cpu内存占用啥1的，就是linux中的top ps 等对应的功能'''
import psutil  #这个不属于标准库，所以要用pip3进行安装 pip3 install psutil
'''
#大致说一下吧，剩余的方法详细请看vs code自己操作下。然后关于计算机人的学习方法论：用即学习，要符合客观规律，白看百练习方能生巧和记忆。符合大脑的记忆原理！！另外关于每个方法都有对应的英文缩写，看缩写就知道是干什么。所以外语很重要，赶紧去学习吧。
#cpu相关的
print(psutil.cpu_times())
print(psutil.cpu_times(percpu=True)) #里面指定的参数代表的是开启详细的信息 
#这里说明下。vscode比xcode对于python来说，确实好用，会自动弹出相对应的方法，而且支持多文件的运行，不用像xcode那样一直要设置运行文件。点赞！！
print(psutil.cpu_count())
#内存
print(psutil.virtual_memory())
#磁盘
print(psutil.disk_partitions())
#网络
print(psutil.net_if_addrs())
#进程
#print(psutil.pids()) #获取进程信息不建议用这个进行查询，原因和前面的一样数量太多会溢出的，所以选择用迭代
for pid in psutil.pids():
    print(pid,end='')
'''

'''文件系统的监控:使用的是watchdog库，不是标准库是一个第三方的库所以需要pip3一下：其原理是通过操作系统的事件触发，不需要循环，也不需要等待'''


'''
#import watchdog 可以看下python的部分导入和完全导入的区别，怎么用的都是可以看一下的
from watchdog.observers import Observer
from watchdog.events import *
import time

class FileEventHandler(FileSystemEventHandler):  #创建一个类 在类中写出方法定义函数，这比java好多了，java还有继承啥啥的，指定类型啥的
    def __init__(self) :   #def后面一定要加空格，不然它是会报错的，在vscode明显可以看出来的
        FileSystemEventHandler.__init__(self)

    def on_moved(self, event):
        now = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
        if event.is_directory:
            print(f'{now} 文件夹由{ event.src_path } 移动至 { event.dest_path }')
        else:
            print(f'{now} 文件夹由{ event.src_path } 移动至 { event.dest_path }')

    def on_ceated(self, event):
        now = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
        if event.is_directory:
            print(f'{now} 文件夹由{ event.src_path } 创建')
        else:
            print(f'{now} 文件{ event.src_path } 创建')

    def on_deleted(self,event):
        now = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
        if event.is_directory: # 用于判断是否是文件还是目录 这是判断是不是目录
            print(f'{now} 文件夹由{ event.src_path } 删除')
        else:
            print(f'{now} 文件{ event.src_path } 删除')

    def on_deleted(self,event):
        now = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
        if event.is_directory:
            print(f'{now} 文件夹由{ event.src_path } 修改')
        else:
            print(f'{now} 文件{ event.src_path } 修改')
 

if __name__ == "__main__":
    observer = Observer() #创建一个实例
    path = r"/Volumes/SYSTEM/windos/python train/python3" 
    #z这里说明下我用的是mac。mac是非常好用的结合vscode直接输入linux相关命令就可以获取到东西，mac本身就是uinx为原型搭建的。比如路径pwd比windos好用多了。
    event_handler = FileEventHandler()
    observer.schedule(event_handler,path,True) # True 表示的是递归子目录
    print(f"你现在的监控目录是 {path}") 
    observer.start()
    observer.join()
    ###写完了，不出意外代码报错了，所以要去排查，不是谁的代码都是一番风顺的。仔细细致，有错误才能学到更多。146和176没有加（）导致错误细节决定成败

'''


####执执行外部命令，这个模块h还是很不错的很实用。是python的内置库 subprocess 

'''首先来看下subprocess.run()方法 官方推荐的强调一遍 '''
'''
#函数原型 ：subproces.run('args命令'，stdin=None ,input=None,stout=None,shell=False（代表着程序是否需要在shell中执行，一旦开启。可以使用shell的命令还是很好的，如管道啥的）)
import subprocess
a=subprocess.run('ls -l a.txt.bak',shell=True) ##这里说明下，不用printf也能直接显示出来，相当于你直接敲了ls命令
#直接使用第一种要比第二种好，符合运维人呀哈哈哈哈
b=subprocess.run(['ls','l','b.txt'])
#print(a)
#print(a.args)  #可以指出你输入的命令是啥
#pepen类暂时不做解说，深入，大家有兴趣其实可以去看看的，里面有很多参数
'''

###涉及外部指令了。以及前面的cngfig编写，不得深入学习下远程命令，这是说不过去的。备注下执行远程命令属于高级运维范畴啥的，工具就是工具，好用效率高就行
'''
所使用的库是，paramiko：其中的类做些说明：1.通道类 2.传输类 3.SSHclient类
具体的解释如下：
通道是ssh2 channel的抽象类，ssh的安全传输通道 和嵌套字是类似的。close() exec_command(*args,**kwds) exit_status_ready() recv_exit_command 
传输是核心实现类 ，ssh传输连接到流，通常是套接字（关于套接字网络编程那部门有可以去百度一下或者维基百科）  协商加密会话 身份验证 创建流隧道 多夸通道 多路复用 方法有 send() recv(int) close() settimeout(n)  关于意思是啥自己看英文大概就猜到了，不会英文就去学
既然说到这里了。那就插一嘴：关于英语学习，我觉得不能是应试教育，你因该符合你身体的意志，将英语作为日常，让大脑觉得你需要英语才能活下去，才能生存，激发大脑的学习欲望，这样学习才会化为主动学习，而不是天天abandon，只会记忆不会去运用。导致不容易记忆，沉静式学习记单词是非常快的。
SSHclient,使用ssh的高级形式，将上述的类进行包装，处理验证和打开通道。connect exec_command recv_exit_status()
paramiko的使用
'''
#paramiko 是第三方库要进行安装

import paramiko 

#基于用户名和密码SSHclient进行登录 步骤见代码
#File Name:xxxxxw #文件的名字 看看就行

'''
#下面是回顾的代码插入的
def mima():
    import configparser
    config = configparser.ConfigParser() #实例化方法
    config.read(r'key.txt')
    for section in config.sections():
       # a=section  #遍历setcion也就是ttile 有了这个再去便利里面的值
        for key in config[section]:
            b1=key
            b2=config[section][key] 
#我文件中的写法是section内的 user = passwd
    return [key,config[section][key]]
#   print(f'{config[section][key]}')
#    print(f'{section}')
###方法有点绕，这是我目前思考的解决方式，首先定义函数，对其进行遍历。得出想要的值，以列表反回然后进行读取
#print(type(mima())) #看看类型
#print(mima())
my_user=mima()[0]
my_passwd=mima()[1]
##使用config进行隐藏密码 ：密码方式脚本key。txt
#这才是本节的paramiko代码
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname="www.XXX.top",username=my_user,password=my_passwd)  ##www.XXX.top 是我的云主机

stdin,stdout,stderr = ssh.exec_command("echo `date` && ls -ltr")
print(stdout.read().decode("utf-8"))
returncode = stdout.channel.recv_exit_status()  ###这一句要结合起来做显示的
print(r"returncode:[{returncode}]")

stdin,stdout,stderr = ssh.exec_command("cd /miku && ls -l")
print(stdout.read().decode("utf-8"))
returncode = stdout.channel.recv_exit_status()  ###这一句要结合起来做显示的,是可以直接显示的，不过是吧上慢的命令结果进行存入显示
#print(r"returncode:[{returncode}]")
ssh.close()
'''


'''使用微信进行告警提醒 ：邮箱提醒有兴趣的可以去看看，在国内微信还是用的蛮多的，可以在微信上发指令对于运维猿来说再好不过了'''
#微信小程序所使用的库是wxpy 我们采用豆瓣源进行安装：pip3 install -U wxpy -i ‘https://pypi.doubanio.com/simple’
#import wxpy   #这里导入包不彻底 ，建议大家去查一下关于 上面和下面的from的区别
''' 区别如下：一个全局一个更加精细
import 模块：导入一个模块；注：相当于导入的是一个文件夹，是个相对路径。
from…import：导入了一个模块中的一个函数；注：相当于导入的是一个文件夹中的文件，是个绝对路径
'''
from wxpy import *  

bot = Bot(cache_path=True)  ##开启缓存不用重新扫码
myself = bot.self
bot.self.add()
bot.self.accept()
bot.self.send("can you revice?")
bot.file_helper.send("hello,file_hellper")
bot.enable_puid("wxpy_puid.pkl")
my_friend=bot.friends().search("123")[0] ##[0] 代表的是附加条件

print(my_friend.puid)

my_friend=bot.friends().search(puid="puid")[0]
my_friend.send("hello,my friend")
my_friend.send_video("dir")
my_friend.send_file("dir")
my_friend.send("@img@my_picture.png")
my_friend.send_image("dir")

my_group=bot.groups().search("group_name")[0]
my_group.send("hello")
my_groups= bot.groups().search("group_name",[my_friend])   ##查找群名为goup——name，并且my_friend的群


###接受信息、自动回复、转发消息功能的实现
@bot.register()
def save_msg(msg):
    print(msg)
@bot.register(Friend)
def save_msg(msg):
    print(msg)
    Tuling().do_reply(msg)   ##调用wxpy自带的机器人，也可添加自己的api接口


'''
###以下是一个职场人自我修养1的代码：利用接受消息然后转发消息，用于保存boss的所发的重要消息。
bot = Bot(cache_path=True)  ##开启缓存不用重新扫码

company_group=bot.groups().search('公司微信群')[0]

boss=company_group.search('boss_name')[0]

@bot.register(company_group)
def forward_boss_message(msg):
    if msg.member == boss:
        msg.forward(bot.file_helper,prefix='老板发言')
embed() #这里是堵塞线程
'''

'''
#####统计好友信息，如身份、城市、性别等
bot=Bot(cache_path=True)
friends_stat = bot.friends().stats()

friend_loc = [] #每一个元素都是一个二元列表，分别存储地区和人数信息
for provinice,count in friends_stat["province"].items():
    if provinice != "":
        friend_loc.append([provinice,count])

#对人数进行倒数排序
friend_loc.sort(key=lambda x:x[1],reverse=True)

#打印前10
for item in friend_loc[:10]:
    print(item[0],item[1])

'''

