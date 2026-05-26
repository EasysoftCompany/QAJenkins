from dataclasses import dataclass
from faker import Faker

fake = Faker("es_MX")


@dataclass
class PersonData:
    first_name: str
    last_name: str
    full_name: str
    email: str
    age: int
    salary: int
    department: str
    current_address: str
    permanent_address: str


def generate_person() -> PersonData:
    """Genera datos de una persona aleatoria usando Faker."""
    first_name = fake.first_name()
    last_name = fake.last_name()
    return PersonData(
        first_name=first_name,
        last_name=last_name,
        full_name=f"{first_name} {last_name}",
        email=fake.email(),
        age=fake.random_int(min=18, max=65),
        salary=fake.random_int(min=20000, max=120000),
        department=fake.random_element(
            ["QA", "Engineering", "Marketing", "Finance", "HR", "Design"]
        ),
        current_address=fake.address().replace("\n", " "),
        permanent_address=fake.address().replace("\n", " "),
    )
