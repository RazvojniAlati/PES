import requests

API_URL = "https://jsonplaceholder.typicode.com/users"

def fetch_data():
    print(f"Preuzimam podatke sa adrese: {API_URL}...\n")
    
    try:
       
        response = requests.get(API_URL, timeout=5)
        
        if response.status_code == 200:
            
            users = response.json()
            
            print(f"Uspešno preuzeto! Ukupno korisnika: {len(users)}\n")
            print("-" * 50)
            
            for user in users:
                name = user.get("name")
                username = user.get("username")
                email = user.get("email")
                city = user.get("address", {}).get("city")
                
                print(f"Ime: {name} (@{username})")
                print(f"Email: {email}")
                print(f"Grad: {city}")
                print("-" * 50)
                
        else:
            print(f"Greška prilikom preuzimanja. HTTP Status kod: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"Došlo je do mrežne greške: {e}")

if __name__ == "__main__":
    fetch_data()