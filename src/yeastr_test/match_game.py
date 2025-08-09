from abc import ABC, abstractmethod

@def_macro()
def describe_macro():
    print(self.name)
    print('Objects:', ', '.join(self.objects))
    print('Directions:', ', '.join(emap(
        lambda direction, room:
            f'{direction}={room.name}',
        self.directions.items()
    )))

class Room(ABC):
    name = 'Room'
    #objects = []
    #directions = {}

    def describe(self):
        describe_macro()

    @abstractmethod
    def neighbor(self, direction): ...

    @property
    def exits(self):
        return self.directions.keys()

class MainRoom(Room):
    name = 'Main'
    objects = ['PC', 'Bed']

    def neighbor(self, direction):
        return self.directions.get(direction, self)

class KitchenRoom(Room):
    name = 'Kitchen'
    objects = ['Cofee', 'Moka']

    def neighbor(self, direction):
        return self.directions.get(direction, self)

class MirrorsRoom(Room):
    name = 'Mirrors'
    objects = ['Mirror', ]

    def neighbor(self, direction):
        if direction == 'back':
            return MainRoom()
        print('You get lost and starved to death')
        raise Break('mainloop')

MainRoom.directions = {
    'est': KitchenRoom(),
    'north': MirrorsRoom(),
}
KitchenRoom.directions = {
    'west': MainRoom(),
}
MirrorsRoom.directions = {
    'back': MainRoom(),
}

class Character:
    def __init__(self):
        self.objects = []

    def get(self, obj, current_room):
        if obj in current_room.objects:
            if obj == 'Mirror':
                print('You became a narcisist, forgot to eat then died')
                raise Break('mainloop')
            current_room.objects.remove(obj)
            self.objects.append(obj)
            return obj
        print('Endless research lead to death')
        raise Break('mainloop')

    def drop(self, obk, current_room):
        if obj in self.objects:
            self.objects.remove(obj)
            current_room.objects.append(obj)
        else:
            print('You looked hard, then started to look inside your body, you\'re now dead in a pool of blood')
            raise Break('mainloop')


character = Character()
current_room = MainRoom()


with While(True) as mainloop:
    print(f'In your pockets: {character.objects}')
    command = input('Command:')
    match command.split():
        case ["quit"]:
            print("Goodbye!")
            mainloop.Break
        case ["look"]:
            current_room.describe()
        case ["get", obj]:
            character.get(obj, current_room)
        case ["north"] | ["go", "north"]:
            current_room = current_room.neighbor("north")
        case ["go", ("north" | "south" | "east" | "west") as direction]:
            print(f'You tried to go {direction}')
            print('but nah...')
        case ["go", direction] if direction in current_room.exits:
            current_room = current_room.neighbor(direction)
        case ["go", _]:
            print("Sorry, you can't go that way")
        case ["get", obj] | ["pick", "up", obj] | ["pick", obj, "up"]:
            character.get(obj, current_room)
        case ["drop", *objects, 'Hearth']:
            print('You don\'t have one, died')
            mainloop.Break
        case ["drop", *objects]:
            print(f'dropping {objects}')
            for obj in objects:
                character.drop(obj, current_room)
        case _:
            print(f"Sorry, I couldn't understand {command!r}")
