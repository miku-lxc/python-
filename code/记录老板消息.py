
from wxpy import *

###以下是一个职场人自我修养1的代码：利用接受消息然后转发消息，用于保存boss的所发的重要消息。
bot = Bot(cache_path=True)  ##开启缓存不用重新扫码

company_group=bot.groups().search('公司微信群')[0]

boss=company_group.search('boss_name')[0]

@bot.register(company_group)
def forward_boss_message(msg):
    if msg.member == boss:
        msg.forward(bot.file_helper,prefix='老板发言')
embed() #这里是堵塞线程