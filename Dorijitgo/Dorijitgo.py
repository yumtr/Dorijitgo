from tkinter import *
from tkinter import font
from winsound import *
from Card import *
from Player import *
from configuration import *
import random


class Dorijitgo:
    def __init__(self):
        self.window = Tk()
        self.window.title("도리짓고 땡")
        self.window.geometry("800x600")
        self.window.configure(bg="green")
        self.fontstyle = font.Font(self.window, size=24, weight='bold', family='Consolas')
        self.fontstyle2 = font.Font(self.window, size=16, weight='bold', family='Consolas')
        self.setupButton()
        self.setupLabel()
        self.player = [Player("player"), Player("player2"), Player("player3")]
        self.dealer = Player("dealer")
        self.betMoney = [0, 0, 0]
        self.playerMoney = 1000
        self.LcardsPlayer = [[], [], []]
        self.LcardsLabelPlayer = [[], [], []]
        self.LcardsDealer = []
        self.LcardsLabelDealer = []
        self.deckN = 0
        self.round = 0
        self.window.mainloop()

    def setupButton(self):
        self.Won5 = [Button(self.window, text="5만", width=4, height=1, font=self.fontstyle2,
                            command=lambda: self.pressedWon5(0)),
                     Button(self.window, text="5만", width=4, height=1, font=self.fontstyle2,
                            command=lambda: self.pressedWon5(1)),
                     Button(self.window, text="5만", width=4, height=1, font=self.fontstyle2,
                            command=lambda: self.pressedWon5(2))]

        self.Won1 = [Button(self.window, text="1만", width=4, height=1, font=self.fontstyle2,
                            command=lambda: self.pressedWon1(0)),
                     Button(self.window, text="1만", width=4, height=1, font=self.fontstyle2,
                            command=lambda: self.pressedWon1(1)),
                     Button(self.window, text="1만", width=4, height=1, font=self.fontstyle2,
                            command=lambda: self.pressedWon1(2))]
        for i in range(3):
            self.Won5[i].place(x=50 + (i * 200), y=550)
            self.Won1[i].place(x=120 + (i * 200), y=550)

        self.Deal = Button(self.window, text="Deal", width=6, height=1, font=self.fontstyle2, command=self.pressedDeal)
        self.Deal.place(x=600, y=550)
        self.Again = Button(self.window, text="Again", width=6, height=1, font=self.fontstyle2,
                            command=self.pressedAgain)
        self.Again.place(x=700, y=550)

        self.Deal['state'] = 'disabled'
        self.Deal['bg'] = 'gray'
        self.Again['state'] = 'disabled'
        self.Again['bg'] = 'gray'

        # self.test = Button(self.window, text="test", width=6, height=1, font=self.fontstyle2,
        #                    command=lambda: self.test1(0))
        # self.test.place(x=500, y=300)
        # self.test["state"] = "active"
        # self.test["bg"] = "white"

    def setupLabel(self):
        self.LbetMoney = [Label(text="0만", width=6, height=1, font=self.fontstyle, bg="green", fg="orange"),
                          Label(text="0만", width=6, height=1, font=self.fontstyle, bg="green", fg="orange"),
                          Label(text="0만", width=6, height=1, font=self.fontstyle, bg="green", fg="orange")]

        self.LplayerRank = [Label(text="", width=10, height=1, font=self.fontstyle2, bg="green", fg="cyan"),
                            Label(text="", width=10, height=1, font=self.fontstyle2, bg="green", fg="cyan"),
                            Label(text="", width=10, height=1, font=self.fontstyle2, bg="green", fg="cyan")]
        self.Lstatus = [Label(text="", width=5, height=1, font=self.fontstyle, bg="green", fg="red"),
                        Label(text="", width=5, height=1, font=self.fontstyle, bg="green", fg="red"),
                        Label(text="", width=5, height=1, font=self.fontstyle, bg="green", fg="red")]

        for i in range(3):
            self.LbetMoney[i].place(x=60 + (i * 200), y=500)
            self.LplayerRank[i].place(x=80 + (i * 230), y=290)
            self.Lstatus[i].place(x=60 + (i * 230), y=250)

        self.LplayerMoney = Label(text="1000만", width=15, height=1, font=self.fontstyle, bg="green",
                                  fg="blue")
        self.LplayerMoney.place(x=560, y=500)

        self.LdealerRank = Label(text="", width=10, height=1, font=self.fontstyle2, bg="green", fg="cyan")
        self.LdealerRank.place(x=330, y=40)

    def pressedWon5(self, i):
        self.betMoney[i] += 5
        if self.playerMoney >= 5:
            self.LbetMoney[i].configure(text=str(self.betMoney[i]) + "만")
            self.playerMoney -= 5
            self.LplayerMoney.configure(text=str(self.playerMoney) + "만")
            self.Deal["state"] = "active"
            self.Deal["bg"] = "white"
            PlaySound('sounds/chip.wav', SND_FILENAME | SND_ASYNC | SND_ALIAS)
        else:
            self.betMoney[i] -= 5

    def pressedWon1(self, i):
        self.betMoney[i] += 1
        if self.playerMoney >= 1:
            self.LbetMoney[i].configure(text=str(self.betMoney[i]) + "만")
            self.playerMoney -= 1
            self.LplayerMoney.configure(text=str(self.playerMoney) + "만")
            self.Deal["state"] = "active"
            self.Deal["bg"] = "white"
            PlaySound('sounds/chip.wav', SND_FILENAME | SND_ASYNC | SND_ALIAS)
        else:
            self.betMoney[i] -= 1

    def deal(self):
        if self.round == 0:
            for i in range(3):
                self.player[i].reset()
            self.dealer.reset()  # 카드 덱 48장 셔플링 0,1,,.51
            self.cardDeck = [i for i in range(48)]
            random.shuffle(self.cardDeck)
            self.deckN = 0
            for i in range(3):
                self.hitPlayer(i, 0)
            self.hitDealerDown(0)
            PlaySound('sounds/cardFlip1.wav', SND_FILENAME | SND_ASYNC | SND_ALIAS)
        elif self.round == 1:
            for i in range(3):
                for j in range(3):
                    self.hitPlayer(j, i + 1)
                self.hitDealerDown(i + 1)
            PlaySound('sounds/cardFlip1.wav', SND_FILENAME | SND_ASYNC | SND_ALIAS)
        if self.round == 2:
            for j in range(3):
                self.hitPlayer(j, 4)
            self.hitDealerDown(4)
            self.checkWinner()
        else:
            self.round += 1
            for i in range(3):
                self.Won5[i]['state'] = 'active'
                self.Won5[i]['bg'] = 'white'
                self.Won1[i]['state'] = 'active'
                self.Won1[i]['bg'] = 'white'
            self.Deal['state'] = 'disabled'
            self.Deal['bg'] = 'gray'

    def hitPlayer(self, i, n):
        newCard = Card(self.cardDeck[self.deckN])
        self.deckN += 1
        self.player[i].addCard(newCard)
        p = PhotoImage(file="cards/" + newCard.filename())
        self.LcardsPlayer[i].append(Label(self.window, image=p))
        # 파이썬은 라벨 이미지 레퍼런스를 갖고 있어야 이미지가 보임
        self.LcardsPlayer[i][self.player[i].inHand() - 1].image = p
        self.LcardsPlayer[i][self.player[i].inHand() - 1].place(x=50 + (i * 230) + n * 35, y=350)
        # 카드 숫자 라벨 출력
        self.LcardsLabelPlayer[i].append(
            Label(text=newCard.value, width=2, height=1, font=self.fontstyle2, bg="green", fg="white"))
        self.LcardsLabelPlayer[i][self.player[i].inHand() - 1].place(x=70 + (i * 230) + n * 35, y=320)

    def hitDealerDown(self, n):
        newCard = Card(self.cardDeck[self.deckN])
        self.deckN += 1
        self.dealer.addCard(newCard)
        p = PhotoImage(file="cards/cardback.gif")
        self.LcardsDealer.append(Label(self.window, image=p))
        # 파이썬은 라벨 이미지 레퍼런스를 갖고 있어야 이미지가 보임
        self.LcardsDealer[self.dealer.inHand() - 1].image = p
        self.LcardsDealer[self.dealer.inHand() - 1].place(x=300 + n * 35, y=100)
        # 카드 숫자 라벨 출력
        self.LcardsLabelDealer.append(
            Label(text=newCard.value, width=2, height=1, font=self.fontstyle2, bg="green", fg="white"))
        # PlaySound('sounds/cardFlip1.wav', SND_FILENAME)

    def pressedDeal(self):
        self.deal()

    def pressedAgain(self):
        self.LdealerRank.configure(text="")
        self.LplayerMoney.configure(text=str(self.playerMoney) + "만")
        self.betMoney = [0, 0, 0]
        for i in range(3):
            self.Lstatus[i].configure(text="")
            self.LplayerRank[i].configure(text="")
            self.LbetMoney[i].configure(text=str(self.betMoney[i]) + "만")
            for t in self.LcardsPlayer[i]:
                t.destroy()

        for t in self.LcardsDealer:
            t.destroy()
        self.LcardsPlayer = [[], [], []]

        for j in range(3):
            for i in self.LcardsLabelPlayer[j]:
                i.configure(text="")

        self.LcardsLabelPlayer = [[], [], []]
        self.LcardsDealer = []
        for i in self.LcardsLabelDealer:
            i.configure(text="")
        self.LcardsLabelDealer = []

        self.deckN = 0
        self.round = 0
        for i in range(3):
            self.Won5[i]['state'] = 'active'
            self.Won5[i]['bg'] = 'white'
            self.Won1[i]['state'] = 'active'
            self.Won1[i]['bg'] = 'white'
        self.Deal['state'] = 'disabled'
        self.Deal['bg'] = 'gray'
        self.Again['state'] = 'disabled'
        self.Again['bg'] = 'gray'
        PlaySound('sounds/ding.wav', SND_FILENAME | SND_ASYNC | SND_ALIAS)

    def checkWinner(self):
        # 뒤집힌 카드를 다시 그린다.
        for i in range(5):
            p = PhotoImage(file="cards/" + self.dealer.cards[i].filename())
            self.LcardsDealer[i].configure(image=p)  # 이미지 레퍼런스 변경
            self.LcardsDealer[i].image = p  # 파이썬은 라벨 이미지 레퍼런스를 갖고 있어야 이미지가 보임
            self.LcardsLabelDealer[i].place(x=320 + i * 35, y=70)
        for i in range(3):
            self.LplayerRank[i].configure(text="플레이어 족보")
        self.LdealerRank.configure(text="플레이어 족보")

        # 승리판단
        for i in range(3):
            self.Lstatus[i].configure(text="승")
            self.playerMoney += self.betMoney[i] * 2
        PlaySound('sounds/win.wav', SND_FILENAME | SND_ASYNC | SND_ALIAS)
        # PlaySound('sounds/wrong.wav', SND_FILENAME)

        for i in range(3):
            self.Won5[i]['state'] = 'disabled'
            self.Won5[i]['bg'] = 'gray'
            self.Won1[i]['state'] = 'disabled'
            self.Won1[i]['bg'] = 'gray'
        self.Deal['state'] = 'disabled'
        self.Deal['bg'] = 'gray'
        self.Again['state'] = 'active'
        self.Again['bg'] = 'white'


Dorijitgo()
