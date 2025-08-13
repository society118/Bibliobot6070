class Dog:
    name = "bobik"
    age = 7
    weight = 22

    def __init__(self, name, age, weight):
        self.name = name
        self.age = age
        self.weight = weight

    def bark(self):
        print("Woof - Woof")


dog = Dog("bobik", 7, 22)

dog.bark()
