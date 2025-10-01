from dataclasses import dataclass, fields
from typing import Optional

@dataclass
class Stats:
    hp: int
    attack: int
    defense: int 
    special_attack: int
    special_defense: int
    speed: int

    def __str__(self) -> str:
        return "".join(f"\t{field.name.capitalize()}: {getattr(self, field.name)}\n" for field in fields(self))

@dataclass
class Types:
    type1: str
    type2: Optional[str]

    def __str__(self) -> str:
        if self.type2:
            return (
                f"\t- {self.type1}\n"
                f"\t- {self.type2}\n"
            )
        return (
            f"\t- {self.type1}\n"
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




