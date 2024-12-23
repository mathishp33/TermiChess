def delete(ls: list, i: int):
    cpy = ls.copy()
    del(cpy[i])
    return cpy