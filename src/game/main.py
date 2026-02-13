from random import random, randint


DD_AREAS = {
    0: None,
    1: "голова",
    2: "тело",
    3: "ноги"
}


def calc_hp(player: Player) -> int:
    '''Возвращает общее состояние (`hp`) игрока, подсчитывая медиану здоровья головы, тела и ног'''
    return player.hp_head + player.hp_body + player.hp_legs - min(player.hp_head, player.hp_body, player.hp_legs) - max(player.hp_head, player.hp_body, player.hp_legs)


class Weapon:
    def __init__(self, name: str, bonus_damage: int, bonus_crit_chance: float, bonus_crit_damage: float) -> None:
        self.name: str = name
        self.bonus_damage: int = bonus_damage
        self.bonus_crit_chance: float = bonus_crit_chance
        self.bonus_crit_damage: float = bonus_crit_damage

class Armor:
    def __init__(self, name: str, helmet: int, chestplate: int, greaves: int) -> None:
        self.name = name
        self.helmet = helmet
        self.chestplate = chestplate
        self.greaves = greaves

class Player:
    def __init__(self, name: str, weapon: Weapon, armor: Armor,
                 hp_head: int = 100, hp_body: int = 100, hp_legs: int = 100,
                 damage: int = 10, crit_chance: float = 0.3, crit_damage = 2.0) -> None:
        self.name = name
        self.hp_head = hp_head
        self.hp_body = hp_body
        self.hp_legs = hp_legs
        self.hp = calc_hp(self)
        self.armor = armor
        self.damage = damage
        self.weapon = weapon
        self.crit_chance = crit_chance
        self.crit_damage = crit_damage

    def crit(self) -> tuple[float, bool]:
        roll = random()

        if roll <= self.crit_chance:
            return self.crit_damage, True
        else:
            return 1, False
    
    def attack(self, enemy: Player, area: int) -> str:
        crit, crit_val = self.crit()
        
        if crit_val:
            crit_str = "крит. "
        else:
            crit_str = ""

        damage = 0
        match area:
            case 1:
                damage = int(self.damage * crit - enemy.armor.helmet)
                enemy.hp_head -= damage
            case 2:
                damage = int(self.damage * crit - enemy.armor.chestplate)
                enemy.hp_body -= damage
            case 3:
                damage = int(self.damage * crit - enemy.armor.greaves)
                enemy.hp_legs -= damage

        enemy.hp = calc_hp(enemy)

        return f"{self.name} нанес {enemy.name} {damage} ед. {crit_str}урона в {DD_AREAS[area]}\n"

# ТЕСТИРОВАНИЕ
Chainmail = Armor("Кольчуга", 7, 10, 4)

Claymore = Weapon("Клеймор", 10, 0.1, 1.1)
Stiletto = Weapon("Стилет", 7, 0.4, 0.4)

Timur = Player("Тимурджан", Claymore, Chainmail, damage=15)
Gaine = Player("Генджел", Stiletto, Chainmail, crit_chance=0.35, crit_damage=1.9)


while True:
    print(Gaine.attack(Timur, randint(1, 3)))
    if Timur.hp <= 0:
        print(f"{Gaine.name} победилa!")
        break
    print(Timur.attack(Gaine, randint(1, 3)))
    if Gaine.hp <= 0:
        print(f"{Timur.name} победил!")
        break
