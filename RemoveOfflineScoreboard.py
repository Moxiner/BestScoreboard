# 此插件是实现去除离线玩家排行榜，感谢柳姐姐（@WillowSauceR）的帮助与指导！初代版本，很不完善！（希望我还会更新）
import mc
import time
import threading
# ===================配置界面=====================================================================
SocreboardDisplayName = "游戏币"    # 显示计分板游戏内显示内容
SocreboardName = "displaymoney"    # 显示计分板名称（萌新请勿修改，修改时，请查阅此代码，并将其替换！）
socreboardOld = "money"    # SocreboardOld 为 经济计分板名称
Time = 10 # 计分板刷新时间（太短的话，会出现计分板鬼畜）
# ===============================================================================================
# True 为显示 False 为不显示
Socreboardsidebar = True    #  为 右侧计分板 
Socreboardlist = True   #  为 游戏暂停界面计分板
SocreboardBelowname =True    # 为 玩家头顶显示计分板
# ===============================================================================================





# ====================================代码部分======================================================
# 以下内容为代码部分，萌新切勿修改

i = True

def CreatScoreboard(e):
    global i
    if i :
        print("[RemoveOfflineScoreboard][INFO]创建显示计分板....")
        mc.runcmd("scoreboard objectives add %s dummy %s" % (SocreboardName , SocreboardDisplayName)) 
        if Socreboardsidebar :
            mc.runcmd("scoreboard objectives setdisplay sidebar %s" % SocreboardName)
            print("[RemoveOfflineScoreboard][INFO]右侧计分板显示已开启....")
        else :
            print("[RemoveOfflineScoreboard][INFO]右侧计分板显示关闭启....") 
        if SocreboardBelowname :
            mc.runcmd("scoreboard objectives setdisplay belowname %s" % SocreboardName)
            print("[RemoveOfflineScoreboard][INFO]人物头部计分板显示已开启....")
        else :
            print("[RemoveOfflineScoreboard][INFO]任务头部计分板显示已关闭....")
        if Socreboardlist :
            mc.runcmd("scoreboard objectives setdisplay list %s" % SocreboardName)
            print("[RemoveOfflineScoreboard][INFO]暂停界面计分板显示已开启....")
        else :
            print("[RemoveOfflineScoreboard][INFO]暂停界面计分板显示已开启....")
        i = False
    # 刷新计分板
    while True :
        time.sleep(Time)
        mc.runcmd("execute @a ~ ~ ~ scoreboard players operation @s %s = @s %s" % (SocreboardName , socreboardOld))
#负责执行多线程的函数
def newThread(e):
    t = threading.Thread(target=CreatScoreboard, args=(e,)) 
    t.setDaemon(True)
    t.start()


# 删除离线玩家的计分板
def RemovePlayerScore(e) :
    mc.runcmd("scoreboard players reset * %s" % SocreboardName)
    print("[RemoveOfflineScoreboard][INFO]已删除玩家【" + e.name + "】的记分板")
# 屏蔽控制台刷屏通知
def disableCmdOut(e):
    if e[:34] == "Reset score displaymoney of player":
        return False
    elif e[:18] == "Set [displaymoney]" :
        return False
    elif e[:27] == "No targets matched selector" :
        return False
print("===========================================================")
print("[RemoveOfflineScoreboard]已加载...")
print("[RemoveOfflineScoreboard]作者：莫欣儿（Moxiner）")
print("[RemoveOfflineScoreboard]感谢柳姐姐（@WillowSauceR）的帮助与指导")
print("===========================================================")
mc.setListener('onPlayerJoin',newThread)
mc.setListener('onConsoleOutput',disableCmdOut)
mc.setListener("onPlayerLeft",RemovePlayerScore)
