from werkzeug.security import generate_password_hash, check_password_hash

# Исходный пароль
password = "admin123"

# Хешируем пароль


# Выводим хешированный пароль
print(generate_password_hash(password))