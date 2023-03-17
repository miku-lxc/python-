from wxpy import *

####统计好友信息，如身份、城市、性别等
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

