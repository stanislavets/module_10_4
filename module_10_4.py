import random
import time
from threading import Thread
from queue import Queue

class Table:
    def __init__(self, number):
        self.number = number
        self.guest = None

    def assign_guest(self, guest):
        self.guest = guest

    def free_table(self):
        self.guest = None

    def serve_guest(self):
        if self.guest is not None:
            if self.guest.is_alive():
                print(f"{self.guest.name} покушал(-а) и ушёл(ушла)")
                self.free_table()
            else:
                print(f"Стол номер {self.number} свободен")
                self.free_table()

class Guest(Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        time.sleep(random.randint(3, 10))

class Cafe:
    def __init__(self, *tables):
        self.queue = Queue()
        self.tables = tables

    def guest_arrival(self, *guests):
        for guest in guests:
            if any(table.guest is None for table in self.tables):
                index = next(i for i, table in enumerate(self.tables) if table.guest is None)
                table = self.tables[index]
                table.assign_guest(guest)
                print(f"{guest.name} сел(-а) за стол номер {table.number}")
                guest.start()
            else:
                self.queue.put(guest)
                print(f"{guest.name} в очереди")

    def discuss_guests(self):
        while not self.queue.empty() or any(table.guest is not None for table in self.tables):
            for table in self.tables:
                table.serve_guest()
            if not self.queue.empty():
                guest = self.queue.get()
                index = next(i for i, table in enumerate(self.tables) if table.guest is None)
                table = self.tables[index]
                table.assign_guest(guest)
                print(f"{guest.name} вышел(-ла) из очереди и сел(-а) за стол номер {table.number}")
                guest.start()

# Пример использования
tables = [Table(number) for number in range(1, 6)]
guests_names = [
    'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
    'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra'
]
guests = [Guest(name) for name in guests_names]
cafe = Cafe(*tables)
cafe.guest_arrival(*guests)
cafe.discuss_guests()