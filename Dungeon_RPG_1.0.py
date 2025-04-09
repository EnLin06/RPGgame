import random as rd
import pygame as py
import sys
import json

#初始化
py.init()
screen = py.display.set_mode((800,550))
py.display.set_caption("An_Adventure_RPG")

#背景導入 & 設定
bg = py.image.load("image/bg1.jpg")
bg = py.transform.scale(bg, (800, 200))
def bgset(newbg):
    global bg
    bg = py.image.load(newbg)
    bg = py.transform.scale(bg, (800, 200))

#設定顏色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

# 字型設定
font = py.font.Font("Cubic_11.ttf", 24)
titlefont = py.font.Font("Cubic_11.ttf", 72)
m_menufont = py.font.Font("Cubic_11.ttf", 36)
# 選擇清單類別
class Menu:
    def __init__(self, options, x, y):
        self.options = options
        self.index = 0
        self.x = x
        self.y = y

    def draw(self, screen):
        for i, option in enumerate(self.options):
            if i == self.index:
                color = GREEN 
            else:
                color =  WHITE
            text_surf = font.render(option, True, color)
            screen.blit(text_surf, (self.x, self.y + i * 30))

    def move_selection(self, direction):
        if direction == "up":
            self.index = (self.index - 1) % len(self.options)
        elif direction == "down":
            self.index = (self.index + 1) % len(self.options)

class titleMenu:
    def __init__(self, options, x, y):
        self.options = options
        self.index = 0
        self.x = x
        self.y = y

    def draw(self, screen):
        for i, option in enumerate(self.options):
            if i == self.index:
                color = GREEN 
            else:
                color =  WHITE
            text_surf = m_menufont.render(option, True, color)
            screen.blit(text_surf, (self.x, self.y + i * 70))

    def move_selection(self, direction):
        if direction == "up":
            self.index = (self.index - 1) % len(self.options)
        elif direction == "down":
            self.index = (self.index + 1) % len(self.options)

#顯示文字類別
class Label:
    def __init__(self, color, x, y):
        self.color = color
        self.x = x
        self.y = y

    def draw(self, msg):
        lines = msg.split("\n")
        for i, line in enumerate(lines):
            txt = font.render(line, True, self.color)
            screen.blit(txt, (self.x, self.y + i * 30))

class titleLabel:
    def __init__(self, color, x, y):
        self.color = color
        self.x = x
        self.y = y

    def draw(self, msg):
        lines = msg.split("\n")
        for i, line in enumerate(lines):
            txt = m_menufont.render(line, True, self.color)
            screen.blit(txt, (self.x, self.y + i * 50))

discribe = Label(WHITE, 170, 370)
text = Label(WHITE, 10, 10)
p_block = 0
p_poison = [0, 0]
e_block = 0
e_poison = [0, 0]
enemy_list = [[1, "史萊姆", 40, 0], [1, "洞穴蝙蝠", 30, 3], [2, "哥布林", 80, 3], [2, "殭屍", 150, 0], 
[2, "骷髏士兵", 200, 3], [2, "骷髏騎士", 220, 5], [2, "獸人戰士", 300, 4], [3, "地下蠕蟲", 500, 0], 
[2, "妖魔", 300, 10], [3, "烈焰惡龍", 600, 4]]
enemy_data = [
    [["撞擊", "normal", 5], ["再生", "heal", 5]],
    [["咬", "normal", 15], ["超音波", "normal", 20]],
    [["襲擊", "normal", 20], ["突刺", "normal", 40], ["簡易藥水", "heal", 20]],
    [["咬", "normal", 30], ["毒素注入", "poison", 3, 10], ["再生", "heal", 50]],
    [["斬擊", "normal", 40], ["舉盾", "block", 30], ["全力斬", "normal", 60]],
    [["斬擊", "normal", 40], ["騎士衝鋒", "normal", 80], ["防禦姿態", "block", 40]],
    [["重擊", "normal", 60], ["狂襲", "normal", 100], ["吃果子", "heal", 200]],
    [["鑽地", "normal", 40], ["硬化防護", "block", 200], ["自我再生", "heal", 200], ["劇毒","poison",3,70]],
    [["魔力擾亂", "normal", 80], ["火焰彈", "normal", 160], ["恢復法術", "heal", 300]],
    [["吐息", "normal", 150], ["烈焰龍息", "normal", 300], ["鱗甲強化", "block", 250], ["巨龍不滅", "heal", 200]]
    ]
arr_spc = ["普通的", "輕盈的", "堅韌的", "尖刺的", "重裝的"]
wep_spc = ["普通的", "輕盈的", "沉重的", "鋒利的", "神聖的", "劇毒的", "烈焰的"]
arr_rarity = ["破舊", "簡易", "常見", "稀有", "史詩", "神話", "傳奇"]
wep_rarity = ["棍子", "木劍", "鐵劍",  "銀劍", "金劍", "黑金劍", "聖劍"]
class armor:
    def __init__(self, rarity, affixe):
        self.name = arr_spc[affixe] + arr_rarity[rarity]
        self.rarity = rarity
        self.affixe = affixe
    
    def renew(self, rarity, affixe):
        self.name = arr_spc[affixe] + arr_rarity[rarity]
        self.rarity = rarity
        self.affixe = affixe


class weapon:
    def __init__(self, rarity, affixe):
        self.name = wep_spc[affixe] + wep_rarity[rarity]
        self.rarity = rarity
        self.affixe = affixe
    
    def renew(self, rarity, affixe):
        self.name = wep_spc[affixe] + wep_rarity[rarity]
        self.rarity = rarity
        self.affixe = affixe


p_arr = [armor(0, 0), armor(0,0), armor(0,0)]
p_wep = weapon(0, 0)
p_skill = [["治癒", 1, 20], ["火焰球", 2, 30], ["毒箭", 3, 50], ["光明護盾", 4, 50]]
p_skillunlock = [1,0,0,0]
def drawline():
    py.draw.rect(screen, WHITE, (0, 350, 800, 10))
    py.draw.rect(screen, WHITE, (0, 140, 800, 10))
    py.draw.rect(screen, WHITE, (150, 350, 10, 400))
    py.draw.rect(screen, WHITE, (0, 0, 800, 10))

#玩家初始化
hp = [100, 100]
mp = [50, 50]
xp = [0, 0]
level, power, money, p_lvl = 0, 200, 200, 1
p_atk, p_shd, p_spd, p_basicatk = 0, 0, 0, 0
itemtype = ["生命藥水", "魔力藥水", "體力藥水", "逃脫繩", "退出"]
itemcnt = [2, 0, 0, 1, 3]
gameover = False
#戰鬥用，代表是否逃跑和是否返回上一步
getoff = False
back = False
def show_msg(txt):
    for i in range(len(txt)):
        index = 0
        while index < len(txt[i]) + 1:
            for event in py.event.get():
                if event.type == py.QUIT:
                    sys.exit()
            screen.fill(BLACK)
            screen.blit(bg, (0, 150))
            text.draw(txt[i][:index])
            drawline()
            py.display.flip()
            py.time.delay(50)  # 控制速度
            index += 1
        py.time.delay(400)
    
        

