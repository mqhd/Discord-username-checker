import argparse
import json
import requests
import string
import random
from colorama import Fore, Style

BASE_URL = "https://discord.com/api/v9"
ENDPOINT = "unique-username/username-attempt-unauthed"

def generate_username(length):
    """Generate a random username of the specified length."""
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def get_proxy():
    """Read proxies from the proxy.txt file."""
    proxies = []
    with open("proxy.txt", "r") as file:
        for line in file:
            proxies.append(line.strip())
    return proxies

def brute_force(username_length, use_proxy, result_file):
    """Brute force usernames and check their availability."""
    url = f"{BASE_URL}/{ENDPOINT}"
    proxies = get_proxy() if use_proxy else [None]
    while True:
        username = generate_username(username_length)
        data = {"username": username}
        for proxy in proxies:
            proxies_dict = {"http": proxy, "https": proxy} if proxy else None
            try:
                response = requests.post(url, json=data, proxies=proxies_dict, timeout=10)
                if response.status_code == 200:
                    result = response.json()
                    if "taken" in result and result["taken"]:
                        print(f"{Fore.RED}Username '{username}' is taken.{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.GREEN}Username '{username}' is available.{Style.RESET_ALL}")
                        with open(result_file, "a") as file:
                            file.write(f"Username '{username}' is available.\n")
                        return
            except requests.exceptions.RequestException as e:
                print(f"{Fore.YELLOW}Failed to check username '{username}' with proxy '{proxy}': {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Brute force usernames on a specific URL.")
    parser.add_argument("-l", "--username_length", type=int, default=6, help="Length of the usernames to generate")
    parser.add_argument("-r", "--result_file", default="result.txt", help="File to store the results")
    parser.add_argument("-p", "--proxy", action="store_true", help="Use proxies from proxy.txt")
    args = parser.parse_args()

    # Start brute force attack
    brute_force(args.username_length, args.proxy, args.result_file)

    # Copyright notice
    print("\nCopyright (c) 2024 Mohammad Fahad Altamimi. All rights reserved.")
