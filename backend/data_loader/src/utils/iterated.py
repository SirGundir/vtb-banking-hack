from typing import Callable, Any

from utils.datetime import try_parse_date


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def find(iterable, predicate):
    return next((x for x in iterable if predicate(x)), None)


def recursive_find(
    value: dict,
    target_key: Any,
    find_in_lists: bool = False
) -> Any | None:
    if target_key in value:
        return value[target_key]

    for key, value in value.items():
        if isinstance(value, dict):
            result = recursive_find(value, target_key, find_in_lists)
            if result is not None:
                return result
        elif find_in_lists and isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    result = recursive_find(item, target_key, find_in_lists)
                    if result is not None:
                        return result
    return None


def remove_by_condition(list_, condition: Callable):
    found = next((x for x in list_ if condition(x)), None)
    if found is not None:
        list_.remove(found)
    return found, list_


def split_by_condition(list_, condition: Callable):
    matched, not_matched = [], []
    for element in list_:
        (matched if condition(element) else not_matched).append(element)
    return matched, not_matched


def dicts_equal_ignore_order(first, second):
    if isinstance(first, dict) and isinstance(second, dict):
        if first.keys() != second.keys():
            return False
        return all(dicts_equal_ignore_order(first[k], second[k]) for k in first)

    elif isinstance(first, list) and isinstance(second, list):
        if len(first) != len(second):
            return False
        used = [False] * len(second)
        for item_a in first:
            found = False
            for i, item_b in enumerate(second):
                if not used[i] and dicts_equal_ignore_order(item_a, item_b):
                    used[i] = True
                    found = True
                    break
            if not found:
                return False
        return True

    elif isinstance(first, (set, tuple)) and isinstance(second, (set, tuple)):
        return sorted(first) == sorted(second)

    # Попытка распарсить строки как даты и сравнить
    if isinstance(first, str) and isinstance(second, str):
        dt1 = try_parse_date(first)
        dt2 = try_parse_date(second)
        if dt1 and dt2:
            return dt1 == dt2

    # Обычное сравнение
    return first == second