def y_or_n(msg2):
    menu = Menu(["是", "否"], 10, 370)
    show_msg([msg2])
    while True:
        if menu.options[menu.index] == "是":
            msg = "接受提議"
        if menu.options[menu.index] == "否":
            msg = "否定提議"
        screen.fill(BLACK)
        screen.blit(bg, (0, 150))
        menu.draw(screen)
        discribe.draw(msg)
        text.draw(msg2)
        drawline()
        py.display.flip()
        for event in py.event.get():
            if event.type == py.QUIT:
                sys.exit()
            elif event.type == py.KEYDOWN:
                if event.key == py.K_UP:
                    menu.move_selection("up")
                elif event.key == py.K_DOWN:
                    menu.move_selection("down")
                elif event.key == py.K_RETURN: 
                    if menu.options[menu.index] == "是":
                        return True
                    if menu.options[menu.index] == "否": 
                        return False

def p_check():
    global p_atk
    global p_shd
    global p_spd
    global xp
    xp[1] = 15 + (p_lvl * 4)
    if xp[0] >= xp[1]:
        levelup()
    spdcount = 0
    atkcount = 0
    defcount = 0
    for i in range(0, 3):
        p_arr[i].renew(p_arr[i].rarity, p_arr[i].affixe)
    p_wep.renew(p_wep.rarity, p_wep.affixe)
    for i in range(0, 3):
        if p_arr[i].affixe == 1:
            spdcount += 1
        if p_arr[i].affixe == 2:
            defcount += 1
        if p_arr[i].affixe == 3:
            atkcount += 1
        if p_arr[i].affixe == 1:
            defcount += 2
            spdcount -= 1
    if p_wep.affixe == 1:
        spdcount += 1
    if p_wep.affixe == 2:
        defcount += 1
    if p_wep.affixe == 3:
        atkcount += 1
    if p_wep.affixe == 4:
        defcount += 2
    if p_wep.affixe == 5:
        spdcount += 2
    if p_wep.affixe == 6:
        atkcount += 2
    p_atk = int(p_lvl/3) + int(p_wep.rarity*2) + p_basicatk + atkcount + 1
    p_shd = int(p_arr[0].rarity + p_arr[1].rarity) + int(p_lvl/3) + defcount + 1
    p_spd = p_arr[2].rarity + spdcount + 1

def main():
    global gameover
    msg, msg2 = "", ""
    main_menu = Menu(["繼續冒險", "使用物品", "檢視裝備", "存檔", "退出"], 10, 370)
    while not gameover:
        if level <= 20:
            bgset("image/bg1.jpg")
        elif level <= 40:
            bgset("image/bg2.jpg")
        elif level <= 60:
            bgset("image/bg3.jpeg")
        else:
            bgset("image/bg4.jpg")
        
        p_check()
        if main_menu.options[main_menu.index] == "繼續冒險":
            msg = "繼續往地下城的更深處冒險"
        elif main_menu.options[main_menu.index] == "使用物品":
            msg = "打開背包，使用道具"
        elif main_menu.options[main_menu.index] == "檢視裝備":
            msg = "檢視自己的裝備和數值"
        elif main_menu.options[main_menu.index] == "存檔":
            msg = "保存遊戲進度"
        elif main_menu.options[main_menu.index] == "退出":
            msg = "離開遊戲"


        msg2 = f"請選擇下一步動作 \n目前層數 : {level}  |   目前生命 : {hp[0]} / {hp[1]} \n目前魔力 : {mp[0]} / {mp[1]}    |    目前經驗 : {xp[0]} / {xp[1]} \n剩餘體力 : {power}   |   目前等級 : {p_lvl}   |   持有金錢 : {money}"
        screen.fill(BLACK)
        screen.blit(bg, (0, 150))
        main_menu.draw(screen)
        discribe.draw(msg)
        text.draw(msg2)
        drawline()
        py.display.flip()
        for event in py.event.get():
            if event.type == py.QUIT:
                sys.exit()
            elif event.type == py.KEYDOWN:
                if event.key == py.K_UP:
                    main_menu.move_selection("up")
                elif event.key == py.K_DOWN:
                    main_menu.move_selection("down")
                elif event.key == py.K_RETURN:
                    if main_menu.options[main_menu.index] == "繼續冒險":
                        adventure()
                    elif main_menu.options[main_menu.index] == "使用物品":
                        use()
                    elif main_menu.options[main_menu.index] == "檢視裝備":
                        show()
                    elif main_menu.options[main_menu.index] == "存檔":
                        save()
                        show_msg(["存檔成功"])
                    elif main_menu.options[main_menu.index] == "退出":
                        gameover = True
                        sys.exit()

def show():
    p_check()
    bgset("image/equipment.jpg")
    msg, msg2 = "", ""
    show_menu = Menu(["下一頁", "返回"], 10, 370)
    cnt = 1
    while not gameover:
        if cnt == 1:
            msg2 = f"頭部 : {p_arr[0].name}頭盔    |    身體 : {p_arr[1].name}護甲\n腳 : {p_arr[2].name}靴子   |   武器 : {p_wep.name}"
        elif cnt == 2:
            msg2 = f"護甲值 : {p_shd} \n攻擊力 : {p_atk}\n速度 : {p_spd}"
        elif cnt == 3:
            msg2 = f"生命藥水 : {itemcnt[0]}   |   魔力藥水 : {itemcnt[1]}\n體力藥水 : {itemcnt[2]}   |   逃脫繩 : {itemcnt[3]}"
        
        if show_menu.options[show_menu.index] == "下一頁":
            msg = "其他數據"
        elif show_menu.options[show_menu.index] == "返回":
            msg = "返回原本的選單"
        screen.fill(BLACK)
        screen.blit(bg, (0, 150))
        show_menu.draw(screen)
        discribe.draw(msg)
        text.draw(msg2)
        drawline()
        py.display.flip()
        for event in py.event.get():
            if event.type == py.QUIT:
                sys.exit()
            elif event.type == py.KEYDOWN:
                if event.key == py.K_UP:
                    show_menu.move_selection("up")
                elif event.key == py.K_DOWN:
                    show_menu.move_selection("down")
                elif event.key == py.K_RETURN:
                    if show_menu.options[show_menu.index] == "下一頁":
                        cnt += 1
                        if cnt > 3:
                            cnt = 1
                    elif show_menu.options[show_menu.index] == "返回":
                        return
    return
