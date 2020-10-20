import os 

db_user = os.environ.get('EMAIL_USER')
db_pass = os.environ.get('EMAIL_PASS')

print(db_user)
print(db_pass)

# this is only a test file to test how the environmental variables work. 
# so i can store some private information in my computer without showing it when i push my code