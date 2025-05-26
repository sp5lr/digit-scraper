import requests
import random
import time
from colorama import init, Fore

init(autoreset=True)

ASCII_ART = """
████████▄   ▄█     ▄██████▄   ▄█      ███        ▄████████  ▄████████    ▄████████    ▄████████    ▄███████▄    ▄████████    ▄████████ 
███   ▀███ ███    ███    ███ ███  ▀█████████▄   ███    ███ ███    ███   ███    ███   ███    ███   ███    ███   ███    ███   ███    ███ 
███    ███ ███▌   ███    █▀  ███▌     ▀███▀▀██   ███    █▀  ███    █▀    ███    ███   ███    ███   ███    ███   ███    █▀    ███    ███ 
███    ███ ███▌  ▄███        ███▌     ███   ▀   ███        ███         ▄███▄▄▄▄██▀   ███    ███   ███    ███  ▄███▄▄▄      ▄███▄▄▄▄██▀ 
███    ███ ███▌ ▀▀███ ████▄  ███▌     ███     ▀███████████ ███        ▀▀███▀▀▀▀▀   ▀███████████ ▀█████████▀  ▀▀███▀▀▀     ▀▀███▀▀▀▀▀   
███    ███ ███    ███    ███ ███      ███              ███ ███    █▄  ▀███████████   ███    ███   ███          ███    █▄  ▀███████████ 
███   ▄███ ███    ███    ███ ███      ███        ▄█    ███ ███    ███   ███    ███   ███    ███   ███          ███    ███   ███    ███ 
████████▀  █▀     ████████▀  █▀      ▄████▀    ▄████████▀  ████████▀    ███    ███   ███    █▀   ▄████▀        ██████████   ███    ███ 
                                                                        ███    ███                                          ███    ███ 
made with love by wicked and the moral support of aerdisk <3
"""

def read_webhook_url(file_path="webhook.txt"):
    try:
        with open(file_path, "r") as f:
            webhook_url = f.readline().strip()
            if not webhook_url:
                raise ValueError("Webhook URL file is empty")
            return webhook_url
    except FileNotFoundError:
        print(Fore.RED + f"Webhook file '{file_path}' not found. Please create it with a valid Discord webhook URL on the first line.")
        exit(1)
    except Exception as e:
        print(Fore.RED + f"Error reading webhook file: {e}")
        exit(1)

WEBHOOK_URL = read_webhook_url()

def send_webhook_message(message):
    try:
        data = {"content": message}
        response = requests.post(WHOOK_URL, json=data)
        if response.status_code == 204:
            print(Fore.GREEN + "Message sent successfully!")
        else:
            print(Fore.RED + f"Failed to send message. Status code: {response.status_code}")
    except requests.RequestException as e:
        print(Fore.RED + f"Error sending webhook: {e}")

def search_inventory(user_id, search_term):
    try:
        url = f"https://inventory.roblox.com/v1/users/{user_id}/assets/collectibles?limit=100"
        response = requests.get(url, timeout=10)
        if response.status_code == 404:
            print(Fore.RED + f"Inventory for user {user_id} returned 404 Not Found.")
            return None
        if response.status_code == 429:
            print(Fore.RED + "Rate limit exceeded. Waiting before retrying...")
            time.sleep(20)  # Wait for rate limit reset
            return None
        if response.status_code != 200:
            print(Fore.RED + f"Failed to get inventory for user {user_id}, status code: {response.status_code}")
            return None
        items = response.json().get("data", [])
        matches = [item for item in items if search_term.lower() in item["name"].lower()]
        return matches
    except requests.RequestException as e:
        print(Fore.RED + f"Error fetching inventory for user {user_id}: {e}")
        return None