#戰鬥外使用道具
def use():
    global getoff, back
    global hp, mp, power
    global itemcnt
    bgset("image/backpack.jpg")
    show_msg(['請選擇你要使用的物品'])
    use_menu = Menu(itemtype, 10, 370)
    Type = -1
    success = True
    already_use = False
    msg, msg2 = "", "請選擇你要使用的物品"
    while True:
        msg2 = f"請選擇你要使用的物品\n背包容量 : {itemcnt[4]} / 25"
        
        if not success:
            show_msg(["用完了..."])
            success = True
            Type = -1
        elif already_use and Type == 0:
            show_msg([f"恢復了部分生命，現在生命 : {hp[0]} / {hp[1]}"])
            already_use = False
        elif already_use and Type == 1:
            show_msg([f"恢復了部分魔力，現在魔力 : {mp[0]} / {mp[1]}"]) 
            already_use = False
        elif already_use and Type == 2:
            show_msg([f"恢復了部分體力，現在體力 : {power}"])
            already_use = False
        elif already_use and Type == 3:
            show_msg(["沒有用...(一個逃脫繩已被丟棄)"])
            already_use = False

        
        if use_menu.options[use_menu.index] == "生命藥水":
            msg = f"恢復20%生命值 (持有 : {itemcnt[0]})"
        elif use_menu.options[use_menu.index] == "魔力藥水":
            msg = f"恢復40魔力 (持有 : {itemcnt[1]})"
        elif use_menu.options[use_menu.index] == "體力藥水":
            msg = f"恢復100體力 (持有 : {itemcnt[2]})"
        elif use_menu.options[use_menu.index] == "逃脫繩":
            msg = f"於戰鬥時使用可脫離戰鬥 (持有 : {itemcnt[3]})\n*目前非戰鬥狀態，使用將會丟棄該物品"
        elif use_menu.options[use_menu.index] == "退出":
            msg = f"退出使用清單，回到上一頁"
        screen.fill(BLACK)
        screen.blit(bg, (0, 150))
        use_menu.draw(screen)
        discribe.draw(msg)
        text.draw(msg2)
        drawline()
        py.display.flip()
        for event in py.event.get():
            if event.type == py.QUIT:
                sys.exit()
            elif event.type == py.KEYDOWN:
                if event.key == py.K_UP:
                    use_menu.move_selection("up")
                elif event.key == py.K_DOWN:
                    use_menu.move_selection("down")
                elif event.key == py.K_RETURN:
                    if use_menu.options[use_menu.index] == "生命藥水":
                        Type = 0
                        if itemcnt[0] > 0: 
                            itemcnt[0] -= 1
                            itemcnt[4] -= 1
                            hp[0] = min(hp[0] + int(hp[1] * 0.2), hp[1])
                            already_use = True
                        else:
                            success = False
                    elif use_menu.options[use_menu.index] == "魔力藥水":
                        Type = 1
                        if itemcnt[1] > 0:
                            itemcnt[1] -= 1
                            itemcnt[4] -= 1
                            mp[0] = min(mp[0] + 40, mp[1])
                            already_use = True
                        else:
                            success = False
                    elif use_menu.options[use_menu.index] == "體力藥水":
                        Type = 2
                        if itemcnt[2] > 0:
                            itemcnt[2] -= 1
                            itemcnt[4] -= 1
                            power += 100
                            already_use = True
                        else:
                            success = False    
                    elif use_menu.options[use_menu.index] == "逃脫繩":
                        Type = 3
                        if itemcnt[3] > 0:
                            itemcnt[3] -= 1
                            itemcnt[4] -= 1
                            already_use = True
                        else:
                            success = False   
                    elif use_menu.options[use_menu.index] == "退出":
                        return


#戰鬥中使用道具
def use_inbattle():
    show_msg(['請選擇你要使用的物品'])
    global getoff, back
    global hp, mp, power
    global itemcnt
    use_menu = Menu(itemtype, 10, 370)
    Type = -1
    getoff = False
    success = True
    already_use = False
    msg, msg2 = "", "請選擇你要使用的物品"
    while True:
        
        
        msg2 = f"請選擇你要使用的物品\n背包容量 : {itemcnt[4]} / 25"
        if not success:
            show_msg(["用完了..."])
            already_use = False
            success = True
            Type = -1
        elif already_use and Type == 0:
            show_msg([f"恢復了部分生命，現在生命 : {hp[0]} / {hp[1]}"])
        elif already_use and Type == 1:
            show_msg([f"恢復了部分魔力，現在魔力 : {mp[0]} / {mp[1]}"]) 
        elif already_use and Type == 2:
            show_msg([f"恢復了部分體力，現在體力 : {power}"])
        elif already_use and Type == 3:
            show_msg(["逃跑了 !"])
                
        if already_use:
            return
        if use_menu.options[use_menu.index] == "生命藥水":
            msg = f"恢復20%生命值 (持有 : {itemcnt[0]})"
        elif use_menu.options[use_menu.index] == "魔力藥水":
            msg = f"恢復40魔力 (持有 : {itemcnt[1]})"
        elif use_menu.options[use_menu.index] == "體力藥水":
            msg = f"恢復100體力 (持有 : {itemcnt[2]})"
        elif use_menu.options[use_menu.index] == "逃脫繩":
            msg = f"於戰鬥時使用可脫離戰鬥 (持有 : {itemcnt[3]})"
        elif use_menu.options[use_menu.index] == "退出":
            msg = f"退出使用清單，回到上一頁"
        screen.fill(BLACK)
        screen.blit(bg, (0, 150))
        use_menu.draw(screen)
        discribe.draw(msg)
        text.draw(msg2)
        drawline()
        py.display.flip()
        for event in py.event.get():
            if event.type == py.QUIT:
                sys.exit()
            elif event.type == py.KEYDOWN:
                if event.key == py.K_UP:
                    use_menu.move_selection("up")
                elif event.key == py.K_DOWN:
                    use_menu.move_selection("down")
                elif event.key == py.K_RETURN:
                    if use_menu.options[use_menu.index] == "生命藥水":
                        Type = 0
                        if itemcnt[0] > 0: 
                            itemcnt[0] -= 1
                            itemcnt[4] -= 1
                            hp[0] = min(hp[0] + int(hp[1] * 0.2), hp[1])
                            already_use = True
                        else:
                            success = False
                    elif use_menu.options[use_menu.index] == "魔力藥水":
                        Type = 1
                        if itemcnt[1] > 0:
                            itemcnt[1] -= 1
                            itemcnt[4] -= 1
                            mp[0] = min(mp[0] + 40, mp[1])
                            already_use = True
                        else:
                            success = False
                    elif use_menu.options[use_menu.index] == "體力藥水":
                        Type = 2
                        if itemcnt[2] > 0:
                            itemcnt[2] -= 1
                            itemcnt[4] -= 1
                            power += 100
                            already_use = True
                        else:
                            success = False    
                    elif use_menu.options[use_menu.index] == "逃脫繩":
                        Type = 3
                        if itemcnt[3] > 0:
                            itemcnt[3] -= 1
                            itemcnt[4] -= 1
                            getoff = True
                            already_use = True
                        else:
                            success = False   
                    elif use_menu.options[use_menu.index] == "退出":
                        back = True
                        return        
def save():
    p_check()
    save_data = {
        "hp": hp,
        "mp": mp,
        "level": level,
        "xp": xp,
        "money": money,
        "power": power,
        "p_lvl": p_lvl,
        "p_wep": {"rarity": p_wep.rarity, "affixe": p_wep.affixe},
        "p_arr": [{"rarity": a.rarity, "affixe": a.affixe} for a in p_arr],
        "p_basicatk": p_basicatk,
        "levelup_cnt": levelup_cnt,
        "p_skillunlock": p_skillunlock,
        "itemcnt": itemcnt
    }
    with open("save.json", "w") as f:
        json.dump(save_data, f)

