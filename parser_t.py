import requests
from bs4 import BeautifulSoup, element

from typing import List, NamedTuple, Dict

from model import Teacher, Classroom

class PersonUrl(NamedTuple):
    surname: str
    name: str
    patronymic: str
    
    url: str

    url_image: str

class MetaSingleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Persons(metaclass=MetaSingleton):

    teacher: Dict[str, Teacher | None] = {}

    perPage = 100
    position = 0
    facultyWithChairs = 389
    subunit = 0
    fullname = ''

    full_url = 'https://pro.guap.ru/professors?position={position}&facultyWithChairs={facultyWithChairs}&subunit={subunit}&fullname={fullname}&perPage={perPage}'

    people: List[PersonUrl] | None = None 

    def __init__(self, ):
        self.init()

    def init(self):
        self.get_list_of_persons()

    def get_full_url(self) -> str:
        return self.full_url.format(
            position=Persons.position, facultyWithChairs=Persons.facultyWithChairs, 
            subunit=Persons.subunit, fullname=Persons.fullname, perPage=Persons.perPage
        )

    def get_list_of_persons(self):
        if self.people is not None:
            print(self.people is not None)
            return self.people

        response = requests.get(self.get_full_url())
        soup = BeautifulSoup(response.text, 'lxml')
        
        date: element.ResultSet[element.Tag] = soup.find_all('div', class_='card shadow-sm my-sm-2')

        self.people = []

        for card in date:
            handler = card.find('h5', class_='mb-sm-1 fw-semibold')
            url_img = 'https://pro.guap.ru' + card.find('img', class_='profile_image').get('src')

            fullname = handler.text.replace('\n', ' ').split()
            src = 'https://pro.guap.ru' + handler.find('a').get('href')

            self.people.append(PersonUrl(*fullname, url=src, url_image=url_img))

    def get_teachers(self, text: str, classroom: Classroom) -> Teacher:
        
        teacher = self.teacher.get(text, None)
        
        if teacher is not None:
            print('skip')
            return teacher

        bloks = text.split()
        surname = bloks[0]
        name, patronymic, *_ =  bloks[1].split('.')

        for pep in self.people:
            if surname.lower() == pep.surname.lower() and \
                name.lower() == pep.name[0].lower() and \
                patronymic.lower() == pep.patronymic[0].lower():
                
                response = requests.get(pep.url)
                soup = BeautifulSoup(response.text, 'lxml')
                
                date: element.ResultSet[element.Tag] = soup.find('div', class_='tab-pane fade', id='subjects')
                cart_text: element.ResultSet[element.Tag] = date.find_all('div', class_='list-group-item')
                
                disciplines = [' '.join(tag.text.replace('\n', ' ').split()) for tag in cart_text]

                tch = Teacher(
                    name=pep.name,
                    surname=pep.surname,
                    patronymic=pep.patronymic,
                    disciplines=disciplines,
                    classroom=classroom,
                    url=pep.url,
                    url_image=pep.url_image
                )

                self.teacher[text] = tch 
                
                return tch
        
        self.teacher[text] = None
        return None
                





