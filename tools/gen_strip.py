import random
from typing import Dict, List

# =========================
# 可調參數
# =========================
SEED = None  # 想要每次都不同就改成 None
REEL_LENGTHS = [100, 100, 100, 100, 100, 100]  # 每軸長度(需 >=100)

# 每軸的「頻率權重」(不是百分比)：數字越大，越常出現
# 沒寫到的符號會用 DEFAULT_WEIGHTS 補上
DEFAULT_WEIGHTS = {i: 1 for i in range(1, 12)}  # 1~11 預設都 1

REEL_WEIGHTS = [
    # Reel[0]
    {1: 15, 2: 0, 3: 1, 4: 2, 5: 2, 6: 3, 7: 3, 8: 5, 9: 15, 10: 14, 11: 14},
    # Reel[1]
    {1: 15, 2: 0, 3: 1, 4: 2, 5: 2, 6: 3, 7: 3, 8: 5, 9: 15, 10: 14, 11: 14},
    # Reel[2]
    {1: 15, 2: 0, 3: 1, 4: 2, 5: 2, 6: 3, 7: 3, 8: 5, 9: 15, 10: 14, 11: 14},
    # Reel[3]
    {1: 15, 2: 0, 3: 1, 4: 2, 5: 2, 6: 3, 7: 3, 8: 6, 9: 16, 10: 15, 11: 15},
    # Reel[4]
    {1: 15, 2: 0, 3: 1, 4: 2, 5: 2, 6: 3, 7: 3, 8: 6, 9: 16, 10: 15, 11: 15},
    # Reel[5]
    {1: 15, 2: 0, 3: 1, 4: 2, 5: 2, 6: 3, 7: 3, 8: 6, 9: 16, 10: 16, 11: 16},
]

# =========================
# 核心邏輯
# =========================
def build_weight_map(overrides: Dict[int, int]) -> Dict[int, int]:
    w = dict(DEFAULT_WEIGHTS)
    for k, v in overrides.items():
        if not (1 <= k <= 11):
            raise ValueError(f"symbol must be 1..11, got {k}")
        if v < 0:
            raise ValueError(f"weight must be >= 0, got {v} for symbol {k}")
        w[k] = v
    # 至少要有一個正權重
    if sum(w.values()) <= 0:
        raise ValueError("all weights are 0; cannot generate reel")
    return w

def gen_reel(length: int, weights: Dict[int, int], rng: random.Random) -> List[int]:
    if length < 100:
        raise ValueError(f"reel length must be >= 100, got {length}")
    symbols = list(range(1, 12))
    w = [weights[s] for s in symbols]
    return rng.choices(symbols, weights=w, k=length)

def fmt_yaml(reel_idx: int, symbols: List[int]) -> str:
    sym_str = ",".join(map(str, symbols))
    weights_str = ", ".join(["1"] * len(symbols))
    return (
        f"                - # Reel[{reel_idx}]\n"
        f"                  symbols : [{sym_str}]\n"
        f"                  weights : [{weights_str}]"
    )

def main():
    rng = random.Random(SEED) if SEED is not None else random.Random()
    for i in range(6):
        wmap = build_weight_map(REEL_WEIGHTS[i] if i < len(REEL_WEIGHTS) else {})
        reel = gen_reel(REEL_LENGTHS[i], wmap, rng)
        print(fmt_yaml(i, reel))

if __name__ == "__main__":
    main()