def load():
    global hp, mp, xp, p_arr, p_wep, p_skillunlock, p_basicatk, level, levelup_cnt, power, money, p_lvl, itemcnt
    with open("save.json", "r") as f:
        save_data = json.load(f)
    
    hp = save_data["hp"]
    mp = save_data["mp"]
    level = save_data["level"]
    xp = save_data["xp"]
    money = save_data["money"]
    power = save_data["power"]
    p_lvl = save_data["p_lvl"]
    levelup_cnt = save_data["levelup_cnt"]
    p_basicatk = save_data["p_basicatk"]
    p_wep = weapon(save_data["p_wep"]["rarity"], save_data["p_wep"]["affixe"])
    p_arr = [armor(a["rarity"], a["affixe"]) for a in save_data["p_arr"]]
    itemcnt = save_data["itemcnt"]
    p_skillunlock = save_data["p_skillunlock"]
    p_check()

def adventure():
    global gameover, level, power
    show_msg(['請選擇你的決定'])
    isgameover = False
    eventlist = ["戰鬥"]
    dice = rd.randint(1, 100)
    if dice >= 30:
        eventlist.append("休息")
    if dice >= 50:
        eventlist.append("事件")
    if dice >= 70:
        eventlist.append("偶遇")
    if dice >= 80:
        eventlist.append("商人")
    menu = Menu(eventlist, 10, 370)
    msg, msg2 = "", "請選擇你的決定"
    while not isgameover:
        if menu.options[menu.index] == "戰鬥":
            msg = "遭遇未知的敵人並發生戰鬥(10體力)"
        if menu.options[menu.index] == "休息":
            msg = "休息一下，恢復生命和體力(不增加層數)"
        if menu.options[menu.index] == "事件":
            msg = "未知事件...不知道是好是壞(30體力)"
        if menu.options[menu.index] == "偶遇":
            msg = "前方似乎有個人影...搭話看看嗎?(50體力)"
        if menu.options[menu.index] == "商人":
            msg = f"是商人，可以用金幣和他交易(目前金幣 : {money})\n*不增加層數"
        
        screen.fill(BLACK)
        screen.blit(bg, (0, 150))
        menu.draw(screen)
        discribe.draw(msg)
        text.draw(msg2)
        drawline()
        py.display.flip()
        for event in py.event.get():
            if event.type == py.QUIT:
                sys.exit()
            elif event.type == py.KEYDOWN:
                if event.key == py.K_UP:
                    menu.move_selection("up")
                elif event.key == py.K_DOWN:
                    menu.move_selection("down")
                elif event.key == py.K_RETURN:
                    if menu.options[menu.index] == "戰鬥":
                        level += 1
                        if power >= 10:
                            power = power - 10
                            show_msg(["發生戰鬥 ! 失去 10 體力"])
                        else:
                            show_msg(["體力不足...失去部分生命"])
                            hp[0] = int(hp[0] * 0.8)
                            if hp[0] <= 0:
                                hp[0] += 1
                        battle()
                        return
                    if menu.options[menu.index] == "休息":
                        takebreak()
                        return
                    if menu.options[menu.index] == "事件":
                        if power >= 30:
                            power = power - 30
                            show_msg(["遭遇事件 ! 失去 30 體力"])
                        else:
                            show_msg(["體力不足...失去部分生命"])
                            hp[0] = int(hp[0] * 0.8)
                            if hp[0] <= 0:
                                hp[0] += 1
                        level += 1
                        Event()
                        return
                    if menu.options[menu.index] == "偶遇":
                        if power >= 50:
                            power = power - 50
                            show_msg(["向人搭話 ! 失去 50 體力"])
                        else:
                            show_msg(["體力不足...失去部分生命"])
                            hp[0] = int(hp[0] * 0.8)
                            if hp[0] <= 0:
                                hp[0] += 1
                        level += 1
                        meet()
                        return 
                    if menu.options[menu.index] == "商人":
                        shop()
                        return
    
def shop():
    global itemcnt, itemtype, money
    bgset("image/shop.jpg")
    menu = Menu(itemtype, 10, 370)
    isoff = False
    show_msg([f"想買些什麼? 剩餘金幣 : {money}   |   背包空間 : {itemcnt[4]} / 25"])
    msg, msg2 = "", f"想買些什麼? 剩餘金幣 : {money}   |   背包空間 : {itemcnt[4]} / 25"
    while not isoff:
        msg2 = f"想買些什麼? 剩餘金幣 : {money}   |   背包空間 : {itemcnt[4]} / 25"
        if menu.options[menu.index] == "生命藥水":
            msg = f"80金幣，恢復20%生命值 (持有 : {itemcnt[0]})"
        elif menu.options[menu.index] == "魔力藥水":
            msg = f"120金幣，恢復40魔力 (持有 : {itemcnt[1]})"
        elif menu.options[menu.index] == "體力藥水":
            msg = f"120金幣，恢復100體力 (持有 : {itemcnt[2]})"
        elif menu.options[menu.index] == "逃脫繩":
            msg = f"200金幣，於戰鬥時使用可脫離戰鬥 (持有 : {itemcnt[3]})"
        elif menu.options[menu.index] == "退出":
            msg = f"退出商店"
        screen.fill(BLACK)
        screen.blit(bg, (0, 150))
        menu.draw(screen)
        discribe.draw(msg)
        text.draw(msg2)
        drawline()
        py.display.flip()
        for event in py.event.get():
            if event.type == py.QUIT:
                sys.exit()
            elif event.type == py.KEYDOWN:
                if event.key == py.K_UP:
                    menu.move_selection("up")
                elif event.key == py.K_DOWN:
                    menu.move_selection("down")
                elif event.key == py.K_RETURN:
                    if menu.options[menu.index] == "生命藥水":
                        if money >= 60 and itemcnt[4] < 25:
                            itemcnt[0] += 1
                            itemcnt[4] += 1
                            money -= 80
                            show_msg([f"購買成功 ! ，剩餘金錢 : {money}"])
                        else:
                            if money < 80:
                                show_msg(["購買失敗...錢不夠"])
                            else:
                                show_msg(["購買失敗...背包太滿了"])
                    if menu.options[menu.index] == "魔力藥水":
                        if money >= 120 and itemcnt[4] < 25:
                            itemcnt[1] += 1
                            itemcnt[4] += 1
                            money -= 120
                            show_msg([f"購買成功 ! ，剩餘金錢 : {money}"])
                        else:
                            if money < 120:
                                show_msg(["購買失敗...錢不夠"])
                            else:
                                show_msg(["購買失敗...背包太滿了"])
                    if menu.options[menu.index] == "體力藥水":
                        if money >= 120 and itemcnt[4] < 25:
                            itemcnt[2] += 1
                            itemcnt[4] += 1
                            money -= 120
                            show_msg([f"購買成功 ! ，剩餘金錢 : {money}"])
                        else:
                            if money < 120:
                                show_msg(["購買失敗...錢不夠"])
                            else:
                                show_msg(["購買失敗...背包太滿了"])
                    if menu.options[menu.index] == "逃脫繩":
                        if money >= 200 and itemcnt[4] < 25:
                            itemcnt[3] += 1
                            itemcnt[4] += 1
                            money -= 200
                            show_msg([f"購買成功 ! ，剩餘金錢 : {money}"])
                        else:
                            if money < 200:
                                show_msg(["購買失敗...錢不夠"])
                            else:
                                show_msg(["購買失敗...背包太滿了"])
                    if menu.options[menu.index] == "退出":
                        return

