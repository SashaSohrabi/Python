# pyright: strict
import hashlib
from getpass import getpass

import requests
from requests import Response


def request_api_data(query_char: str) -> Response:
    url = "https://api.pwnedpasswords.com/range/" + query_char
    res = requests.get(url)

    if res.status_code != 200:
        raise RuntimeError(
            f"Error fetching: {res.status_code}", "Check api and try again"
        )
    return res


def get_password_leaks_count(response: Response, hash_to_check: str) -> int:
    hashes = (line.split(":") for line in response.text.splitlines())

    for h, count in hashes:
        if h == hash_to_check:
            return int(count)
    return 0


def pwned_api_check(password: str) -> int:
    sha1password = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    first_five_char, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(first_five_char)
    return get_password_leaks_count(response, tail)


def main():
    password_to_check = getpass("Enter the password you want to check: ")
    count = pwned_api_check(password_to_check)
    if count:
        print(f"The entered password was found {count} time(s)... ")
    else:
        print("Your password is safe.")


if __name__ == "__main__":
    main()
