#paramiko 是第三方库要进行安装

import paramiko 

#基于用户名和密码SSHclient进行登录 步骤见代码
#File Name:xxxxxw #文件的名字 看看就行

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



'''使用微信进行告警提醒 ：邮箱提醒有兴趣的可以去看看，在国内微信还是用的蛮多的，可以在微信上发指令对于运维猿来说再好不过了'''