def drop():
    global p_arr, p_wep, itemcnt, money, xp
    off = False
    show_msg(["敵人掉落了一些東西"])
    rarity = e_lvl + enemy
    if off:
        return 
    else:
        cnt = [0,0,0,0]
        dice = rd.randint(1, 40)
        money = money + dice
        dice2 = 5
        dice2 += rd.randint((enemy*10), (enemy*20))
        xp[0] = xp[0] + dice2 + int(rarity/5)
        show_msg([f"得到 {dice} 金幣\n得到 {dice2 + int(rarity/5)} 經驗"])
        if itemcnt[4] < 25:
            for i in range(3):
                dice = rd.randint(0, 2)
                if dice == 1:
                    cnt[0] += 1
                    itemcnt[0] += 1 
                    itemcnt[4] += 1
        if itemcnt[4] < 25:
            for i in range(2):
                dice = rd.randint(0, 2)
                if dice == 1:
                    cnt[1] += 1 
                    itemcnt[1] += 1 
                    itemcnt[4] += 1
        if itemcnt[4] < 25:
            for i in range(2):
                dice = rd.randint(0, 2)
                if dice == 1:
                    cnt[2] += 1 
                    itemcnt[2] += 1 
                    itemcnt[4] += 1
        if itemcnt[4] < 25:
            for i in range(2):
                dice = rd.randint(0, 2)
                if dice == 1:
                    cnt[3] += 1
                    itemcnt[3] += 1 
                    itemcnt[4] += 1
        msg = []
        for i in range(4):
            if cnt[i] != 0:
                msg.append(f"得到 {itemtype[i]} {cnt[i]} 個")
        show_msg(msg)
        t_arr = [armor(0, 0), armor(0, 0), armor(0, 0)]
        t_wep = weapon(0, 0)
        for i in range(0, 3):
            if rarity >= (40 + level*3):
                dice = rarity
            else:
                dice = rd.randint(rarity, 40 + level*3)
            dice2 = rd.randint(0, 1)
            randomspc = True
            if dice2 == 1:
                raritytmp, affixetmp = 0, 0
                if dice <= 30:
                    raritytmp = 1
                elif dice <= 50:
                    raritytmp = 2
                elif dice <= 70:
                    raritytmp = 3
                elif dice <= 90:
                    raritytmp = 4
                elif dice <= 110:
                    raritytmp = 5
                elif dice <= 170:
                    raritytmp = 6
                else:
                    raritytmp = 6
                    affixetmp = rd.randint(1, 4)
                    randomspc = False
                if randomspc:
                    dice3 = rd.randint(0, 2)
                    if dice3 == 1:
                        affixetmp = rd.randint(1, 4)
                    else: affixetmp = 0
                t_arr[i].renew(raritytmp, affixetmp)
        if rarity >= (40 + level*3):
            dice = rarity
        else:
            dice = rd.randint(rarity, 40 + level*3)
            dice2 = rd.randint(0, 1)
        raritytmp, affixetmp = 0, 0
        randomspc = True
        if dice2 == 1:
            if dice <= 30:
                raritytmp = 1
            elif dice <= 50:
                raritytmp = 2
            elif dice <= 70:
                raritytmp = 3
            elif dice <= 90:
                raritytmp = 4
            elif dice <= 110:
                raritytmp = 5
            elif dice <= 170:
                raritytmp = 6
            else:
                raritytmp = 6
                affixetmp = rd.randint(1, 6)
                randomspc = False
            if randomspc:
                dice3 = rd.randint(0, 2)
                if dice3 == 1:
                    if raritytmp >= 4:
                        affixetmp = rd.randint(1, 6)
                    else:
                        affixetmp = rd.randint(1, 3)
                else: affixetmp = 0
            t_wep.renew(raritytmp, affixetmp)
            if t_arr[0].rarity != 0:        
                ask = y_or_n(f"得到 {t_arr[0].name}頭盔\n是否取代目前的 {p_arr[0].name}頭盔?")
                if ask:
                    p_arr[0].renew(t_arr[0].rarity, t_arr[0].affixe)
                else:
                    money += (t_arr[0].rarity * 30)
                    show_msg([f"把不要的裝備轉換成金錢，得掉金錢 {t_arr[0].rarity * 30}"])
            if t_arr[1].rarity != 0:
                ask = y_or_n(f"得到 {t_arr[1].name}護甲\n是否取代目前的 {p_arr[1].name}護甲?")
                if ask:
                    p_arr[1].renew(t_arr[1].rarity, t_arr[1].affixe)
                else:
                    money += (t_arr[1].rarity * 50)
                    show_msg([f"把不要的裝備轉換成金錢，得掉金錢 {t_arr[1].rarity * 30}"])
            if t_arr[2].rarity != 0:
                ask = y_or_n(f"得到 {t_arr[2].name}靴子\n是否取代目前的 {p_arr[2].name}靴子?")
                if ask:
                    p_arr[2].renew(t_arr[2].rarity, t_arr[2].affixe)
                else:
                    money += (t_arr[2].rarity * 50)
                    show_msg([f"把不要的裝備轉換成金錢，得掉金錢 {t_arr[2].rarity * 30}"])
            if t_wep.rarity != 0:
                ask = y_or_n(f"得到 {t_wep.name}\n是否取代目前的 {p_wep.name}?")
                if ask:
                    p_wep.renew(t_wep.rarity, t_wep.affixe)
                else:
                    money += (t_wep.rarity * 50)
                    show_msg([f"把不要的裝備轉換成金錢，得掉金錢 {t_wep.rarity * 30}"])
    return 
enemy = 0
e_lvl = 0
e_hp = [0, 0]
move = 0
def battle():
    global level, e_hp, getoff, back, move, hp, mp
    off = False
    choose_enemy()
    show_msg([f"等級 {e_lvl} 出現了的 {enemy_list[enemy][1]} 出現了 !"])
    if off:
        return
    else:
        menu = Menu(["普通攻擊", "使用道具", "使用技能"], 10, 370)
        while True:
            back = True
            move = 0
            while back:
                
                msg2 = f"請選擇你的行動\n敵人血量 : {e_hp[0]} / {e_hp[1]}\n你的血量 : {hp[0]} / {hp[1]}   |   你的魔力 : {mp[0]} / {mp[1]}"
                if menu.options[menu.index] == "普通攻擊":
                    msg = "發起攻擊，造成傷害"
                if menu.options[menu.index] == "使用道具":
                    msg = "打開物品選單"
                if menu.options[menu.index] == "使用技能":
                    msg = "打開技能選單"
                screen.fill(BLACK)
                screen.blit(bg, (0, 150))
                menu.draw(screen)
                discribe.draw(msg)
                text.draw(msg2)
                drawline()
                py.display.flip()
                for event in py.event.get():
                    if event.type == py.QUIT:
                        sys.exit()
                    elif event.type == py.KEYDOWN:
                        if event.key == py.K_UP:
                            menu.move_selection("up")
                        elif event.key == py.K_DOWN:
                            menu.move_selection("down")
                        elif event.key == py.K_RETURN:
                            if menu.options[menu.index] == "普通攻擊":
                                move = 0
                                back = False
                            if menu.options[menu.index] == "使用道具":
                                back = False
                                use_inbattle()
                                move = -1
                                if getoff:
                                    back = False
                                    getoff = False
                                    return
                            if menu.options[menu.index] == "使用技能":
                                back = False
                                skill()
                            
            if p_spd >= enemy_list[enemy][3]:
                p_turn()
                if hp[0] <= 0:
                    gameend()
                    return
                elif e_hp[0] <= 0:
                    drop()
                    return
                e_turn()
                if hp[0] <= 0:
                    gameend()
                    return
                elif e_hp[0] <= 0:
                    drop()
                    return
            else:
                e_turn()
                if hp[0] <= 0:
                    gameend()
                    return
                elif e_hp[0] <= 0:
                    drop()
                    return
                p_turn()
                if hp[0] <= 0:
                    gameend()
                    return
                elif e_hp[0] <= 0:
                    drop()
                    return
