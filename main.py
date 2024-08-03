from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from direct.actor.Actor import Actor
from ursina.prefabs.health_bar import HealthBar
import tkinter
from tkinter import END
from PIL import ImageTk,Image
import mysql.connector
import random,sys


def tk_window():
        def in_user(e):
                if user.get() == "Username":
                        user.delete(0,END)

        def leave_user(e):
                if user.get() == "":
                        user.insert(0,"Username")

        def in_pass(e):
                if password.get() == "Password":
                        password.delete(0,END)

        def leave_pass(e):
                if password.get() == "":
                        password.insert(0,"Password")

        def login():
                global coin_count,username
                username = user.get()
                passwrd = password.get()
                con = mysql.connector.connect(host = "localhost",user = "root",password = "saran")
                cur = con.cursor()
                cur.execute("CREATE DATABASE IF NOT EXISTS jungle_madness")
                cur.execute("USE jungle_madness")
                cur.execute("CREATE TABLE IF NOT EXISTS game(user varchar(50) PRIMARY KEY,password varchar(30),coins int)")
                con.commit()
                if username != "Username" and passwrd != "Password":
                        cur.execute("SELECT * FROM game")
                        ids = cur.fetchall()
                        for i in ids:
                                if username not in i:
                                        try:
                                                cur.execute("INSERT INTO game VALUES('{}','{}',0)".format(username,passwrd))
                                        except:
                                                pass
                                        con.commit()
                                        coin_count = 0
                                        coin_count_text.text = str(coin_count)
                                elif username == i[0] and passwrd == i[1]:
                                        coin_count = i[2]
                                        coin_count_text.text = str(coin_count)
                                        
                        if ids == []:
                                cur.execute("INSERT INTO game VALUES('{}','{}',0)".format(username,passwrd))
                                con.commit()
                                coin_count = 0
                                coin_count_text.text = str(coin_count)
                        
                        #if coin_count variable not there,**
                        try:
                                file.write("{}|{},{}".format(username,passwrd,coin_count))
                        except NameError: # **username already exists.
                                pass
                        file.flush()
                        win_tk.withdraw()
                        file.close()
                        con.close()
                        app.run()

        #login/ign up page
        win_tk  = tkinter.Tk()
        win_tk.geometry("1024x550")
        win_tk.resizable(False,False)
        login_page = ImageTk.PhotoImage(Image.open("images/login.jpeg"))
        tkinter.Label(win_tk,image = login_page).pack()

        user = tkinter.Entry(win_tk,width = 30,border = 0,bg = "light green",font = ("Microsoft YaHei UI Light",11),borderwidth = 5,relief = "raised")
        user.place(x = 400,y = 310)
        user.insert(0,"Username")
        user.bind("<FocusIn>",in_user)
        user.bind("<FocusOut>",leave_user)

        password = tkinter.Entry(win_tk,width = 30,border = 0,bg = "light green",font = ("Microsoft YaHei UI Light",11),borderwidth = 5,relief = "raised")
        password.place(x = 400,y = 350)
        password.insert(0,"Password")
        password.bind("<FocusIn>",in_pass)
        password.bind("<FocusOut>",leave_pass)

        tkinter.Label(win_tk,text = "Sign Up/Login",bg = "#CC9900",fg = "#33FF66",border = 0,borderwidth = 5,relief = "raised",font = ("Microsoft YaHei UI Light",15,"bold")).place(x = 460,y = 260)
        tkinter.Button(win_tk,text = "Enter",bg = "#009900",activebackground = "#00CC00",font = ("Microsoft YaHei UI Light",11),borderwidth = 5,relief = "raised",command = login).place(x= 510,y = 395)

        win_tk.mainloop()


#initalizing the game window
app = Ursina()

#required variables to be used in
ground_no = 1
grounds = []
coins_list = []
enemys_list = []
player_pos = [-1.4,0,1.4]
pos = 1
score = 0
life_count = 0
spend = 20
position_of_ground = 40
dx = 1.5
play = False

#Interface
interface = Button(icon = "images/Interface.jpeg",scale = (1.8,1))

#Instruction menu
instruction = Button(icon = "images/instructions.png",enabled = False)

#running ground
ground = Entity(model='road/scene.gltf', collider='box',scale = (4.5,4.5,10))
grounds.append(ground)


#player
player_controller = FirstPersonController(speed = 0,speed_z = 0,origin = (0,-1.5,-1.5),collider = "box")
player_controller.position = (0,-1.3,-21) #initial position of the player 
camera.position = (0,.25,0) #position of the camera
player = Entity(rotation_y = 180,rotation_x = 180)

#HealthBar
health_bar = HealthBar(max_value = 200,bar_color = color.rgb(241, 196, 15),roundness = .5,position = (-.75,0.45),show_text = False)
health_bar.value = 0

#scoretext
score_text = Text("0",scale = 4,position = (0,.475),color = color.rgb(46, 204, 113),font = "images/DisneyPark.ttf")

