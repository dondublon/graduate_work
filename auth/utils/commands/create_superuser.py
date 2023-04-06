import click

from models import User


@click.command()
@click.argument("email")
def create_superuser(email: str):
    if User.find_by_email(email):
        print("User already exists. Try again with another email")
        return
    if "@" not in email:
        print("Email do not match. Please input your email")
        return
    password = input("Enter password: ")
    password_confirmation = input("Confirm password: ")
    if password != password_confirmation:
        print("Passwords do not match. Superuser wasn't created")
        return

    try:
        user = User(email=email, password=password)
        user.is_superuser = True
        user.active = True
        user.save()
        print("Superuser was successfully created")
        return
    except Exception as error:
        print(error)
        return
