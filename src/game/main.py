from random import random


class Weapon:
    def __init__(self, name: str, bonus_damage: int, bonus_crit_chance: float, bonus_сrit_damage: float):
        self.name: str = name
        self.bonus_damage: int = bonus_damage
        self.bonus_crit_chance: float = bonus_crit_chance
        self.bonus_сrit_damage: int = bonus_сrit_damage

class Player:
    def __init__(self, name: str, is_bot: bool, hp: int, damage: int, armor: int, crit_chance: float, сrit_damage: float, weapon: Weapon):
        self.name: str = name
        self.is_bot: bool = is_bot
        self.hp: int = hp
        self.damage: int = damage + weapon.bonus_damage
        self.armor: int = armor
        self.crit_chance: float = crit_chance + weapon.bonus_crit_chance
        self.сrit_damage: int = сrit_damage + weapon.bonus_сrit_damage
        self.weapon: Weapon = weapon

    def crit(self) -> int | bool:
        roll = random()

        if roll <= self.crit_chance:
            return self.сrit_damage, True
        else:
            return 1, False
    
    def attack(self, enemy: Player) -> str:
        crit, crit_val = self.crit()
        
        if crit_val:
            crit_str = "крит. "
        else:
            crit_str = ""

        damage = round(max(0, self.damage * crit - enemy.armor), 1)
        enemy.hp -= damage

        return f"{self.name} нанес {enemy.name} {damage} ед. {crit_str}урона"


Claymore = Weapon("Клеймор", 10, 0.1, 1.1)
Stiletto = Weapon("Стилет", 7, 0.4, 0.4)

Timur = Player("Тимурджан", False, 100, 15, 3, 0.30, 2.0, Claymore)
Gaine = Player("Генджел", False, 100, 10, 5, 0.35, 1.9, Stiletto)


while True:
    print(Gaine.attack(Timur))
    if Timur.hp <= 0:
        print(f"{Gaine.name} победилa!")
        break
    print(Timur.attack(Gaine))
    if Gaine.hp <= 0:
        print(f"{Timur.name} победил!")
        break
