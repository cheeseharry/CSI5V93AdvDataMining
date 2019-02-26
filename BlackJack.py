import random
from functools import reduce


# init_game
def init_game():
    print('***************************************************')
    print('Welcome to BlackJack！')
    user = [shufflecard(), shufflecard()]
    ai = [shufflecard(), shufflecard()]
    ai_hide = [ai[0], 'Hide']
    print('Your cards：', user)
    print('Dealer cards：', ai_hide)
    if sum(user) > 21:
        print('You lose！Your cards', user, '，total', sum(user), '，You busted。')
        return init_game()
    elif sum(user) == 21:
        print('You win! You got a blackjack.！')
        return init_game()
    elif sum(ai) > 21:
        print('You win！Dealer total is', sum(ai), '，Dealer busted。')
        return init_game()
    elif sum(ai) == 21:
        print('You lose. The dealer got a blackjack.！')
        return init_game()
    elif sum(user) > 21 and sum(ai) > 21:
        print('Tie！Your score is ', sum(user), '，Dealer score is ', sum(ai), 'You and Dealer both busted!')
        return init_game()
    else:
        judge(user, ai, ai_hide)
        decision(user, ai)


# judege
def judge(user, ai, ai_hide):
    decision = str(input('Would You Hit?，“h” = hit，“s” = stop（h/s）：')).lower()
    if decision == 'h':
        user.append(shufflecard())
        ai.append(shufflecard())
        ai_hide.append('Hide')
        if sum(user) > 21:
            print('You lose！Your cards', user, '，total', sum(user), '，You busted。')
            return init_game()
        elif sum(user) == 21:
            print('You win! You got a blackjack.！')
            return init_game()
        elif sum(ai) > 21:
            print('You win！Dealer total is', sum(ai), '，Dealer busted。')
            return init_game()
        elif sum(ai) == 21:
            print('You lose. The dealer got a blackjack.！')
            return init_game()
        elif sum(user) > 21 and sum(ai) > 21:
            print('Tie！Your score is ', sum(user), '，Dealer score is ', sum(ai), 'You and Dealer both busted!')
            return init_game()
        else:
            print('Your cards：', user)
            print('Dealer cards：', ai_hide)
            return judge(user, ai, ai_hide)
    elif decision == 's':
        return


# Cards
cards = [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 8, 9, 9, 9, 9, 10,
         10, 10, 10, 11, 11, 11, 11, 12, 12, 12, 12, 13, 13, 13, 13]


# shuffle Cards
def shufflecard():
    index = random.randint(0, len(cards) - 1)
    shufflecard = cards[index]
    del cards[index]
    if len(cards) == 0:
        print('Game over! Run out of cards!')
        return init_game()
    else:
        return shufflecard


# sum
def sum(user):
    return reduce(lambda x, y: x + y, user)


# decision
def decision(user, ai):
    minus_user = 21 - sum(user)
    minus_ai = 21 - sum(ai)
    if minus_user < minus_ai:
        print('Congratulations! You win! Your score is ', sum(user), '，Dealer score is ', sum(ai), '。')
        return init_game()
    elif minus_user > minus_ai:
        print('Sorry You lose. Your score is ', sum(user), '，Dealer score is ', sum(ai))
        return init_game()
    elif minus_user == minus_ai:
        print('Tie! Your score is ', sum(user), '，Dealer score is ', sum(ai), '。')
        return init_game()


# start
if __name__ == '__main__':
    init_game()
    pass
