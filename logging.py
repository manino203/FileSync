def log(message: str, log_path: str) -> None:
    """
        Log a message to both the console and the specified log file.
    """
    print(message)
    with open(log_path, "a") as log_file:
        log_file.write(f"{message}\n")
