def pick(d: dict, keys: list[str]):
    return dict([(i, d[i]) for i in d if i in set(keys)])
