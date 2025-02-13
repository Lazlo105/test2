import bcrypt

# Исходный пароль
password = "admin123"

# Хешируем пароль
hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

# Выводим хешированный пароль
print(hashed_password.decode())