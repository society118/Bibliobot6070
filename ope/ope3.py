class Animal:
    name = "Animal;"
    age = 0
    weight = 0

    def __init__(self, name, age, weight):
        self.name = name
        self.age = age
        self.weight = weight

    def Make_sound(self):
        print("")

class Dog(Animal):
    pass
    def Make_sound(self):
        print("woof - woof")

    def bite(selfs):
        print("arrrrrr")

class Cat(Animal):
    pass
    def Make_sound(self):
        print("meow - meow")

    def play(self):
        print("i can play with my tail")

    class Fish(Animal):
        pass

murka = Cat("Murka", 2, 10)
haski = Dog("Barabos",5,45)
murka.Make_sound()
haski.bite()



