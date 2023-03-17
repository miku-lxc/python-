import subprocess
from wxpy import *

bot = Bot()
admin = bot.friends().search("xxx")[0]

def remote_shell(command):
    r = subprocess.run(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
    )
    if r.stdout:
        yield r.stdout
    else:
        yield "ok"

def send_iter(receiver, iterable):
    '''
    用迭代的方式发送多条信息
    :param receiver: 接受者
    :param iterable: 可迭代对象
    '''
    if isinstance(iterable,str):
        raise TypeError
    
    for msg in iterable:
        receiver.send(msg)
@bot.register()
def server_mgmt(msg):
    '''
    r若消息文本以！开头，则作为shell命令去执行,可以自行调控哈哈哈哈
    '''
    print(msg)
    if msg.chat == admin:
        if msg.text.startswitch("!"):
            command=msg.text[1:]
            send_iter(msg.chat,remote_shell(command))
#进入阻塞，可以在命令行调试
embed()
