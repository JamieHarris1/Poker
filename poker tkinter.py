from tkinter import *
import tkinter as tk
from tkinter import ttk
import random
from PIL import Image, ImageTk


f=open("cards.txt","r")
data=f.readlines()
f.close()
root = tk.Tk()
f=Frame(root)
root.title("Poker")
root.geometry('800x600')
root.configure(bg='white')

#Poker Hands
RFs=[['01c','Kc','Qc','Jc','10c'],['01s','Ks','Qs','Js','10s'],['01d','Kd','Qd','Jd','10d'],['01h','Kh','Qh','Jh','10h']]
suits=['c','d','s','h']
numbers=['01','2','3','4','5','6','7','8','9','10','J','Q','K']
scores=[22,21,20,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1]
hands_w=['Royal Flush','Straight Flush','Four of a Kind','Full House','Flush','Straight','Three of a Kind','Two Pair','One Pair','High Card: ']
Flush_Coordinates=[10,110,210,310,410]
Playing=True
P_Account=1000
C_Account=1000
Locked=False
R=1

Player_Bet= tk.StringVar(root)
Computer_Bet= tk.StringVar(root)
Log=tk.StringVar(root)
Log2=tk.StringVar(root)
Player_Account=tk.StringVar(root)
Computer_Account=tk.StringVar(root)


def Flop():
    c=random.choice(data)
    data.remove(c)
    c=str(c).replace('\n','')
    return c

def Hands():
    hands=[]
    for i in range(2):
        c1=random.choice(data)
        data.remove(c1)
        c1=str(c1).replace('\n','')
        c2=random.choice(data)
        data.remove(c2)
        c2=str(c2).replace('\n','')
        
        hands=hands+[str(c1+','+c2)]
    return hands


def P_Add():
    global Player_Bet
    if Locked==False:
        if int(Player_Bet.get())<P_Account:
            Player_Bet.set(int(Player_Bet.get())+100)

def P_Minus():
    global Player_Bet
    if Locked==False:
        if int(Player_Bet.get())>0:
            Player_Bet.set(int(Player_Bet.get())-100)

def C_Add():
    global Player_Bet
    if int(Player_Bet.get())<P_Account:
        
        Player_Bet.set(int(Player_Bet.get())+100)

def C_Minus():
    global Player_Bet
    if int(Player_Bet.get())>0:
        Player_Bet.set(int(Player_Bet.get())-100)

def Fold():
    global P_Account
    global C_Account
    global river
    global river2
    P_Account+=-int(Player_Bet.get())
    C_Account+=int(Player_Bet.get())
    Player_Account.set(P_Account)
    Computer_Account.set(C_Account)
    river.place_forget()
    river2.place_forget()
    Start()

def C_Fold():
    global P_Account
    global C_Account
    P_Account+=int(Computer_Bet.get())
    C_Account+=-int(Player_Bet.get())
    Player_Account.set(P_Account)
    Computer_Account.set(C_Account)
    Start()
    
def Match():
    global Player_Bet
    global R
    global P_hand
    global C_hand
    R+=1
    
    Player_Bet.set(int(Computer_Bet.get()))
    
    if R==2:
        Round2()
    elif R==3:
        Round3()
    else:
        print(1)
        P_score=Who_Win(P_hand,flop)
        C_score=Who_Win(C_hand,flop)
        for i in range(len(scores)):
            if int(P_score)==scores[i]:
                if scores[i]<14:
                    print('Player had: '+hands_w[-1])
                    Log.set('Player  had:'+str(hands_w[-1]))
                    Log2.set( 'Computer had:'+str(hands_w[-1]))
                else:
                    Log.set('Player  had:'+str(hands_w[i]))
                    Log2.set( 'Computer had:'+str(hands_w[i]))
                    print('Player had: '+hands_w[i])
        

        if Who_Win(C_hand,flop)>Who_Win(P_hand,flop):
            Fold()
        elif Who_Win(C_hand,flop)<Who_Win(P_hand,flop):
            C_Fold()
        else:
            
            print('tie')
            P_score=HC(P_hand)
            C_score=HC(C_hand)
            if C_score>P_score:
                print('computer has higher card')
                Log.set('tie')
                Log2.set('Computer had HC of:'+str(C_score))
                Fold()
            elif C_score<P_score:
                print('Player has higher card')
                Log.set('tie')
                Log2.set('Player had HC of:'+str(P_score))
                C_Fold()
                

    
    Round2()
