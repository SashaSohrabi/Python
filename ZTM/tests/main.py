def do_stuff(num: int | str = 0) -> object:
    try:
        return int(num) + 5
    except (TypeError, ValueError) as error:
        return error
