import re

string = "search inside of this text! search again!"
exclamation = "!"

pattern = re.compile(r"([a-zA-z]).([a])")

a = pattern.search(string)
b = pattern.findall(string)
c = pattern.fullmatch(exclamation)
d = pattern.match(exclamation)


# print(f"{a}\n")
# print(f"{b}\n")
# print(f"{c}\n")
# print(f"{d}\n")

email_regex = (
    r"(?=.{1,254}\Z)"
    r"(?=[^@]{1,64}@)"
    r"[A-Za-z0-9!#$%&'*+/=?^_`{|}~-]+"
    r"(?:\.[A-Za-z0-9!#$%&'*+/=?^_`{|}~-]+)*"
    r"@"
    r"(?:[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?\.)+"
    r"[A-Za-z]{2,63}"
)

email_validate_pattern = re.compile(email_regex)


def is_valid_email(email: str) -> bool:
    return email_validate_pattern.fullmatch(email) is not None


while True:
    email: str = input("Write an email address to verify: ")
    if is_valid_email(email):
        print(f"Your entered email: {email} is valid")
        break
    else:
        print(f"Your entered email: {email} is not valid")
