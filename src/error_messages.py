def missing_page_message_from_value_error(err: ValueError) -> str | None:
    """Extract user-friendly message when ValueError like 'stat page not found.' occurs."""
    msg = str(err).strip().lower()
    suffix = " page not found."
    if msg.endswith(suffix):
        page = msg[: -len(suffix)].strip()
        pretty_map = {
            "stat": "Stats",
            "battle overview": "Battle Overview",
        }
        page_label = pretty_map.get(page, page.title())
        return (
            f'The "{page_label}" page was not found in the uploaded files. '
            f"Please ensure the images include that page."
        )
    return None