#life span
life1 = Button(icon = "images/life1.png",radius = 20,scale = (.3,.1),position = (.7,.455),enabled = False)
life2 = Button(icon = "images/life2.png",radius = 20,scale = (.3,.1),position = (.7,.455),enabled = False)
life3 = Button(icon = "images/life3.png",radius = 20,scale = (.3,.1),position = (.7,.455),enabled = False)
life4 = Button(icon = "images/life4.png",radius = 20,scale = (.3,.1),position = (.7,.455),enabled = False)
life5 = Button(icon = "images/life5.png",radius = 20,scale = (.3,.1),position = (.7,.455),enabled = False)
life6 = Button(icon = "images/life6.png",radius = 20,scale = (.3,.1),position = (.7,.455),enabled = False)
lives = [life1,life2,life3,life4,life5,life6]

#Pause/Resume button
resume_button = Button(icon = "images/resume.png",radius = .5,scale = (.1,.1),position = (-.835,.455),enabled = False)
pause_button = Button(icon = "images/pause.png",radius = .5,scale = (.1,.1),position = (-.835,.455),enabled = False)
pause_handler = Entity(ignore_paused=True) #To handle the pause and resume of the game

#Texts
gameover_text = Text("Game Over",position = (-.3,.3),color = color.rgb(211,84,0),font = "images/Walt_Disney_Script_v4.1.ttf",scale = 7,enabled = False)
coin_count_text = Text("",position = (-.75,0.4),color = color.rgb(241,196,15),font = "images/Walt_Disney_Script_v4.1.ttf",scale = 5)

#Menu buttons
spend_coins = Button(text = "Spend {}\n\t\tpress ENTER to spend".format(spend),scale = (.1,.1),color = color.lime,text_color = color.rgb( 169, 50, 38),position = (.1,0),enabled = False)
spend_coins.text_entity.scale_y *= 2
spend_coins.text_entity.font = "images/Walt_Disney_Script_v4.1.ttf"

#weapon
actor1 = Actor("weapons/scene.gltf")
actor1.reparentTo(player) #making player as parent
actor1.loop("Armature|Idle")

def screen_off():
        instruction.enabled = False
        life1.enabled = True
        resume_button.enabled = True
        player_controller.speed = 3
        player_controller.speed_z = 10

#to pause and resume the game
def pause_input(key):
        global condition,life_count,coin_count,spend
        if play: #to whether instruction window got off
                if key == 'p' and condition: #while running ------- # "condition"variable is to check whether game paused by user or got over
                        condition = not gameover_text.enabled # set to FALSE if game got over
                        resume_button.enabled = not resume_button.enabled 
                        pause_button.enabled = not pause_button.enabled
                        application.paused = not application.paused #to pause or resume
                
                if coin_count >= spend:
                        if key == "enter" and not condition: #when life got over
                                coin_count -= spend
                                coin_count_text.text = str(coin_count)#changing the value of the coin
                                condition = True # to play normally
                                spend += 20 # increasing the value of the coins spending
                                # set off things that enabled after life = 0
                                spend_coins.enabled = False 
                                gameover_text.enabled = False
                                life_count = 0
                                life6.enabled = False
                                life1.enabled = True
                                health_bar.value = 0
                                resume_button.enabled = not resume_button.enabled
                                pause_button.enabled = not pause_button.enabled
                                application.paused = not application.paused  
        if key == "escape":
                sys.exit()       
pause_handler.input = pause_input


