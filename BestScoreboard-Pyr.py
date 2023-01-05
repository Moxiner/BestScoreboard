
import mc
import json
import time
import os
ConfigName = "BestScoreboard"
ConfigPath = "./plugins/py/" + ConfigName 
j = {
    "Money":"money",
    "DisplayerScore":"displayerMoney",
    "DisplayerName":"金币排行榜",
    "ScoreboardSet":True,
    "Scoreboardsidebar":True,
    "Scoreboardlist":True,
    "ScoreboardBelowname":True,
    "ScoreBoardLog":True
}

# 通知类
class PrintLog:
    '''打印类'''
    def GetTime():
        '''获取当前时间'''
        return time.strftime("%H:%M:%S")

    def InfoLog(concent:str):
        '''弹出 Info 通知
        concent:打印内容
        '''
        print(f"[{PrintLog.GetTime()} Info][{ConfigName}] {concent}")

    def WarmLog(concent:str):
        '''弹出 Warm 通知'''
        print(f"\033[33m[{PrintLog.GetTime()} Warm][{ConfigName} {concent}\033[0m")

    def ErrorLog(concent:str):
        '''弹出 Errror 通知'''
        print(f"\033[31m[{PrintLog.GetTime()} Error][{ConfigName} {concent}\033[0m")

    def TestLog(concent:str):
        '''弹出 Test 通知'''
        print(f"\033[36m[{PrintLog.GetTime()} Test][{ConfigName} {concent}\033[0m")

# 文件类
class Film:
    '''文件操作'''
    def CreateFilm(path:str,name:str):
        '''
        检测文件存在，不存在则创建此文件
        path:文件路径
        name: 文件名称
        '''
        if os.path.exists(f"{path}/{name}"):    
            try:    
                Film.ReadConfig(path, name)     # 顺便读取 Config.json 数据
            except:
                PrintLog.ErrorLog("[code:1] 配置文件发生错误")
                time.sleep(5000)
                exit()
        else:
            if not os.path.exists(path):
                os.makedirs(f"{path}")
            with open(f"{path}/{name}","w+"):
                Film.WriteFilm(path , name, j)    # 顺便写入 Config.json 数据
                try:
                    Film.ReadConfig(path, name)     # 顺便读取 Config.json 数据
                except:
                    time.sleep(5000)
                    PrintLog.ErrorLog("[code:1] 配置文件发生错误")
                    exit()

                PrintLog.WarmLog("检测文件不存在，文件创建完成")
    def WriteFilm(path:str,name:str,concent:dict):
        '''
        写入 json 数据
        path:文件路径
        name: 文件名称
        concent:写入内容
        '''
        j = concent
        with open(f"{ConfigPath}/{name}", "w+") as f:
            oldDate = {}
            oldDate.update(j)
            json.dump(oldDate , f, indent=4)

    def ReadConfig(path:str,name:str):
        '''
        读取 json 数据
        path:文件路径
        name: 文件名称  
        '''
        with open(f"{ConfigPath}/{name}","r") as f:
            j = json.load(f)
            global Money
            global DisplayerScore
            global DisplayerName
            global ScoreboardSet
            global Scoreboardsidebar
            global Scoreboardlist
            global Scoreboardbelowname
            global ScoreboardLog
            Money = j["Money"]
            DisplayerScore = j["DisplayerScore"]
            DisplayerName = j["DisplayerName"]
            ScoreboardSet = j["ScoreboardSet"]
            Scoreboardsidebar = j["Scoreboardsidebar"]
            Scoreboardlist = j["Scoreboardlist"]
            Scoreboardbelowname = j["ScoreboardBelowname"]
            ScoreboardLog = j["ScoreboardLog"]
# 插件主要类
class master:
    def CreateScroe(e):
        '''
        创建必要计分板
        e:MC类属性
        '''
        mc.runCommand(f"scoreboard objectives add {Money} dummy {DisplayerName}")
        mc.runCommand(f"scoreboard objectives add {DisplayerScore} dummy {DisplayerName}")
        master.SetDisplay()

    def SetDisplay():
        '''设置显示计分板模式'''
        if Scoreboardlist:
            mc.runCommand(f"scoreboard objectives setdisplay list {DisplayerScore}")
            if ScoreboardSet:
                PrintLog.InfoLog("暂停界面计分板\t [开启]")
        else:
            mc.runCommand(f"scoreboard objectives setdisplay list")
            if ScoreboardSet:
                PrintLog.InfoLog("暂停界面计分板\t [关闭]")
        if Scoreboardbelowname:
            mc.runCommand(f"scoreboard objectives setdisplay belowname {DisplayerScore}")
            if ScoreboardSet:
                PrintLog.InfoLog("任务头部计分板\t [开启]")
        else:
            mc.runCommand(f"scoreboard objectives setdisplay belowname")
            if ScoreboardSet:
                PrintLog.InfoLog("任务头部计分板\t [关闭]")
        
        if Scoreboardsidebar:
            mc.runCommand(f"scoreboard objectives setdisplay sidebar {DisplayerScore}")
            if ScoreboardSet:
                PrintLog.InfoLog("右侧计分板\t [开启]")        
        else:
            mc.runCommand(f"scoreboard objectives setdisplay sidebar")
            if ScoreboardSet:
                PrintLog.InfoLog("右侧计分板\t [关闭]")
    def ChangeScore(e):
        '''
        刷新计分板
        e:MC类属性
        '''
        player = e["Player"]
        if e["ObjectiveName"] == Money:
            Score =  player.getScore(Money) 
            player.setScore(DisplayerScore , Score)

    def DisplayerScore(e):
        '''
        显示计分板
        e:MC类属性
        '''
        player = e["Player"]
        Score =  player.getScore(Money) 
        player.setScore(DisplayerScore , Score)
        if ScoreboardLog:
            PrintLog.InfoLog(f"已显示玩家 {player} 的计分板")


    def HiddenScore(e):
        '''
        隐藏计分板
        e:MC类属性
        '''
        player = e["Player"]
        mc.runCommand(f"scoreboard players reset {player} {DisplayerScore}")
        if ScoreboardLog:
            PrintLog.InfoLog(f"已隐藏玩家 {player} 的计分板")

    def HiddenConsoleLog(e):
        '''
        拦截不必要控制台输出
        e:MC类属性 
        '''
        output = e["Output"][:-1]
        if output == f"Set the display objective in slot 'sidebar' to '{DisplayerScore}'":
            return False
        elif output == f"Set the display objective in slot 'belowname' to '{DisplayerScore}'":
            return False
        elif output ==  f"Set the display objective in slot 'list' to '{DisplayerScore}'":
            return False
        elif output == f"An objective with the name '{Money}' already exists":
            return False
        elif output == f"An objective with the name '{DisplayerScore}' already exists":
            return False
        elif output[:len(f"Reset score {DisplayerScore} of player")] == f"Reset score {DisplayerScore} of player":
            return False
# 初始化配置文件
Film.CreateFilm(ConfigPath , "config.json")
# 一堆监听器
mc.setListener("onScoreChanged", master.ChangeScore)
mc.setListener("onServerStarted", master.CreateScroe)
mc.setListener("onJoin", master.DisplayerScore)
mc.setListener("onLeft", master.HiddenScore)
mc.setListener("onConsoleOutput" , master.HiddenConsoleLog)
# 控制台输出
PrintLog.InfoLog("已加载  v1.4")
PrintLog.InfoLog("作者：莫欣儿（Moxiner）")