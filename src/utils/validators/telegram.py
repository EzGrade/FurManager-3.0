def validate_tg_id(tg_id: str | int) -> str | int:
    """
    Validates a Telegram ID.

    Args:
        tg_id (str): The Telegram ID to validate.

    Returns:
        bool: True if the ID is valid, False otherwise.
    """
    if isinstance(tg_id, int):
        tg_id = str(tg_id)

    if not tg_id.replace("-", "").isdigit():
        return "Invalid ID: must be numeric."
    if len(tg_id) < 12 or len(tg_id) > 15:
        return "Invalid ID: must be between 12 and 15 digits long."

    return int(tg_id) if tg_id.startswith("-") else f"-{tg_id}"