#similar to while. Function automatically invoked for each frame.
def update():
        global ground_no,position_of_ground,ground,life_count,coin_count,condition,dx
        condition = True
        player_controller.rotation = (0,0,0) #setting up the camera rotations

        if play and not instruction.enabled:
                player_controller.z += (dx*time.dt+.05) #player default movement
        
        if position_of_ground > 800:
                dx += .02  * time.dt           #incresing the default speed 
        
        #position of the player to the firstpersoncontroller
        player_controller.x = player_pos[pos]
        player.position = (player_controller.x,player_controller.y+2,player_controller.z+1.5)
        #recreating ground entity on moving
        if player_controller.z > position_of_ground-(20+ground_no*10):
                for i in range(ground_no-1,ground_no):
                        ground = Entity(model='road/scene.gltf', collider='box',position = (0,0,position_of_ground-(ground_no*10)),scale = (4.5,4.5,10))
                        grounds.append(ground)
                        deleted_ground = grounds.pop(0)
                        destroy(deleted_ground)
                        ground_no += 1
                        position_of_ground += 40
                        for i in range(4): #generating new enemys on moving forward
                                enemys()
                                coins()

        # regenerating enemys if no enemys left.
        if len(enemys_list) == 0:
                for i in range(3):
                        enemys()
        if len(coins_list) == 0:
                for i in range(3):
                        coins()
        
        for coin in coins_list:
                coin.rotation_y +=2  #rotating the coins
                #checking coin collision with player
                direction = Vec3(
                        player.forward * (held_keys['w'] - held_keys['s'])
                        + player.right * (held_keys['d'] - held_keys['a'])
                        )
        
                hitinfo_coin = boxcast(player.position,direction,.5,(1,1),coin)
                if hitinfo_coin.hit:
                        destroy(hitinfo_coin.entity)
                        coins_list.remove(hitinfo_coin.entity)
                        coin_count += 1
                        Audio("music/coin.mpga")
                        coin_count_text.text = str(coin_count) #updating the coins collected
                        health_bar.value += 10 #increasing safe health value 
                        #updating coin value in file
                        with open("coin.txt","r+") as file:
                                lis = file.read().split(",")
                                length = len(lis[0]) + 1
                                file.seek(length)
                                file.write(str(coin_count)) 
                                con = mysql.connector.connect(host = "localhost",user = "root",password = "saran")
                                cur = con.cursor()
                                cur.execute("USE jungle_madness")
                                cur.execute("UPDATE game SET coins = {} WHERE user = '{}'".format(coin_count,username))   
                                con.commit()
                                con.close()

        #checking enemy collision with player
        for enemy in enemys_list:
                direction = Vec3(
                        player.forward * (held_keys['w'] - held_keys['s'])
                        + player.right * (held_keys['d'] - held_keys['a'])
                        )
        
                hitinfo_enemy = boxcast(player.position,direction,.5,(2,2),enemy)
                if hitinfo_enemy.hit:
                        destroy(hitinfo_enemy.entity)
                        enemys_list.remove(hitinfo_enemy.entity)
                        if life_count != 5:
                                lives[life_count].enabled = False
                                life_count += 1 
                                lives[life_count].enabled = True
                        else:
                                if health_bar.value == 200:
                                        health_bar.value = 0
                                        life_count = 0
                                        life1.enabled = True
                                        life6.enabled = False
                                else:
                                        if coin_count >= spend:
                                                spend_coins.enabled = True
                                        else:
                                                Text("Press ESCAPE\n to exit",position = (-.4,.1),color = color.rgb(52, 152, 219),font = "images/Walt_Disney_Script_v4.1.ttf",scale = 7)
                                        
                                        gameover_text.enabled = True
                                        pause_input("p")
        spend_coins.text = "Spend {}\n\t\tpress ENTER to spend".format(spend) #increasing the value for each time                               

#Function automatically invoked during any key press.
def input(key):
        global score,play,pos
        input_handler.bind("s","backspace") #unbinding the key 
        if key == "c hold" or key == "c":
                actor1.play("Armature|Fire")
                for enemy in enemys_list:
                        if round(enemy.position[0]) == round(player_controller.position[0]):
                                destroy(enemy)
                                enemys_list.remove(enemy)
        # movement speed of the player
        if held_keys["w"]:
                player_controller.z += (player_controller.speed_z*time.dt)
                score += round(player_controller.speed_z*time.dt+health_bar.value) 
                score_text.text = str(score) #updating the score

        #changing position of player
        if key == "a":
                if pos > 0:
                        pos -= 1
        if key == "d":
                if pos < 2:
                        pos += 1

        if key == "escape": #to exit 
                sys.exit()

        #To start the game
        if key == "tab":
                play = True
                if player_controller.position.z == -21:
                        interface.enabled = False
                        instruction.enabled = True
                        invoke(screen_off,delay = 6)
        
        
#to generate enemys   
def enemys():
        x = random.choice(player_pos)
        z = random.randint(position_of_ground-(ground_no*10),position_of_ground)
        enemy = FrameAnimation3d("hunter/robot",color = color.rgb( 81, 90, 90 ),scale = .01,position = (x,0,z),collider = "box")
        enemys_list.append(enemy)


#to generate coins
def coins():
        x = random.choice(player_pos)
        z = random.randint(position_of_ground-(ground_no*10),position_of_ground)
        coin = Entity(model = "hunter/Coin/Coin.obj",collider = "box",texture = "hunter/Coin/props.png",scale = 3,position = (x,0,z))
        coins_list.append(coin)

# initial coins and enemys              
for i in range(4):
        enemys()
        coins()
    

#setting the image of the sky
Sky(texture = "images/sky.jpg")
mouse.locked = False
mouse.enabled = False   # Turning off the mouse controll
camera.fov = 35         #view distance from camera
#running up the window
#to restore coin value
with open("coin.txt","a+") as file:
        file.seek(0)
        r = file.read()
        s = r.split(",")
        try:
                username = s[0].split("|")[0]
                coin_count = int(s[1])
                coin_count_text.text = str(coin_count)
                app.run()
        except:
                if username == "": #if user not entered any username and pass before.
                        tk_window()
                else:              #if user not played a match.
                        if not play:
                                coin_count = 0
                                coin_count_text.text = str(coin_count)
                                app.run()
                        else:
                                quit()
      