def skill():
    global move, mp, back
    list_ = []
    for i in range(4):
        if p_skillunlock[i] == 1:
            list_.append(p_skill[i][0])
    list_.append("退出")
    show_msg([f'選擇要使用的技能，剩餘魔力 : {mp[0]} / {mp[1]}'])
    msg = ""
    menu = Menu(list_, 10, 370)
    while True:
        # p_skill = [["治癒", 1, 20], ["火焰球", 2, 30], ["毒箭", 3, 50], ["光明護盾", 4, 50]]
        msg2 = f"選擇要使用的技能，剩餘魔力 : {mp[0]} / {mp[1]}"

        if menu.options[menu.index] == p_skill[0][0]:
            msg = "消耗魔力，治療傷口 (消耗 : 20)"
        if menu.options[menu.index] == p_skill[1][0]:
            msg = "聚集魔力，造成大量傷害 (消耗 : 30)"
        if menu.options[menu.index] == p_skill[2][0]:
            msg = "消耗魔力，給敵人下毒\n毒傷害將持續一段時間，並無視防禦 (消耗 : 50)"
        if menu.options[menu.index] == p_skill[3][0]:
            msg = "消耗魔力，為自己製造一個護盾 (消耗 : 50)"
        if  menu.options[menu.index] == "退出":
            msg = "退出選單"
        screen.fill(BLACK)
        screen.blit(bg, (0, 150))
        menu.draw(screen)
        discribe.draw(msg)
        text.draw(msg2)
        drawline()
        py.display.flip()
        for event in py.event.get():
            if event.type == py.QUIT:
                sys.exit()
            elif event.type == py.KEYDOWN:
                if event.key == py.K_UP:
                    menu.move_selection("up")
                elif event.key == py.K_DOWN:
                    menu.move_selection("down")
                elif event.key == py.K_RETURN:
                    if menu.options[menu.index] == p_skill[0][0]:
                        if mp[0] >= 20:
                            mp[0] -= 20
                            move = 1
                            back = False
                            return
                        else:
                            show_msg(["魔力不夠了..."])
                    if menu.options[menu.index] == p_skill[1][0]:
                        if mp[0] >= 30:
                            mp[0] -= 30
                            move = 2
                            back = False
                            return
                        else:
                            show_msg(["魔力不夠了..."])
                    if menu.options[menu.index] == p_skill[2][0]:
                        if mp[0] >= 50:
                            mp[0] -= 50
                            move = 3
                            back = False
                            return
                        else:
                            show_msg(["魔力不夠了..."])
                    if menu.options[menu.index] == p_skill[3][0]:
                        if mp[0] >= 50:
                            mp[0] -= 50
                            move = 4
                            back = False
                            return
                        else:
                            show_msg(["魔力不夠了..."])
                    if menu.options[menu.index] == "退出":
                        back = True
                        return

def p_turn():
    global move, p_block, hp, p_poison, e_block, e_poison, back
    atk = p_atk * 3
    r_atk = atk - (e_lvl)
    if r_atk <= 5:
        r_atk = 5
    if p_poison[0] > 0:
        p_poison[0] = p_poison[0] - 1
        show_msg(["受到了毒的傷害 ! ", f"生命 - {p_poison[1]}，毒剩餘 {p_poison[0]} 回合"])
        hp[0] = hp[0] - p_poison[1]
        if hp[0] <= 0:
            return
    
    if move == 0:
        if e_block <= 0:
            e_hp[0] = e_hp[0] - r_atk
            if e_hp[0] < 0:
                e_hp[0] = 0
            show_msg([f"普通攻擊 ! 造成了 {r_atk} 點傷害\n敵人生命剩餘 : {e_hp[0]}"])
        else:
            e_block -= atk
            if e_block <= 0:
                e_block = 0
            show_msg([f"普通攻擊 ! 對敵人護盾造成了 {atk} 點傷害\n敵人護盾剩餘 : {e_block}"])
    elif move == 1:
        hp[0] = min(hp[0] + int(hp[1] * 0.3), hp[1])
        show_msg([f"恢復了生命 ! \n現在生命 : {hp[0]} / {hp[1]}"])
    elif move == 2:
        if p_wep.affixe == 6:
            show_msg(["在烈焰武器的加持下，傷害加倍"])
            atk += atk
            r_atk += r_atk
        if e_block <= 0:
            e_hp[0] = e_hp[0] - (r_atk * 3)
            if e_hp[0] < 0:
                e_hp[0] = 0
            show_msg([f"火焰球 ! 造成了 {r_atk * 3} 點傷害\n敵人生命剩餘 : {e_hp[0]}"])
        else:
            e_block -= (atk * 2)
            if e_block <= 0:
                e_block = 0
            show_msg([f"火焰球 ! 對敵人護盾造成了 {atk * 2} 點傷害\n敵人護盾剩餘 : {e_block}"])
    elif move == 3:
        e_poison[0] = 3
        e_poison[1] = int(atk * 0.5)
        if p_wep.affixe == 5:
            e_poison[0] += 3
            e_poison[1] += int(atk * 0.5)
            show_msg(["在劇毒武器的加持下，持續時間、傷害加倍"])
        show_msg([f"下毒成功 ! 毒將持續 {e_poison[0]} 回合，每回合造成 {e_poison[1]} 傷害"])
    elif move == 4:
        p_block = p_block + (p_shd * 3) + 10
        if p_wep.affixe == 4:
            p_block += p_block
            show_msg(["在神聖武器的加持下，護盾值加倍"])
        show_msg([f"施法成功 ! 目前護盾值 : {p_block}"])      
    return

