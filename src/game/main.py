from random import random


TEXT_AREA = {
    0: None,
    1: "голова",
    2: "корпус",
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


# КЛАССЫ
class Weapon:
    '''
    Класс оружия.
    Увеличивает минимальный наносимый урон, шанс нанести крит. и увеличивает минимальный наносимый крит. урон.
    '''
    def __init__(self, name: str, bonus_damage: int, bonus_crit_chance: float, bonus_crit_damage: float) -> None:
        self.name: str = name
        self.bonus_damage: int = bonus_damage
        self.bonus_crit_chance: float = bonus_crit_chance
        self.bonus_crit_damage: float = bonus_crit_damage

NoWeapon = Weapon("Без оружия", 0, 0.0, 0.0)

class Entity:
    def __init__(self, name: str, hp: int = 100,
                 damage: int = 10, weapon: Weapon = NoWeapon,
                 armor: int = 10, crit_chance: float = 0.3, crit_damage = 2.0) -> None:
        self.name: str = name
        self.hp: int = hp
        self.damage: int = damage
        self.weapon: Weapon = weapon
        self.armor: int = armor
        self.shield_area: int = 0
        self.crit_chance: float = crit_chance
        self.crit_damage: float = crit_damage
        self.exp: int = 10

    def crit(self) -> tuple[float, bool]:
        '''Подсчитывает и возвращает критический урон, основываясь на изначальных значениях (`self.crit_chance`, `self.crit_damage`).'''
        roll = random()

        if roll <= self.crit_chance:
            # Если выпавшее число меньше или равно базовому шансу, то возвращаем базовый крит. урон
            return self.crit_damage, True
        else:
            return 1, False

    def attack(self, enemy: Entity, area: int) -> str:
        '''
        Наносит урон противнику (`enemy`) с учётом крита.
        Возвращает string, который сразу можно вывести как итог удара.
        '''
        if area == enemy.shield_area:
            return f"{self.name} не пробил оборону ({TEXT_AREA[area]})"

        crit, crit_val = self.crit()

        if crit_val:
            crit_str = "крит. "
        else:
            crit_str = ""

        damage = int(self.damage * crit - enemy.armor)  # урон * крит. урон - сила брони противника
        enemy.hp -= damage

        return f"{self.name} нанес {enemy.name} {damage} ед. {crit_str}урона в {TEXT_AREA[area]}"

    def defense(self, shield_area: int) -> None:
        '''
        Выставляет щит (`Player.shield_area`) в указанную зону.
        `self.shield_area = shield_area`
        '''
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

        self.exp -= 1

        return f"Параметр \"{TEXT_PLAYER_PARAMS[param_to_upgrade]}\" увеличен до {new_value}"

# ТЕСТИРОВАНИЕ
Sword = Weapon("Меч", 10, 0.1, 1.0)

Teamur = Entity("Тимурджан", damage=15, weapon=Sword)
Diana = Entity("Диана", crit_chance=0.35, crit_damage=1.9)

from random import randint
while True:
    Teamur.defense(randint(1, 3))
    print(Diana.attack(Teamur, randint(1, 3)))
    if Teamur.hp <= 0:
        print(Diana.name + " победила!")
        break

    Diana.defense(randint(1, 3))
    print(Teamur.attack(Diana, randint(1, 3)))
    if Diana.hp <= 0:
        print(Teamur.name + " победил!")
        break
