import requests

SHEETY_USERS_ENDPOINT = "https://api.sheety.co/<YOUR 32-CHARACTER ACCOUNT CODE>/flightDeals/users"

first_name = input("""Welcome to the Flight Club.
We find and email you the best flight deals. 
What is your first name?\n""")

last_name = input("What is your last name?\n")

email = input("What is your email?\n")

email_unconfirmed = True
while email_unconfirmed:
    email_confirmation = input("Type your email again.\n")

    if email == email_confirmation:
        print("Success! Your email has been added to our list.")
        email_unconfirmed = False

    else:
        print('Emails do not match.')

data = {
    'user': {
        'firstName': first_name,
        'lastName': last_name,
        'email': email
    }
}

response = requests.post(url=SHEETY_USERS_ENDPOINT, json=data)
print(response.status_code)
