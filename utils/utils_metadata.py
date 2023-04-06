def paginate(items: list, page: int, per_page: int) -> list:
    start_index = (page - 1) * per_page
    if start_index < 0:
        start_index = 0
    end_index = start_index + per_page
    paginated_items = items[start_index:end_index]

    return paginated_items