def Round2():
    global Locked
    global flop
    global river
    
    Locked=False
    for i in range(3,4):  
        path = "Card Images/"+flop[i][:-1]+flop[i][-1].upper()+".jpg"
        img = ImageTk.PhotoImage(Image.open(path))
        river = Label(root, image=img,height=100,width=65)
        river.photo = img
        river.place(x=Flush_Coordinates[i],y=10)
def Round3():
    global river2

    for i in range(4,5):  
        path = "Card Images/"+flop[i][:-1]+flop[i][-1].upper()+".jpg"
        img = ImageTk.PhotoImage(Image.open(path))
        river2 = Label(root, image=img,height=100,width=65)
        river2.photo = img
        river2.place(x=Flush_Coordinates[i],y=10)

def Who_Win(hand,flop):
    cards=hand+flop
    cards_temp=hand+flop
    cards_temp_2=hand+flop
    cards_temp_3=hand+flop
    if RF(cards):
        score=22
    elif SF(cards_temp_3):
        score=21
    elif FOAK(cards):
        score=20
    elif FH(cards):
        score=19
    elif F(cards_temp_2):
        score=18
    elif S(cards_temp):
        score=17
    elif TOAK(cards):
        score=16
    elif TP(cards):
        score=15
    elif OP(cards):
        score=14
    else:
        score=HC(cards_temp_3)
        
    return score
def RF(cards):
    rf=False
    for i in RFs:
        result=all(elem in cards  for elem in i)
        if result:
            rf=True
    if rf==True:
        return True
    else:
        return False
        
def SF(cards_temp_3):
    sf=False
    suits_5=False
    delete=[]
    new_cards=[]
   
    for i in suits:
        if sum(s.count(i) for s in cards_temp_3)>=5:
            suits_5=True
            num=i
    
    if suits_5==True:
        for z in range(len(cards_temp_3)):
            if num in cards_temp_3[z]:
                cards_temp_3[z]=cards_temp_3[z][:-1]
                
                
    
                if cards_temp_3[z]=='K':
                    cards_temp_3[z]='13'
                if cards_temp_3[z]=='Q':
                    cards_temp_3[z]='12'
                if cards_temp_3[z]=='J':
                    cards_temp_3[z]='11'
                cards_temp_3[z]=int(cards_temp_3[z])
                new_cards=new_cards+[cards_temp_3[z]]
       
       
        new_cards=list( dict.fromkeys(new_cards))
        new_cards.sort()
        
        
        try:
            if new_cards[0]+4==new_cards[4]:
                sf=True
        except:
            pass
        try:
            if new_cards[1]+4==new_cards[5]:
                sf=True
        except:
            pass
        try:
            if new_cards[2]+4==new_cards[6]:
                sf=True
        except:
            pass
       



    if suits_5==True and sf==True:
        return True
    else:
        return False
def FOAK(cards):
    foak=False
    for i in numbers:
        if sum(s.count(i) for s in cards)>=4:
            foak=True
    if foak==True:
        return True
    else:
        return False
    
def FH(cards):
    sets=[]
    fh=False
    three=False
    for i in numbers:
        if sum(s.count(i) for s in cards)>=3:
            three=True
        if sum(s.count(i) for s in cards)>=2:
            sets=sets+[i]
        if three==True and len(sets)>1:
            fh=True
    
    if fh==True:
        return True
    else:
        return False
def F(cards_temp_2):
    f=False
    for i in range(len(cards_temp_2)):
        cards_temp_2[i]=cards_temp_2[i][1]
    for i in suits:
        if sum(s.count(i) for s in cards_temp_2)>=5:
            f=True
    
    if f==True:
        return True
    else:
        return False
    

def S(cards_temp):
    s=False
    for i in range(len(cards_temp)):
        cards_temp[i]=cards_temp[i][:-1]
        
        
        if cards_temp[i]=='K':
            cards_temp[i]='13'
        if cards_temp[i]=='Q':
            cards_temp[i]='12'
        if cards_temp[i]=='J':
            cards_temp[i]='11'
        cards_temp[i]=int(cards_temp[i])
    cards_temp=list( dict.fromkeys(cards_temp))
    cards_temp.sort()
    
    try:
        if cards_temp[0]+4==cards_temp[4]:
            s=True
    except:
        pass
    try:
        if cards_temp[1]+4==cards_temp[5]:
            s=True
    except:
        pass
    try:
        if cards_temp[2]+4==cards_temp[6]:
            s=True
    except:
        pass
    
    if s==True:
        return True
    
    else:
        return False
    