def e_turn():
    global hp, e_hp, e_poison, e_block, p_poison, p_block
    def_ = int(p_shd * 2.5)
    def_ = def_ - int(e_lvl - enemy*2)
    if def_ <= 0:
        def_ = 0
    bck = 0.1 * int(def_ / 3)
    if bck >= 0.5:
        bck = 0.5
    if e_poison[0] > 0:
        e_poison[0] = e_poison[0] - 1
        e_hp[0] -= e_poison[1]
        show_msg([f"下毒奏效了 !\n{enemy_list[enemy][1]} 受到了毒傷害 !\n失去 {e_poison[1]} 生命"])
        if e_hp[0] <= 0:
            return
    dice = rd.randint(1, 3)
    if dice == 3:
        show_msg([f"小心 ! {enemy_list[enemy][1]} 使用技能了"])
        dice2 = rd.randint(1, enemy_list[enemy][0])
        show_msg([f"{enemy_list[enemy][1]} 使出了 {enemy_data[enemy][dice2][0]}"])
        if enemy_data[enemy][dice2][1] ==  "normal":
            if p_block > 0:
                p_block = p_block - enemy_data[enemy][dice2][2]
                show_msg([f"對我方護盾造成了 {enemy_data[enemy][dice2][2]} 點傷害\n護盾剩餘 : {p_block}"])
                if p_block <= 0:
                    p_block = 0
            else:
                dmg = int(enemy_data[enemy][dice2][2] * (1 - bck))
                if dmg <= 0:
                    dmg = 1
                hp[0] = hp[0] - dmg
                show_msg([f"對我方造成了 {enemy_data[enemy][dice2][2]} 點傷害"])
        elif enemy_data[enemy][dice2][1] == "poison":
            show_msg(["被下毒了 ! "])
            p_poison[0] = enemy_data[enemy][dice2][2]
            p_poison[1] = enemy_data[enemy][dice2][3]
        elif enemy_data[enemy][dice2][1] == "block":
            e_block = e_block + enemy_data[enemy][dice2][2]
            show_msg([f"{enemy_list[enemy][1]} 展開了護盾\n當前護盾值 : {e_block}"] )
        elif enemy_data[enemy][dice2][1] == "heal":
            show_msg([f"{enemy_list[enemy][1]} 嘗試恢復生命"])
            e_hp[0] = min(e_hp[0] + enemy_data[enemy][dice2][2], e_hp[1])
            show_msg([f"{enemy_list[enemy][1]} 現在生命 : {e_hp[0]}"])
    else:
        show_msg([f"{enemy_list[enemy][1]} 使出了 {enemy_data[enemy][0][0]}"])
        if p_block > 0:
            p_block = p_block - enemy_data[enemy][0][2]
            show_msg([f"對我方護盾造成了 {enemy_data[enemy][0][2]} 點傷害\n護盾剩餘 {p_block} 點血量"])
            if p_block <= 0:
                p_block = 0
        else:
            dmg = int(enemy_data[enemy][0][2] * (1 - bck))
            if dmg <= 0:
                dmg = 1
            hp[0] = hp[0] - dmg
            show_msg([f"受到了 {dmg} 點傷害"])

dragon_down = False
def choose_enemy():
    global dragon_down, e_block, e_poison
    global enemy, e_lvl
    e_block = 0
    e_poison = [0,0]
    if level <= 15:
        enemy_ = rd.randint(0, 1)
    elif level <= 25:
        enemy_ = rd.randint(0, 2)
    elif level <= 40:
        enemy_ = rd.randint(2, 3)
    elif level <= 60:
        enemy_ = rd.randint(3, 5)
    elif level <= 80:
        enemy_ = rd.randint(5, 7)
    elif level < 100:
        enemy_ = rd.randint(6, 8)
    elif level >= 100 and not dragon_down:
        enemy_ = 9
        dragon_down = True
    else:
        enemy_ = rd.randint(7, 9)

    if enemy_ == 0:
        bgset("image/slime.jpg")
    elif enemy_ == 1:
        bgset("image/bat.jpg")
    elif enemy_ == 2:
        bgset("image/goblin.jpg")
    elif enemy_ == 3:
        bgset("image/zombie.jpg")
    elif enemy_ == 4:
        bgset("image/skeleton_warrior.jpg")
    elif enemy_ == 5:
        bgset("image/skeleton_knight.jpg")
    elif enemy_ == 6:
        bgset("image/orc.jpg")
    elif enemy_ == 7:
        bgset("image/worm.jpg")
    elif enemy_ == 8:
        bgset("image/witch.png")
    elif enemy_ == 9:
        bgset("image/dragon.jpg")



    
    e_lvl = rd.randint(level , level * 3)
    if e_lvl >= enemy_*7:
        e_lvl = enemy_*7 + rd.randint(1, 5)
    enemy = enemy_
    e_hp[1] = enemy_list[enemy][2]
    for i in range(e_lvl):
        e_hp[1] = int(e_hp[1] * 1.01)
    e_hp[0] = e_hp[1]
    
def meet():
    global hp, mp, xp, power, money, p_arr, p_wep
    dice = rd.randint(1, 6)
    if dice == 1:
        bgset("image/thief.jpg")
        show_msg(["該死的...是個小偷", "失去一半的金錢"])
        money = int(money * 0.5)
    elif dice == 2:
        bgset("image/wizard.jpg")
        hp[0] = min(hp[0] + int(hp[1] * 0.5), hp[1])
        mp[0] = min(mp[0] + 100, mp[1])
        show_msg(["是個法師...太好了，他願意無償提供我們幫助", "在他的幫助下，魔力、生命回復"])
    elif dice == 3:
        bgset("image/doctor.jpg")
        show_msg(["是個...醫生?", "他要求我們支付200金幣，以換取他的幫助"])
        ask = y_or_n(f"要付錢嗎?\n(持有金幣 : {money})")
        if ask:
            if money >= 200:
                money -= 200
                show_msg(["醫生感謝你的合作，隨後，提供了醫療援助", "生命值完全恢復 ! "])
                hp[0] = hp[1]
            else:
                show_msg(["錢不夠啊..."])
        else:
            show_msg(["遭到拒絕的醫生默默離開了..."])
    elif dice == 4:
        bgset("image/blacksmith.jpg")
        ask = y_or_n(f"是個鍛造師，要用200金幣請他升級武器嗎?\n(持有金幣 : {money})\n*若武器已經是最高等級，則無法升級")
        if ask:
            if money >= 200:
                if p_wep.rarity < 6:
                    money -= 200
                    show_msg(["武器被升級了 ! "])
                    p_wep.renew(p_wep.rarity + 1, p_wep.affixe)
                else:
                    show_msg(["武器已經無法再升級了 ! "])
            else:
                show_msg(["錢不夠啊..."])
        else:
            show_msg(["遭到拒絕的鍛造師默默離開了..."])
    elif dice == 5:
        bgset("image/blacksmith.jpg")
        ask = y_or_n(f"是個鐵匠，要用400金幣請他升級裝備嗎?\n(持有金幣 : {money})\n*若裝備已經是最高等級，則無法升級")
        if ask:
            if money >= 400:
                if p_arr[0].rarity >= 6 and p_arr[1].rarity >= 6 and p_arr[2].rarity >= 6:
                    show_msg(["裝備已經無法再升級了 ! "])
                else:
                    money -= 400
                    show_msg(["裝備被升級了 ! "])
                    for i in range(3):
                        if p_arr[i].rarity < 6:
                            p_arr[i].renew(p_arr[i].rarity + 1, p_arr[i].affixe)
            else:
                show_msg(["錢不夠啊..."])
        else:
            show_msg(["遭到拒絕的鐵匠默默離開了..."])
    elif dice == 6:
        bgset("image/adventurer.jpg")
        ask = y_or_n(f"是個經驗老道的冒險家，要用200金幣請他指導我們嗎?\n(持有金幣 : {money})")
        if ask:
            if money >= 200:
                money -= 200
                if p_lvl <= 20:
                    xp[0] += 150
                else:
                    xp[0] += 250
                show_msg(["在他的指導下，得到大量經驗 !"])
            else:
                show_msg(["錢不夠啊..."])
        else:
            show_msg(["那位冒險家默默離開了..."])
    p_check()
    return
