import re

persons = {}
command_list = "'add' - новий контакт\n"\
                "'change' - змінює контакт\n"\
                "'phone' - показує конакт за ім'ям\n"\
                "'show' - показує список конактів\n"\
                "'ok', 'bye', 'close', 'exit' - вихід з бота"
input_line = "-" * 40 + "\n"\
            "Введіть команду \n"\
    "(example: 'add name, phone_number')\n"\
    "Щоб відобразити список команд введіть 'help': "

def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            print("Контакт відсутній")
        except ValueError:
            print("Номер телефона тільки цифри")
        except IndexError:
            print("Неповний номер")
    return wrapper

@input_error
def add_contact(name, phone):
    persons[name] = int(phone)
    print(f"Контакт {name}, з номером {phone} збережено")

@input_error
def get_phone(name):
    phone = persons[name]
    print(f"Номер телефону для контакту {name}: {phone}")

@input_error
def change_phone(name, new_phone):
    persons[name] = int(new_phone)
    print(f"Номер телефону для контакту {name} змінено на {new_phone}")

def parse_command(command):
    match = re.match(r'(\w+)(?:\s+(.*))?', command)
    if not match:
        return None, None
    return match.group(1), match.group(2)

def list_persons():
    if not persons:
        print("Список контактів порожній")
    else:
        print("Список контактів:")
        for name, phone in persons.items():
            print(f"{name}: {phone}")

def key_to_change_data(key, params):
    if key == 'add':
        name, phone = params.split()
        return add_contact(name, phone)

    elif key == 'change':
        name, new_phone = params.split()
        return change_phone(name, new_phone)
    return False

def data_output_key(key, params):
    if key == 'hello':
        return print("How can I help you?")
    elif key == 'help':
        return print(command_list)
    elif key == 'show':
        return list_persons()
    elif key == 'phone':
        name = params
        return get_phone(name)
    return False

def main():
    while True:
        command = input(input_line)
        key, params = parse_command(command)
        if not key:
            print("Невірний формат")
            continue
        key = key.lower()

        try:
            data_output_key(key, params)
            key_to_change_data(key, params)
        except AttributeError:
            print("Не вказані дані контакту")
            continue

        if key in ['ok', 'bye', 'close', 'exit']:
            print("Good bye!")
            break

        if data_output_key is False or key_to_change_data is False:
            print("Невідома команда")

if __name__ == '__main__':
    main()