def search_avatar(user_id, search_term):
    try:
        url = f"https://avatar.roblox.com/v1/users/{user_id}/currently-wearing"
        response = requests.get(url, timeout=10)
        if response.status_code == 404:
            print(Fore.RED + f"Avatar for user {user_id} returned 404 Not Found.")
            return []
        if response.status_code == 429:
            print(Fore.RED + "Rate limit exceeded. Waiting before retrying...")
            time.sleep(20)
            return []
        if response.status_code != 200:
            print(Fore.RED + f"Failed to get avatar for user {user_id}, status code: {response.status_code}")
            return []
        asset_ids = response.json().get("assetIds", [])
        matches = []
        for asset_id in asset_ids:
            info = get_asset_info(asset_id)
            if info and "data" in info and len(info["data"]) > 0:
                item_name = info["data"][0].get("name", "")
                if search_term.lower() in item_name.lower():
                    matches.append({"name": item_name, "assetId": asset_id})
        return matches
    except requests.RequestException as e:
        print(Fore.RED + f"Error fetching avatar for user {user_id}: {e}")
        return []

def get_asset_info(asset_id):
    try:
        url = f"https://catalog.roblox.com/v1/catalog/items/details?itemIds={asset_id}"
        response = requests.get(url, timeout=10)
        if response.status_code == 404:
            print(Fore.RED + f"Asset info for asset {asset_id} returned 404 Not Found.")
            return None
        if response.status_code == 429:
            print(Fore.RED + "Rate limit exceeded. Waiting before retrying...(30 seconds)")
            time.sleep(30)
            return None
        if response.status_code != 200:
            print(Fore.RED + f"Failed to get asset info for asset {asset_id}, status code: {response.status_code}")
            return None
        return response.json()
    except requests.RequestException as e:
        print(Fore.RED + f"Error fetching asset info for asset {asset_id}: {e}")
        return None

def random_6_digits():  # 2008 account
    return f"{random.randint(0, 999999):06d}"

def random_7_digits():  # 2009 account
    return f"{random.randint(0, 9999999):07d}"

def random_8_digits():  # 2012 account
    return f"{random.randint(0, 99999999):08d}"

def random_9_digits():  # 2017 account
    return f"{random.randint(0, 999999999):09d}"

def get_user_id_func():
    user_id_func = {
        '1': random_6_digits,
        '2': random_7_digits,
        '3': random_8_digits,
        '4': random_9_digits
    }
    while True:
        try:
            account_age_search = input("""
How old do you want the accounts to be?
1) 2008
2) 2009
3) 2012
4) 2017
Enter 1, 2, 3, or 4: """)
            if account_age_search in ['1', '2', '3', '4']:
                return user_id_func[account_age_search]
            print(Fore.RED + "Invalid choice. Please enter 1, 2, 3, or 4.")
        except KeyboardInterrupt:
            print(Fore.RED + "\nSearch interrupted by user.")
            exit(1)

