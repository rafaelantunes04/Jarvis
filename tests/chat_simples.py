import requests

username = input("Username: ")
password = input("Password: ")

while True:
    message = input("\nTu: ")
    if message.lower() in ("sair", "exit", "quit"):
        break

    r = requests.post(
        "http://localhost:8000/chat",
        json={"username": username, "password": password, "message": message},
    )

    if r.status_code == 401:
        print("Credenciais inválidas.")
        break

    print(f"Jarvis: {r.json()['message']}")