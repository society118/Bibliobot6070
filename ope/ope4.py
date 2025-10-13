class Car:
    trunk = 0
    engine = 0
    year = 0
    max_speed = 0
    num_doors = 0
    horsepower = 0

    def __init__(self, trunk, engine, year):
        self.trunk = trunk
        self.engine = engine
        self.year = year

    def info(self):
        print(f"Год: {self.year}, Объем двигателя: {self.engine}, Багажник: {self.trunk}")

class Sedan(Car):

    def info(self):
        print(f"Sedan - Год: {self.year}, Объем двигателя: {self.engine}, Багажник: {self.trunk}")

class Jeep(Car):
    def __init__(self , trunk, engine, year, max_speed, num_doors, horsepower):
        super().__init__(trunk, engine, year)
        self.max_speed = max_speed
        self.num_doors = num_doors
        self.horsepower = horsepower

    def info(self):
        print(f"Jeep - Год: {self.year}, Объем двигателя: {self.engine}, Багажник: {self.trunk}, "
              f"Макс. скорость: {self.max_speed}, Дверей: {self.num_doors}, Лошадиные силы: {self.horsepower}")

sedan1 = Sedan(550, 2, 2009)
jeep1 = Jeep(1300, 1.5, 2015, 220, 4, 72)

sedan1.info()
jeep1.info()
#!