from collections import UserDict
from datetime import datetime, timedelta


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
        pass

class Phone(Field):
    def __init__(self, value):
        if not self.number_validation(value):
            raise ValueError(f"Invalid phone number: {value}")
        super().__init__(value)

    def number_validation(self, value):
        return len(value) == 10 and value.isdigit()



class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

    def __str__(self):
        return self.value.strftime("%d.%m.%Y")


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        phone_obj = Phone(phone)
        self.phones.append(phone_obj)


    def remove_phone(self, phone_to_delete):
        for phone in self.phones:
            if phone.value == phone_to_delete:
                self.phones.remove(phone)
                return
            raise ValueError(f"Phone {phone_to_delete} not found.")

    def edit_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if phone.value == old_phone:
                self.add_phone(new_phone)
                self.phones.remove(phone)
                return
            else:
                raise ValueError (f"Invalid phone number: {old_phone}")


    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def add_birthday(self, birthday):
        if self.birthday is not None:
            raise ValueError("This record already has a birthday.")
        self.birthday = Birthday(birthday)

    def __str__(self):
        birthday_str = f", birthday: {self.birthday}" if self.birthday else ""
        phones_str = ', '.join(p.value for p in self.phones)
        return f"Contact name: {self.name.value}, phones: {phones_str}{birthday_str}"



class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name, None)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def __str__(self):
        if not self.data:
            return "AddressBook is empty."
        return "\n".join(f"{record}" for record in self.data.values())

    def adjust_for_weekend(self, birthday):
        if birthday.weekday() == 5:
            return birthday + timedelta(days=2)
        elif birthday.weekday() == 6:
            return birthday + timedelta(days=1)
        return birthday

    def date_to_string(self, date):
        return date.strftime("%d.%m.%Y")

    def get_upcoming_birthdays(self, days=7):
        today = datetime.today()
        upcoming_birthdays = []

        for record in self.data.values():
            if record.birthday is None:
                continue

            birthday_this_year = record.birthday.value.replace(year=today.year)
            if birthday_this_year < today:
                birthday_this_year = birthday_this_year.replace(year=today.year + 1)

            if 0 <= (birthday_this_year - today).days <= days:
                birthday_this_year = self.adjust_for_weekend(birthday_this_year)
                upcoming_birthdays.append({
                    "name": record.name.value,
                    "birthday": self.date_to_string(birthday_this_year)
                })

        return upcoming_birthdays