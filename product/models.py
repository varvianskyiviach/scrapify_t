from dataclasses import dataclass


@dataclass
class Product:
    name: str
    description: str
    colories: dict
    fats: dict
    carbs: dict
    proteins: dict
    unsaturated_fats: dict
    sugar: dict
    salt: dict
    portion: dict

    def __str__(self) -> str:
        return self.name
