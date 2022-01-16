def print_operations(opertaions: list[str], header: str = None) -> int:
    if header is not None:
        print(header)
    else:
        print("Choose the operation to perform:")

    index = 1
    for opertaion in opertaions:
        print(f"{index} - {opertaion}")
        index += 1

    valid_operation = False
    while not valid_operation:
        try:
            selected_index = int(input())

            if selected_index not in range(1, len(opertaions) + 1):
                raise
        except Exception:
            print("Invalid operation number. Try again: ")
            continue

        valid_operation = True

    return selected_index - 1
