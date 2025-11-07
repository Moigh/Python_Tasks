import math

class Weapon:
    def __init__(self, name, damage, range):
        self.name = name
        self.damage = damage
        self.range = range
    
    def hit(self, actor, target):
        if not target.is_alive():
            print("Враг уже повержен")
            return
        
        actor_x, actor_y = actor.get_coords()
        target_x, target_y = target.get_coords()
        distance = math.sqrt((actor_x - target_x)**2 + (actor_y - target_y)**2)
        
        if distance > self.range:
            print(f"Враг слишком далеко для оружия {self.name}")
            return
        
        print(f"Врагу нанесен урон оружием {self.name} в размере {self.damage}")
        target.get_damage(self.damage)
    
    def __str__(self):
        return self.name


class BaseCharacter:
    def __init__(self, pos_x, pos_y, hp):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.hp = hp
    
    def move(self, delta_x, delta_y):
        self.pos_x += delta_x
        self.pos_y += delta_y
    
    def is_alive(self):
        return self.hp > 0
    
    def get_damage(self, amount):
        self.hp = max(0, self.hp - amount)
    
    def get_coords(self):
        return (self.pos_x, self.pos_y)


class BaseEnemy(BaseCharacter):
    def __init__(self, pos_x, pos_y, weapon, hp):
        super().__init__(pos_x, pos_y, hp)
        self.weapon = weapon
    
    def hit(self, target):
        if not isinstance(target, MainHero):
            print("Могу ударить только Главного героя")
            return
        self.weapon.hit(self, target)
    
    def __str__(self):
        return f"Враг на позиции ({self.pos_x}, {self.pos_y}) с оружием {self.weapon}"


class MainHero(BaseCharacter):
    def __init__(self, pos_x, pos_y, name, hp):
        super().__init__(pos_x, pos_y, hp)
        self.name = name
        self.weapons = []
        self.current_weapon_index = -1
    
    def hit(self, target):
        if not self.weapons:
            print("Я безоружен")
            return
        
        if not isinstance(target, BaseEnemy):
            print("Могу ударить только Врага")
            return
        
        current_weapon = self.weapons[self.current_weapon_index]
        current_weapon.hit(self, target)
    
    def add_weapon(self, weapon):
        if not isinstance(weapon, Weapon):
            print("Это не оружие")
            return
        
        self.weapons.append(weapon)
        print(f"Подобрал {weapon}")
        
        if len(self.weapons) == 1:
            self.current_weapon_index = 0
    
    def next_weapon(self):
        if not self.weapons:
            print("Я безоружен")
            return
        
        if len(self.weapons) == 1:
            print("У меня только одно оружие")
            return
        
        self.current_weapon_index = (self.current_weapon_index + 1) % len(self.weapons)
        print(f"Сменил оружие на {self.weapons[self.current_weapon_index]}")
    
    def heal(self, amount):
        self.hp += amount
        if self.hp > 200:
            self.hp = 200
        print(f"Полечился, теперь здоровья {self.hp}")


# Пример
weapon1 = Weapon("Короткий меч", 5, 1)
weapon2 = Weapon("Длинный меч", 7, 2)
weapon3 = Weapon("Лук", 3, 10)
weapon4 = Weapon("Лазерная орбитальная пушка", 1000, 1000)

princess = BaseCharacter(100, 100, 100)
archer = BaseEnemy(50, 50, weapon3, 100)
armored_swordsman = BaseEnemy(10, 10, weapon2, 500)

archer.hit(armored_swordsman)
armored_swordsman.move(10, 10)
print(armored_swordsman.get_coords())  # (20, 20)

main_hero = MainHero(0, 0, "Король Артур", 200)
main_hero.hit(armored_swordsman) 
main_hero.next_weapon() 
main_hero.add_weapon(weapon1) 
main_hero.hit(armored_swordsman) 
main_hero.add_weapon(weapon4) 
main_hero.hit(armored_swordsman) 
main_hero.next_weapon() 
main_hero.hit(princess) 
main_hero.hit(armored_swordsman) 
main_hero.hit(armored_swordsman) 