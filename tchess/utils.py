def position_to_index(pos: tuple[int, int]) -> int:
    return 8*pos[1]+pos[0]

def index_to_position(i: int) -> tuple[int, int]:
    return (i % 8, i // 8)