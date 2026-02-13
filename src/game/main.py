from random import random, choice


TEXT_AREA = {
    # Словарь для формирования текста
    0: None,
    1: "голова",
    2: "тело",
    3: "ноги"
}
TEXT_PLAYER_PARAMS = {
    'name': "Имя",
    'hp_head': "Целостность головы",
    'hp_body': "Целостность тела",
    'hp_legs': "Целостность ног",
    'hp': "Общее состояние здоровья",
    'shield_power': "Прочность щита (поглощение урона от атаки)",
    'shield_area': "Место на теле, защищаемое с помощью щита",
    'armor': "Броня",
    'damage': "Минимальный урон",
    'weapon': "Оружие",
    'crit_chance': "Шанс крит. удара",
    'crit_damage': "Минимальный доп. урон при крит-е",
    'points': "Очки прокачки"
}

# Словари для функций *attr()
ATTR_HP = {
    0: None,
    1: 'hp_head',
    2: 'hp_body',
    3: 'hp_legs'
}
ATTR_ARMOR = {
    0: None,
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
    Суммируется с щитом (`Player.shield_power`).
    '''
    def __init__(self, name: str, helmet: int = 7, chestplate: int = 15, greaves: int = 7) -> None:
        self.name: str = name
        self.helmet: int = helmet
        self.chestplate: int = chestplate
        self.greaves: int = greaves

class Player:
    '''Homo Sapiens Sapiens'''
    def __init__(self, name: str, weapon: Weapon, armor: Armor,
                 hp_head: int = 100, hp_body: int = 100, hp_legs: int = 100,
                 shield_power: int = 7, damage: int = 10, crit_chance: float = 0.3, crit_damage = 2.0) -> None:
        self.name: str = name
        self.hp_head: int = hp_head
        self.hp_body: int = hp_body
        self.hp_legs: int = hp_legs
        self.hp: int = calc_hp(self)
        self.shield_power: int = shield_power
        self.shield_area: int = 0
        self.armor: Armor = armor
        self.damage: int = damage
        self.weapon: Weapon = weapon
        self.crit_chance: float = crit_chance
        self.crit_damage: float = crit_damage
        self.points: int = 10

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
            damage -= enemy.shield_power
            text += " (защита)"

        setattr(enemy, area_hp, getattr(enemy, area_hp) - damage) # Отнять здоровье в размере урона (damage) у области куда был совершён удар
        enemy.hp = calc_hp(enemy)

        return f"{text}\n"

    def defense(self, shield_area: int) -> None:
        '''`self.shield_area = shield_area`'''
        self.shield_area = shield_area

    def upgrade(self, param_to_upgrade: str) -> str:
        restricted = ['name', 'hp', 'shield_area', 'armor', 'weapon', 'crit_chance', 'crit_damage', 'points']

        if param_to_upgrade in restricted:
            return "Вы не можете изменить этот параметр!"

        if not hasattr(self, param_to_upgrade):
            raise ValueError(f"Параметр {param_to_upgrade} не существует")

        current_value = getattr(self, param_to_upgrade)
        new_value = current_value + 1
        setattr(self, param_to_upgrade, new_value)

        self.points -= 1

        return f"Параметр \"{TEXT_PLAYER_PARAMS[param_to_upgrade]}\" увеличен до {new_value}"


# ТЕСТИРОВАНИЕ
from random import randint


Naked = Armor("Голое тело", 0, 0, 0)
Chainmail = Armor("Кольчуга", chestplate=10, greaves=4)

Fists = Weapon("Кулаки", 0, 0.0, 0.0)
Claymore = Weapon("Клеймор", 10, 0.1, 1.1)
Stiletto = Weapon("Стилет", 7, 0.4, 0.4)

Timur = Player("Тимурджан", Fists, Naked, damage=15)
Diana = Player("Диана", Fists, Naked, crit_chance=0.35, crit_damage=1.9)


while Timur.points != 0:
    print(Timur.upgrade(choice(list(TEXT_PLAYER_PARAMS))))

while Diana.points != 0:
    print(Diana.upgrade(choice(list(TEXT_PLAYER_PARAMS))))

while True:
    Timur.defense(randint(1, 3))
    print(Diana.attack(Timur, randint(1, 3)))
    if Timur.hp <= 0:
        print(f"{Diana.name} победилa!")
        break
    Diana.defense(randint(1, 3))
    print(Timur.attack(Diana, randint(1, 3)))
    if Diana.hp <= 0:
        print(f"{Timur.name} победил!")
        break
