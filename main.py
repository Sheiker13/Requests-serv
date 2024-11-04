import requests
from datetime import datetime

API_URL = "https://66095c000f324a9a28832d7e.mockapi.io/users"


def get_users():
    response = requests.get(API_URL)
    if response.status_code == 200:
        return response.json()
    return []


def parse_birthdate(birthdate_str):
    try:
        return datetime.strptime(birthdate_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    except ValueError:
        return None


def find_user_id(name, users):
    for user in users:
        if user.get("name") == name:
            return user.get("id")
    return None


def calculate_total_state(users):
    total_state = 0
    for user in users:
        state = user.get("state", 0)
        if isinstance(state, (int, float)) or (isinstance(state, str) and state.isdigit()):
            total_state += float(state)
    return total_state


def create_user(name, state):
    user_data = {
        "name": name,
        "state": state
    }
    response = requests.post(API_URL, json=user_data)
    if response.status_code == 201:
        return response.json()
    return response.text


def find_oldest_user(users):
    users_with_birthdate = []
    for user in users:
        if "birth" in user and user["birth"]:
            birth_date = parse_birthdate(user["birth"])
            if birth_date:
                users_with_birthdate.append((user, birth_date))

    if users_with_birthdate:
        return min(users_with_birthdate, key=lambda x: x[1])[0]
    return None


def find_poorest_user(users):
    return min(users, key=lambda user: float(user.get("state", 0)))


def count_april_birthdays(users):
    count = 0
    for user in users:
        if "birth" in user:
            birth_date = parse_birthdate(user["birth"])
            if birth_date and birth_date.month == 4:
                count += 1
    return count


if __name__ == "__main__":
    users = get_users()

# Найти Wilson Von Rueden
    wilson_id = find_user_id("Wilson VonRueden", users)
    if wilson_id:
        print(f"ID пользователя Wilson VonRueden: {wilson_id}")
    else:
        print("Пользователь Wilson VonRueden не найден.")

# Состояние 76 пользователей
    total_state = calculate_total_state(users)
    print(f"Общее состояние первых 76 пользователей: {total_state}")

# Свой пользователь
    created_user_info = create_user("Max", "1000000")
    if isinstance(created_user_info, dict):
        print(f"Создан пользователь: {created_user_info}")
    else:
        print("Не удалось создать пользователя:", created_user_info)

# Самый старый
    oldest_user = find_oldest_user(users)
    if oldest_user:
        print(f"Самый старый пользователь: {oldest_user['name']}")
    else:
        print("Не удалось найти пользователей с датой рождения.")

# Самый беный
    poorest_user = find_poorest_user(users)
    print(f"Самый бедный пользователь: {poorest_user['name']}")

# Количество в апр
    april_birthdays_count = count_april_birthdays(users)
    print(f"Количество пользователей, родившихся в апреле: {april_birthdays_count}")
