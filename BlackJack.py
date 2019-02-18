import random
from functools import reduce


# 游戏
def game():
    print('***************************************************')
    print('欢迎光临21点！游戏开始！')
    user = [randcard(), randcard()]
    ai = [randcard(), randcard()]
    ai_hide = [ai[0], '暗牌']
    print('您的牌组：', user)
    print('庄家牌组：', ai_hide)
    if sum(user) > 21:
        print('游戏结束！您的牌组是', user, '，点数是', sum(user), '，超过了21点。')
        return game()
    elif sum(user) == 21:
        print('You win! You got a blackjack.！')
        return game()
    elif sum(ai) > 21:
        print('恭喜！您获得了胜利！庄家的点数为', sum(ai), '，超过了21点。')
        return game()
    elif sum(ai) == 21:
        print('You lose. The dealer got a blackjack.！')
        return game()
    elif sum(user) > 21 and sum(ai) > 21:
        print('平局！您的点数是', sum(user), '，庄家的点数是', sum(ai), '。')
        return game()
    else:
        decide(user, ai, ai_hide)
        compare(user, ai)


# 抉择
def decide(user, ai, ai_hide):
    decision = str(input('Would You Hit?，“h” = hit，“s” = stop（h/s）：')).lower()
    if decision == 'h':
        user.append(randcard())
        ai.append(randcard())
        ai_hide.append('暗牌')
        if sum(user) > 21:
            print('游戏结束！您的牌组是', user, '，点数是', sum(user), '，超过了21点。')
            return game()
        elif sum(user) == 21:
            print('You win! You got a blackjack.！')
            return game()
        elif sum(ai) > 21:
            print('恭喜！您获得了胜利！庄家的点数为', sum(ai), '，超过了21点。')
            return game()
        elif sum(ai) == 21:
            print('You lose. The dealer got a blackjack.！')
            return game()
        elif sum(user) > 21 and sum(ai) > 21:
            print('平局！您的点数是', sum(user), '，庄家的点数是', sum(ai), '，你们的点数都超过了21点。')
            return game()
        else:
            print('您的牌组：', user)
            print('庄家牌组：', ai_hide)
            return decide(user, ai, ai_hide)
    elif decision == 's':
        return


# 牌组
cards = [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 8, 9, 9, 9, 9, 10,
         10, 10, 10, 11, 11, 11, 11, 12, 12, 12, 12, 13, 13, 13, 13]


# 发牌
def randcard():
    index = random.randint(0, len(cards) - 1)
    randcard = cards[index]
    del cards[index]
    if len(cards) == 0:
        print('游戏结束！没牌发啦！')
        return game()
    else:
        return randcard


# 求和
def sum(user):
    return reduce(lambda x, y: x + y, user)


# 判断
def compare(user, ai):
    minus_user = 21 - sum(user)
    minus_ai = 21 - sum(ai)
    if minus_user < minus_ai:
        print('恭喜！您获得了胜利！您的点数是', sum(user), '，庄家的点数是', sum(ai), '。')
        return game()
    elif minus_user > minus_ai:
        print('非常遗憾！您输掉了本场对局，您的点数是', sum(user), '，庄家的点数是', sum(ai))
        return game()
    elif minus_user == minus_ai:
        print('平局！您的点数是', sum(user), '，庄家的点数是', sum(ai), '。')
        return game()


# 执行
game()