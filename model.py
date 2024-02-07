from pydantic.dataclasses import dataclass

from typing import Literal, List

@dataclass
class Hender:
    name_group: str
    type_week: Literal['ЧИСЛИТЕЛЬ', 'ЗНАМЕНАТЕЛЬ']

    def __str__(self):
        return f'Группа: {self.name_group} ({self.type_week})'
    
    def __format__(self, __format_spec: str) -> str:
        return format(self.__str__(), __format_spec)

@dataclass
class Classroom:
    name: str | None
    
@dataclass
class Teacher:
    name: str
    surname: str
    patronymic: str

    disciplines: List[str]

    classroom: Classroom 

    url: str
    url_image: str

    def __str__(self):
        return f'{self.name} ({self.classroom.name})'
    
@dataclass
class Class:
    number: int
    name: str | None
    teachers: List[Teacher | None] | None
    
@dataclass
class Day:
    week_day: Literal['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']
    classes: List[Class]

@dataclass
class Schedule:
    days: List[Day]

def get_hender(text: str) -> Hender:
    bloks = text.split()

    return Hender(name_group=bloks[2], type_week=bloks[4])

@dataclass
class ScheduleGroup():
    hender: Hender
    schedule: Schedule