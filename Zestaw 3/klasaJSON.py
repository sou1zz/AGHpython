import json
from dataclasses import dataclass

@dataclass
class Person:
    first_name: str
    last_name: str
    address: str
    postal_code: str
    pesel: str

    def to_json(self):
        return json.dumps(self.__dict__, indent=4)

    @classmethod
    def from_json(cls, json_data):
        data = json.loads(json_data)
        return cls(**data)

# Przykład użycia
person = Person("Jan", "Kowalski", "Warszawa", "00-001", "12345678901")
json_data = person.to_json()
print(json_data)

loaded_person = Person.from_json(json_data)
print(loaded_person)