def TOAK(cards):

    toak=False
    for i in numbers:
        if sum(s.count(i) for s in cards)>=3:
            toak=True
    if toak==True:
        return True
    else:
        return False
def TP(cards):
    sets=[]
    tp=0
    for i in numbers:
        if sum(s.count(i) for s in cards)==2:
            tp+=1
    if tp>=2:
        return True
    else:
        return False
def OP(cards):
    
    sets=[]
    op=0
    count=0
    num=0
    for i in numbers:
        if sum(s.count(i) for s in cards)>=2:
            
            num=i
    
    for i in cards:
        
        if num==i[:-1]:
            count=count+1
    
    if count==2:
        return True
    else:
        return False
def HC(cards_temp):
    for i in range(len(cards_temp)):
    
        cards_temp[i]=cards_temp[i][:-1]
        if cards_temp[i]=='K':
            cards_temp[i]='13'
        if cards_temp[i]=='Q':
            cards_temp[i]='12'
        if cards_temp[i]=='J':
            cards_temp[i]='11'
        cards_temp[i]=int(cards_temp[i])
    cards_temp.sort()
    
    return cards_temp[-1]
def Confirm():
    global Locked
    global R
    Locked=True



    num=random.randint(1,2)
    
    if num==1:
        Log.set('computer matched')
        Computer_Bet.set(Player_Bet.get())
        Match()
        
    if num==2:
        Log.set('computer raised')
        amount=int(Player_Bet.get())+random.randrange(100,1000,100)
        if amount>C_Account:
            amount=C_Account
        Computer_Bet.set(str(amount))
        Locked=False
    if num==3:
        Log.set('computer folded')
        C_Fold()
    
def Start():
    print(1)
    Locked=False
    R=1
    global flop
    global panel
    global P_hand
    global C_hand
    flop=[Flop()]+[Flop()]+[Flop()]+[Flop()]+[Flop()]
    hands=Hands()
    P_hand=hands[0].split(',')
    C_hand=hands[1].split(',')
    for i in range(len(flop)-2):  
        path = "Card Images/"+flop[i][:-1]+flop[i][-1].upper()+".jpg"
        img = ImageTk.PhotoImage(Image.open(path))
        panel = Label(root, image=img,height=100,width=65)
        panel.photo = img
        panel.place(x=Flush_Coordinates[i],y=10)


    l=Label(root,text='Player hand', height=3,width=10).place(x=60,y=210)
    l=Label(root,text='Currnet Bet', height=3,width=10).place(x=260,y=210)
    Player_Bet_l=Label(root,textvariable=Player_Bet, height=3,width=10).place(x=260,y=310)
    Player_Bet.set(0)

    add_b=Button(root,text='+', height=3,width=10,command=P_Add).place(x=215,y=370)
    minus_b=Button(root,text='-', height=3,width=10,command=P_Minus).place(x=305,y=370)
    Confirm_b=Button(root,text='Confirm', height=3,width=10,command=Confirm).place(x=215,y=470)

    Confirm_b=Button(root,text='Fold', height=3,width=10,command=Fold).place(x=305,y=470)
    Confirm_b=Button(root,text='Match', height=3,width=10,command=Match).place(x=395,y=470)


    l=Label(root,text='Computer Bet', height=3,width=10).place(x=600,y=10)
    Computer_Bet_l=Label(root,textvariable=Computer_Bet, height=3,width=10).place(x=700,y=10)
    Computer_Bet.set(0)


    Label(root,textvariable=Log, height=3).place(x=550,y=110)
    Label(root,textvariable=Log2, height=3).place(x=550,y=210)

    Label(root,text='Player Account :', height=3).place(x=0,y=110)
    Label(root,textvariable=Player_Account, height=3).place(x=135,y=110)
    Player_Account.set(P_Account)

    Label(root,text='Computer Account :', height=3).place(x=0,y=150)
    Label(root,textvariable=Computer_Account, height=3).place(x=135,y=150)
    Computer_Account.set(C_Account)


    for i in range(len(hands)):  
        path = "Card Images/"+P_hand[i][:-1]+P_hand[i][-1].upper()+".jpg"
        img = ImageTk.PhotoImage(Image.open(path))
        panel = Label(root, image=img,height=100,width=65)
        panel.photo = img
        panel.place(x=Flush_Coordinates[i],y=310)



    if C_Account==0:
        root.destroy()
        print('You win')
    elif P_Account==0:
        root.destroy()
        print('You lose')
    
    root.mainloop()
Start()

