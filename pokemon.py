from dataclasses import dataclass

@dataclass
class Stats:
    hp: int
    attack: int
    defense: int 
    special_attack: int
    special_defense: int
    speed: int

    def __str__(self) -> str:
        return (
            f"\t- HP: {self.hp}\n"
            f"\t- Attack: {self.attack}\n"
            f"\t- Defense: {self.defense}\n"
            f"\t- Special Attack: {self.special_attack}\n"
            f"\t- Special Defense: {self.special_defense}\n"
            f"\t- Speed: {self.speed}\n"
        )


@dataclass
class Types:
    type1: str
    type2: str

    def __str__(self) -> str:
        return (
            f"\t- {self.type1}\n"
            f"\t- {self.type2}\n"
        )


@dataclass
class Pokemon:
    name: str
    height: int
    weight: int
    stats: Stats
    types: Types

    def __str__(self) -> str:
        return (
            f"Name: {self.name}\n"
            f"Height: {self.height}\n"
            f"Weight: {self.weight}\n"
            f"Stats:\n{self.stats}"
            f"Types:\n{self.types}"
        )




