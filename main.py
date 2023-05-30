import sqlite3

# Camada de domínio
class User:
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email

class UserRepository:
    def get_user(self, user_id):
        pass

    def get_all_users(self):
        pass

    def save_user(self, user):
        pass

    def update_user(self, user):
        pass

    def delete_user(self, user_id):
        pass

# Camada de infraestrutura
class SQLiteUserRepository(UserRepository):
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT)"
        )
        self.connection.commit()

    def get_user(self, user_id):
        self.cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        result = self.cursor.fetchone()
        if result:
            id, name, email = result
            return User(id, name, email)
        return None

    def get_all_users(self):
        self.cursor.execute("SELECT * FROM users")
        results = self.cursor.fetchall()
        users = []
        for result in results:
            id, name, email = result
            users.append(User(id, name, email))
        return users

    def save_user(self, user):
        self.cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", (user.name, user.email))
        self.connection.commit()
        user.id = self.cursor.lastrowid

    def update_user(self, user):
        self.cursor.execute("UPDATE users SET name = ?, email = ? WHERE id = ?", (user.name, user.email, user.id))
        self.connection.commit()

    def delete_user(self, user_id):
        self.cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        self.connection.commit()

# Camada de aplicação
class UserService:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def get_user(self, user_id):
        return self.user_repository.get_user(user_id)

    def get_all_users(self):
        return self.user_repository.get_all_users()

    def create_user(self, name, email):
        user = User(None, name, email)
        self.user_repository.save_user(user)

    def update_user(self, user_id, name, email):
        user = self.user_repository.get_user(user_id)
        if user:
            user.name = name
            user.email = email
            self.user_repository.update_user(user)

    def delete_user(self, user_id):
        self.user_repository.delete_user(user_id)

# Exemplo de uso
db_file = "users.db"
repository = SQLiteUserRepository(db_file)
service = UserService(repository)

# Criação de usuário
service.create_user("John Doe", "john@example.com")
service.create_user("Jane Smith", "jane@example.com")

# Obtenção de usuário por ID
user = service.get_user(1)
print(user.id, user.name, user.email)

# Obtenção de todos os usuários
users = service.get_all_users()
for user in users:
    print(user.id, user.name, user.email)

# Atualização de usuário
service.update_user(1, "John Smith", "john.smith@example.com")

# Deleção de usuário
service.delete_user(2)

# Encerramento da conexão com o banco de dados
repository.connection
