from yeastr_test import match_game

def inputs():
    yield 'pick PC up'
    yield 'press Q'

    yield 'go east'
    yield 'look'
    yield 'get Bed'
    yield 'look'
    yield 'get PC'
    yield 'look'
    yield 'press s'
    yield 'drop PC Bed'
    yield 'press s'
    yield 'north'
    yield 'pick up Mirror'

    yield 'get PC'
    yield 'click 50 100'
    yield 'press s'
    yield 'pick up Bed'
    yield 'press s'
    yield 'quit'

    yield 'clickm 3 5 r'
    yield 'clickd 3 5'
    yield 'quit'

inputs = inputs()
match_game.input = lambda _: next(inputs)

for _ in range(4):
    match_game.play()
    print('GAME OVER')
