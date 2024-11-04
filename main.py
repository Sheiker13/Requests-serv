import requests
from datetime import datetime


class User:
    def __init__(self, user_id, name, birth_date, state):
        self.user_id = user_id
        self.name = name
        self.birth_date = birth_date
        self.state = float(state) if state is not None else 0

    def get_age(self):
        """Возвращает возраст пользователя."""
        if self.birth_date:
            try:
                birth_date = datetime.strptime(self.birth_date, "%Y-%m-%d")
            except ValueError:
                try:
                    birth_date = datetime.strptime(self.birth_date, "%Y-%m-%dT%H:%M:%S.%fZ")
                except ValueError:
                    return None
            return (datetime.now() - birth_date).days // 365
        return None


class UserManager:
    API_URL = "https://66095c000f324a9a28832d7e.mockapi.io/users"

    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        """Загружает пользователей из API."""
        response = requests.get(self.API_URL)
        if response.status_code == 200:
            return [User(user['id'], user['name'], user.get('birth'), user.get('state')) for user in response.json()]
        return []

    def find_user_id(self, name):
        """Находит ID пользователя по имени."""
        for user in self.users:
            if user.name == name:
                return user.user_id
        return None

    def calculate_total_state(self):
        """Считает общее состояние всех пользователей."""
        return sum(user.state for user in self.users)

    def create_user(self, name, state):
        """Создает нового пользователя."""
        user_data = {
            "name": name,
            "state": state
        }
        response = requests.post(self.API_URL, json=user_data)
        if response.status_code == 201:
            created_user = response.json()
            return User(created_user['id'], created_user['name'], created_user.get('birth'), created_user.get('state'))
        return response.text

    def find_oldest_user(self):
        """Находит самого старого пользователя."""
        users_with_age = [user for user in self.users if user.get_age() is not None]
        return min(users_with_age, key=lambda u: u.get_age(), default=None) if users_with_age else None

    def find_poorest_user(self):
        """Находит самого бедного пользователя."""
        return min(self.users, key=lambda user: user.state)

    def count_april_birthdays(self):
        """Считает пользователей, родившихся в апреле."""
        count = 0
        for user in self.users:
            if user.birth_date:
                try:
                    # Попробуем разобрать дату в двух форматах
                    birth_date = datetime.strptime(user.birth_date, "%Y-%m-%d")
                except ValueError:
                    try:
                        birth_date = datetime.strptime(user.birth_date, "%Y-%m-%dT%H:%M:%S.%fZ")
                    except ValueError:
                        continue  # Пропускаем, если ни один формат не подошел
                if birth_date.month == 4:
                    count += 1
        return count


if __name__ == "__main__":
    user_manager = UserManager()

    # Найти Wilson VonRueden
    wilson_id = user_manager.find_user_id("Wilson VonRueden")
    if wilson_id:
        print(f"ID пользователя Wilson VonRueden: {wilson_id}")
    else:
        print("Пользователь Wilson VonRueden не найден.")

    # Состояние пользователей
    total_state = user_manager.calculate_total_state()
    print(f"Общее состояние первых 76 пользователей: {total_state}")

    # Создание своего пользователя
    created_user = user_manager.create_user("Max", "1000000")
    if isinstance(created_user, User):
        print(f"Создан пользователь: {created_user.name}, ID: {created_user.user_id}")
    else:
        print("Не удалось создать пользователя:", created_user)

    # Самый старый пользователь
    oldest_user = user_manager.find_oldest_user()
    if oldest_user:
        print(f"Самый старый пользователь: {oldest_user.name}")
    else:
        print("Не удалось найти пользователей с датой рождения.")

    # Самый бедный пользователь
    poorest_user = user_manager.find_poorest_user()
    print(f"Самый бедный пользователь: {poorest_user.name}")

    # Количество пользователей, родившихся в апреле
    april_birthdays_count = user_manager.count_april_birthdays()
    print(f"Количество пользователей, родившихся в апреле: {april_birthdays_count}")