def get_usernames_from_ids(user_ids):
    url = "https://users.roblox.com/v1/users"
    headers = {
        "Content-Type": "application/json"
    }

    payload = {
        "userIds": user_ids
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code != 200:
            print(Fore.RED + f"Failed to fetch usernames: {response.status_code}")
            return {}
        data = response.json()
        return {user['id']: user['name'] for user in data['data']}
    except requests.RequestException as e:
        print(Fore.RED + f"Error fetching usernames: {e}")
        return {}

def normal_search(search_term, user_id_func, fetch_usernames):
    print(Fore.RED + ASCII_ART)
    for _ in range(10_000):
        user_id = user_id_func()  # Call the selected function to get a user ID
        print(Fore.YELLOW + f"\nChecking user ID: {user_id}...")

        results = search_inventory(user_id, search_term)
        if results is None:
            print(Fore.RED + "Inventory private or inaccessible, checking avatar instead...💅")
            results = search_avatar(user_id, search_term)

        if results:
            print(Fore.GREEN + f"Found the following items matching '{search_term}':")
            for item in results:
                print(Fore.GREEN + f"- {item['name']} (ID: {item['assetId']})")
            with open("found_users.txt", "a") as f:
                f.write(f"{user_id}\n")
            print(Fore.GREEN + f"User ID {user_id} saved to found_users.txt.")
            
            if fetch_usernames:
                # Fetch username and save possible passwords
                usernames = get_usernames_from_ids([int(user_id)])
                if usernames:
                    username = usernames.get(int(user_id), "Unknown")
                    print(Fore.GREEN + f"Username for User ID {user_id}: {username}")
                    with open("possible_passwords.txt", "a") as f:
                        modified0 = username
                        modified = f"{username}123"
                        modified1 = f"{username}1234"
                        modified2 = f"123{username}"
                        modified3 = f"1234{username}"
                        f.write(f"Possible Passwords For {username}:\n")
                        f.write(f"{modified0}\n")
                        f.write(f"{modified}\n")
                        f.write(f"{modified1}\n")
                        f.write(f"{modified2}\n")
                        f.write(f"{modified3}\n")
                    print(Fore.GREEN + f"Possible passwords for {username} saved to possible_passwords.txt")
                else:
                    print(Fore.RED + f"Could not fetch username for User ID {user_id}")
            break
        else:
            print(Fore.YELLOW + f"No items with '{search_term}' found in inventory or avatar for user {user_id}.")
        time.sleep(0.5)

def afk_mode(search_term, user_id_func, fetch_usernames):
    print(Fore.RED + ASCII_ART)
    last_webhook = time.time()
    while True:
        user_id = user_id_func()  # Call the selected function to get a user ID
        print(Fore.YELLOW + f"\nChecking user ID: {user_id}...")

        results = search_inventory(user_id, search_term)
        if results is None:
            print(Fore.RED + "Inventory private or inaccessible, checking avatar instead...💅")
            results = search_avatar(user_id, search_term)

        if results:
            print(Fore.GREEN + f"Found the following items matching '{search_term}':")
            for item in results:
                print(Fore.GREEN + f"- {item['name']} (ID: {item['assetId']})")
            with open("found_users.txt", "a") as f:
                f.write(f"{user_id}\n")
            print(Fore.GREEN + f"User ID {user_id} saved to found_users.txt.")
            send_webhook_message(f"Found user ID {user_id} with items matching '{search_term}': {[item['name'] for item in results]}")
            
            if fetch_usernames:
                # Fetch username and save possible passwords
                usernames = get_usernames_from_ids([int(user_id)])
                if usernames:
                    username = usernames.get(int(user_id), "Unknown")
                    print(Fore.GREEN + f"Username for User ID {user_id}: {username}")
                    with open("possible_passwords.txt", "a") as f:
                        modified0 = username
                        modified = f"{username}123"
                        modified1 = f"{username}1234"
                        modified2 = f"123{username}"
                        modified3 = f"1234{username}"
                        f.write(f"Possible Passwords For {username}:\n")
                        f.write(f"{modified0}\n")
                        f.write(f"{modified}\n")
                        f.write(f"{modified1}\n")
                        f.write(f"{modified2}\n")
                        f.write(f"{modified3}\n")
                    print(Fore.GREEN + f"Possible passwords for {username} saved to possible_passwords.txt")
                else:
                    print(Fore.RED + f"Could not fetch username for User ID {user_id}")

        else:
            print(Fore.YELLOW + f"No items with '{search_term}' found in inventory or avatar for user {user_id}.")

        if time.time() - last_webhook >= 300:
            send_webhook_message(f"AFK mode active: checked user ID {user_id} for '{search_term}' and continuing...")
            last_webhook = time.time()

        time.sleep(0.5)

def run():
    print(Fore.RED + ASCII_ART)
    search_term = input("Enter the name of the item you're searching for: ")
    user_id_func = get_user_id_func()  # Get the user ID function based on account age
    while True:
        fetch_choice = input("Fetch usernames and generate possible passwords?\n1. Yes\n2. No\nEnter 1 or 2: ")
        if fetch_choice in ['1', '2']:
            fetch_usernames = fetch_choice == '1'
            break
        print(Fore.RED + "Invalid choice. Please enter 1 or 2.")
    while True:
        mode = input("Choose mode:\n1. Normal search🔍 (stop when found)\n2. AFK mode🌙 (keep running, send webhook)\nEnter 1 or 2: ")
        if mode in ['1', '2']:
            break
        print(Fore.RED + "Invalid choice. Please enter 1 or 2.")

    if mode == '1':
        normal_search(search_term, user_id_func, fetch_usernames)
    else:
        afk_mode(search_term, user_id_func, fetch_usernames)

if __name__ == "__main__":
    run()
