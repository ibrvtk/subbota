from random import random


TEXT_AREA = {
    # Словарь для формирования текста
    0: None,
    1: "голова",
    2: "тело",
    3: "ноги"
}

# Словари для функций *attr()
ATTR_HP = {
    1: 'hp_head',
    2: 'hp_body',
    3: 'hp_legs'
}
ATTR_ARMOR = {
    1: 'helmet',
    2: 'chestplate',
    3: 'greaves'
}


def calc_hp(player: Player) -> int:
    '''Возвращает общее состояние (`hp`) игрока, подсчитывая медиану здоровья головы, тела и ног.'''
    return player.hp_head + player.hp_body + player.hp_legs - min(player.hp_head, player.hp_body, player.hp_legs) - max(player.hp_head, player.hp_body, player.hp_legs)


class Weapon:
    '''
    Класс оружия. Выдаётся игроку (`class Player`).
    Увеличивает минимальный наносимый урон, шанс нанести крит. и увеличивает минимальный наносимый крит. урон.
    '''
    def __init__(self, name: str, bonus_damage: int, bonus_crit_chance: float, bonus_crit_damage: float) -> None:
        self.name: str = name
        self.bonus_damage: int = bonus_damage
        self.bonus_crit_chance: float = bonus_crit_chance
        self.bonus_crit_damage: float = bonus_crit_damage

class Armor:
    '''
    Класс брони. Выдаётся игроку (`class Player`).
    Понижает получаемый урон.
    Суммируется с щитом (`Player.shield`).
    '''
    def __init__(self, name: str, helmet: int = 7, chestplate: int = 15, greaves: int = 7) -> None:
        self.name = name
        self.helmet = helmet
        self.chestplate = chestplate
        self.greaves = greaves

class Player:
    def __init__(self, name: str, weapon: Weapon, armor: Armor,
                 hp_head: int = 100, hp_body: int = 100, hp_legs: int = 100,
                 defense: int = 7, damage: int = 10, crit_chance: float = 0.3, crit_damage = 2.0) -> None:
        self.name = name
        self.hp_head = hp_head
        self.hp_body = hp_body
        self.hp_legs = hp_legs
        self.hp = calc_hp(self)
        self.shield = defense
        self.armor = armor
        self.shield_area = 0
        self.damage = damage
        self.weapon = weapon
        self.crit_chance = crit_chance
        self.crit_damage = crit_damage

    def crit(self) -> tuple[float, bool]:
        '''Подсчитывает и возвращает критический урон, основываясь на изначальных значениях (`self.crit_chance`, `self.crit_damage`).'''
        roll = random()

        if roll <= self.crit_chance:
            return self.crit_damage, True
        else:
            return 1, False
    
    def attack(self, enemy: Player, area: int) -> str:
        '''
        Наносит урон противнику (`enemy`) с учётом крита.
        Возвращает string, который сразу можно вывести как итог удара.
        '''
        area_armor = ATTR_ARMOR[area]
        area_hp = ATTR_HP[area]
        crit, crit_val = self.crit()
        
        if crit_val:
            crit_str = "крит. "
        else:
            crit_str = ""

        damage = int(self.damage * crit - getattr(enemy.armor, area_armor)) # урон * крит. урон - сила брони противника (в этой области)
        text = f"{self.name} нанес {enemy.name} {damage} ед. {crit_str}урона в {TEXT_AREA[area]}"

        if area == enemy.shield_area:
            # Если зона удара совпадает с зоной где у противника стоит щит, то отнять от значения урона значение силы щита противника
            damage -= enemy.shield
            text += " (защита)"

        setattr(enemy, area_hp, getattr(enemy, area_hp) - damage) # Отнять здоровье в размере урона (damage) у области куда был совершён удар
        enemy.hp = calc_hp(enemy)

        return f"{text}\n"

    def defense(self, shield_area: int) -> None:
        '''`self.shield_area = shield_area`'''
        self.shield_area = shield_area


# ТЕСТИРОВАНИЕ
from random import randint


Chainmail = Armor("Кольчуга", chestplate=10, greaves=4)

Claymore = Weapon("Клеймор", 10, 0.1, 1.1)
Stiletto = Weapon("Стилет", 7, 0.4, 0.4)

Timur = Player("Тимурджан", Claymore, Chainmail, damage=15)
Gaine = Player("Генджел", Stiletto, Chainmail, crit_chance=0.35, crit_damage=1.9)


while True:
    Timur.defense(randint(1, 3))
    print(Gaine.attack(Timur, randint(1, 3)))
    if Timur.hp <= 0:
        print(f"{Gaine.name} победилa!")
        break
    Gaine.defense(randint(1, 3))
    print(Timur.attack(Gaine, randint(1, 3)))
    if Gaine.hp <= 0:
        print(f"{Timur.name} победил!")
        break
