from random import random


TEXT_AREA = {
    0: None,
    1: "голова",
    2: "корпус",
    3: "ноги"
}
TEXT_ARMORELEMENT_TYPE = {
    'helmet': "шлем",
    'chestplate': "нагрудник",
    'greaves': "поножи"
}
TEXT_PLAYER_PARAMS = {
    'name': "имя",
    'hp': "здоровье",
    'damage': "минимальный урон",
    'weapon': "оружие",
    'shield_area': "положение щита",
    'crit_chance': "шанс нанести крит. удар",
    'crit_damage': "минимальный доп. урон при крит-е",
    'exp': "опыт (очки прокачки)"
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

class ArmorElement:
    '''
    Элемент брони.
    * name: str - Название элемента брони (например "Железный шлем");
    * type: str - Должен быть равен только ЛИБО `helmet` ЛИБО `chestplate` ЛИБО `greaves` (шлем, нагрудник, поножи);
    * absorp(tion): int - Поглощение урона;
    * dur(ability): int - Прочность (ЭКСПЕРИМЕНТАЛЬНО. ПОКА НЕ ИСПОЛЬЗУЕТСЯ). Можно оставить `None` (тогда никогда не поломается).
    '''
    def __init__(self, type: str, name: str, absorption: int, durability: int = None) -> None:
        self.type: str = type
        self.name: str = name
        self.absorp: int = absorption
        self.dur: int = durability

NoHelmet = ArmorElement('helmet', "Без шлема", 0)
NoChestplate = ArmorElement('chestplate', "Без нагрудника", 0)
NoGreaves = ArmorElement('greaves', "Без поножей", 0)

class Entity:
    def __init__(self, name: str, hp: int = 100,
                 damage: int = 10, weapon: Weapon = NoWeapon,
                 helmet: ArmorElement = NoHelmet, chestplate: ArmorElement = NoChestplate, greaves: ArmorElement = NoGreaves,
                 crit_chance: float = 0.3, crit_damage = 2.0) -> None:
        self.name: str = name
        self.hp: int = hp
        self.damage: int = damage
        self.weapon: Weapon = weapon
        self.helmet: ArmorElement = helmet
        self.chestplate: ArmorElement = chestplate
        self.greaves: ArmorElement = greaves
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

        damage = 0
        match area:
            # урон * крит. урон - сила брони противника
            case 1:
                damage = int((self.damage * crit) - enemy.helmet.absorp)
            case 2:
                damage = int((self.damage * crit) - enemy.chestplate.absorp)
            case 3:
                damage = int((self.damage * crit) - enemy.greaves.absorp)

        enemy.hp -= damage

        return f"{self.name} нанес {enemy.name} {damage} ед. {crit_str}урона ({TEXT_AREA[area]})"

    def defense(self, shield_area: int) -> None:
        '''
        Выставляет щит (`Player.shield_area`) в указанную зону.
        `self.shield_area = shield_area`
        '''
        self.shield_area = shield_area

    def upgrade(self, param_to_upgrade: str, free: bool = False) -> str:
        '''
        Прокачивает integer-параметр, например дамаг или кол-во здоровья (в определённой зоне).
        Снимает Player.points -= 1, если free не равен True.
        '''
        if not hasattr(self, param_to_upgrade):
            raise ValueError(f"Параметр {param_to_upgrade} не существует")

        restricted = ['name', 'weapon', 'helmet', 'chestplate', 'greaves', 'shield_area', 'crit_chance', 'exp'] # Недоступные для улучшения параметры
        if param_to_upgrade in restricted:
            return "Вы не можете изменить этот параметр!"

        # Берём текущее значение требуемого параметра; прибавляем единицу; устанавливаем новое значение в класс
        current_value = getattr(self, param_to_upgrade)
        new_value = current_value + 1
        setattr(self, param_to_upgrade, new_value)

        if not free:
            self.exp -= 1

        return f"Параметр \"{TEXT_PLAYER_PARAMS[param_to_upgrade]}\" увеличен до {new_value}"


# ТЕСТИРОВАНИЕ
Sword = Weapon("Меч", 10, 0.1, 1.0)

Teamur = Entity("Тимурджан", damage=15, weapon=Sword)
Diana = Entity("Диана", weapon=Sword, crit_chance=0.35, crit_damage=1.9)

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
