import os

email_user = os.environ.get('DB_USER')
email_password = os.environ.get('DB_PASS')

print(email_user)
print(email_password)