def takebreak():
    global power, hp, mp
    dice = rd.randint(1, 3)
    hp[0] = min(hp[0] + int(hp[1] * 0.3), hp[1])
    power += 100
    if dice == 2:
        mp[0] = min(mp[0] + int(mp[1] * 0.5), mp[1])
        show_msg(["休息了一下", "感覺到魔力湧動 !", "生命、體力恢復，還恢復了大量魔力 !"])
    else:
        show_msg(["休息了一下","生命、體力恢復 ! "])
    return
def Event():
    global hp, mp, power
    dice = rd.randint(1, 11)
    if dice <= 4:
        bgset("image/trap.jpeg")
        hp[0] -= int(hp[0] * 0.3)
        show_msg(["運氣真差...是個陷阱", f"失去 {int(hp[0] * 0.3)} 點生命"])
    elif dice <= 7:
        bgset("image/hot_spring.jpg")
        hp[0] = min(hp[0] + int(hp[1] * 0.4), hp[1])
        power += 100
        show_msg(["太好了，是個溫泉 !", "休息了一下，恢復生命值和體力"])
    elif dice <= 9:
        bgset("image/hot_spring.jpg")
        hp[0] = min(hp[0] + int(hp[1] * 0.4), hp[1])
        mp[0] = min(mp[0] + 40, mp[1])
        power += 100
        show_msg(["太好了，是個蘊含大量魔力的溫泉 !", "休息了一下，恢復生命值、體力和魔力"])
    elif dice == 10:
        bgset("image/statue.jpg")
        hp[1] = int(hp[1] * 1.05) + 20
        hp[0] = hp[1]
        mp[1] += 50
        mp[0] = mp[1]
        show_msg(["是個散發著莊嚴氣息的女神像...", "觸摸了神像，感受到神像的賜福", "生命、魔力最大值成長並完全恢復 !"])
    else:
        show_msg(["無事發生...算件好事嗎?"])
    return
levelup_cnt = 0
def levelup():
    global gameover
    global xp, p_lvl, levelup_cnt, p_skillunlock
    tmp_hp, tmp_mp = hp[1], mp[1]
    while xp[0] >= xp[1]:
        xp[0] -= xp[1]
        xp[1] = 15 + (p_lvl * 4)
        hp[1] = int(hp[1] * 1.03) + 10
        mp[1] = int(mp[1] * 1.03) + 3
        hp[0] = min(hp[0] + int(hp[1] * 0.03) + 10, hp[1])
        mp[0] = min(mp[0] + int(mp[1] * 0.03 + 3), mp[1])
        p_lvl += 1

        levelup_cnt += 1
    if p_lvl >= 5 and p_skillunlock[1] == 0:
        p_skillunlock[1] = 1
        show_msg(["習得技能 火焰球\n聚集魔力，造成大量傷害"])
    if p_lvl >= 13 and p_skillunlock[2] == 0:
        p_skillunlock[2] = 1
        show_msg(["習得技能 毒箭\n消耗魔力，給敵人下毒\n毒傷害將持續一段時間，並無視防禦"])
    if p_lvl >= 21 and p_skillunlock[3] == 0:
        p_skillunlock[3] = 1
        show_msg(["習得技能 光明護盾\n消耗魔力，為自己製造一個護盾"])

    show_msg([f"你升級了，現在等級 {p_lvl}\n生命最大值 : {tmp_hp} --> {hp[1]}\n魔力最大值 : {tmp_mp} --> {mp[1]}"])
    run, off = True, False
    t = py.time.get_ticks()

    while levelup_cnt >= 3 and not off:
        levelup_cnt -= 3
        upgrade()
        
    return

def upgrade():
    global hp, mp, p_basicatk
    t = 0
    freeze = False
    choice = Menu(["最大生命", "最大魔力", "攻擊力"], 10, 370)
    show_msg(["額外加點 ! 請選擇想要加點的項目"])
    while True:
        if freeze and py.time.get_ticks() - t >= 1000:
            return
        
        if not freeze:
            msg2 = "額外加點 ! 請選擇想要加點的項目"
        else:
            show_msg(["加點成功 !"])

        if choice.options[choice.index] == "最大生命":
            msg = "得到額外的生命最大值"
        if choice.options[choice.index] == "最大魔力":
            msg = "得到額外的魔力最大值"
        if choice.options[choice.index] == "攻擊力":
            msg = "得到額外的攻擊力"    
        screen.fill(BLACK)
        screen.blit(bg, (0, 150))
        choice.draw(screen)
        text.draw(msg2)
        discribe.draw(msg)
        drawline()
        py.display.flip()
        for event in py.event.get():
            if event.type == py.QUIT:
                sys.exit()
            elif event.type == py.KEYDOWN and not freeze:
                if event.key == py.K_UP:
                    choice.move_selection("up")
                elif event.key == py.K_DOWN:
                    choice.move_selection("down")
                elif event.key == py.K_RETURN:
                    if choice.options[choice.index] == "最大生命":
                        hp[1] = int(hp[1] * 1.03) + 10
                        hp[0] = min(hp[0] + int(hp[1] * 1.03) + 10, hp[1])
                        t = py.time.get_ticks()
                        freeze = True
                    if choice.options[choice.index] == "最大魔力":
                        mp[1] = int(mp[1] * 1.03) + 3
                        mp[0] = min(mp[0] + int(mp[1] * 1.03) + 3, mp[1])
                        t = py.time.get_ticks()
                        freeze = True
                    if choice.options[choice.index] == "攻擊力":
                        p_basicatk += 1
                        t = py.time.get_ticks()
                        freeze = True

def gameend():
    global select, level
    ask = y_or_n("你倒下了，是否返回上一層重來?\n選否將直接結束遊戲 !")
    if not ask:
        ask = show_msg(["遊戲結束 ! 下次好運 !"])
        sys.exit()
    else:
        level -= 1
        hp[0] = 1
        return
def titlescreen():
    menu = titleMenu(["開始遊戲","讀取存檔", "退出遊戲"], 10, 300)
    menu_label = titleLabel(WHITE, 330, 300)
    msg = "test"
    while True:
        if menu.options[menu.index] == "開始遊戲":
            msg = "那就開始吧 > <"
        if menu.options[menu.index] == "讀取存檔":
            msg = "原來之前玩過啊? 那太好了\n讀取記錄吧 !\n*若無存檔，可能導致遊戲\n崩潰"
        if menu.options[menu.index] == "退出遊戲":
            msg = "剛開起來就要走掉喔...\n好吧..."
        screen.fill(BLACK)     
        title_text = titlefont.render("某冒險 RPG", True, WHITE)
        py.draw.rect(screen, WHITE, (0, 225, 800, 10))
        py.draw.rect(screen, WHITE, (300, 225, 10, 800))
        screen.blit(title_text, (10, 70))
        menu_label.draw(msg)
        menu.draw(screen)
        py.display.flip()

        for event in py.event.get():
            if event.type == py.QUIT:
                sys.exit()
            elif event.type == py.KEYDOWN:
                if event.key == py.K_UP:
                    menu.move_selection("up")
                elif event.key == py.K_DOWN:
                    menu.move_selection("down")
                elif event.key == py.K_RETURN:
                    if menu.options[menu.index] == "開始遊戲":
                        main()
                        sys.exit()
                    if menu.options[menu.index] == "讀取存檔":
                        load()
                        main()
                        sys.exit()
                    if menu.options[menu.index] == "退出遊戲":
                        sys.exit()
                   

titlescreen()