class Person:
    name = "Person" #поля классу
    attack = 0 #поля классу
    speed = 15 #поля классу

    def __init__(self , name1 , attack1 , speed1):
        super().__init__()
        self.name = name1
        self.attack = attack1
        self.speed = speed1


    def __str__(self):
        return (f"I am {
        self.name
        } and my {self.attack=} "
                f"and my {self.speed=}")


    def say_name(self): #Метод классу
        print(self.name)

criper = Person("cryper", 500, 50 )
criper.say_name()
print(criper)

steve = Person("Steve " ,250 ,150)
steve.say_name()
print(steve)



# zombie = Person()
# zombie.say_name()
# zombie.name = "Zombie"
# zombie.say_name()

