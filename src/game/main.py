from random import random


TEXT_AREA = {
    # Словарь для формирования текста
    0: None,
    1: "голова",
    2: "тело",
    3: "ноги"
}

ATTR_HP = {
    # Почти то же, что TEXT_AREA, но для *attr*()-функций (например в функции Player.attack())
    0: None,
    1: 'hp_head',
    2: 'hp_body',
    3: 'hp_legs'
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

class Player:
    '''
    Homo Sapiens Sapiens
    * name - имя игрока;
    * hp_head, hp_body, hp_legs - здоровье головы, тела и ног;
    * hp - медиана hp_head, hp_body и hp_legs (см. функцию calc_hp());
    * armor - поглощение урона (броня на всё тело);
    * shield_area - если щит стоит там же, куда наносится удар, то будет "непробитие";
    * damage - минимальный наносимый урон;
    * crit_change - шанс нанести крит. удар;
    * crit_damage - минимальная надбавка к уроку при крит. ударе.
    '''
    def __init__(self, name: str, weapon: Weapon, armor: int = 10,
                 hp_head: int = 100, hp_body: int = 100, hp_legs: int = 100,
                 damage: int = 10, crit_chance: float = 0.3, crit_damage = 2.0) -> None:
        self.name: str = name
        self.hp_head: int = hp_head
        self.hp_body: int = hp_body
        self.hp_legs: int = hp_legs
        self.hp: int = calc_hp(self)
        self.armor: int = armor
        self.shield_area: int = 0
        self.damage: int = damage
        self.weapon: Weapon = weapon
        self.crit_chance: float = crit_chance
        self.crit_damage: float = crit_damage

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
        if area == enemy.shield_area:
            return f"{self.name} не пробил оборону {enemy.name} (удар был в {TEXT_AREA[area]})"

        area_hp = ATTR_HP[area]
        crit, crit_val = self.crit()
        
        if crit_val:
            crit_str = "крит. "
        else:
            crit_str = ""

        damage = int(self.damage * crit - enemy.armor) # урон * крит. урон - сила брони противника
        setattr(enemy, area_hp, getattr(enemy, area_hp) - damage) # Отнять здоровье в размере урона (damage) у области куда был совершён удар
        enemy.hp = calc_hp(enemy)

        return f"{self.name} нанес {enemy.name} {damage} ед. {crit_str}урона в {TEXT_AREA[area]}"

    def defense(self, shield_area: int) -> None:
        '''`self.shield_area = shield_area`'''
        self.shield_area = shield_area


# ТЕСТИРОВАНИЕ
from random import randint


Fists = Weapon("Кулаки", 0, 0.0, 0.0)
Claymore = Weapon("Клеймор", 10, 0.1, 1.1)
Stiletto = Weapon("Стилет", 7, 0.4, 0.4)

Timur = Player("Тимурджан", Claymore, 8, damage=15)
Diana = Player("Диана", Fists, 9, crit_chance=0.35, crit_damage=1.9)


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
