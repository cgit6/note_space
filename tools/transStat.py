import re

text = r"""
+----------------------------------+
|           StormOfSeth            |
+--------------+-------------------+
| Game Name    | StormOfSeth       |
| Game ID      | 1801              |
| Total Rounds | 1,000,000         |
| Total RTP    | 736.41 %          |
| RTP 95% CI   | [700.30%,772.52%] |
| Total Bet    | 20,000,000        |
| Total Win    | 147,281,638       |
| Base Win     | 19,098,112        |
| Free Win     | 128,183,526       |
| NoWin Rounds | 299,673           |
| Trigger      | 77,093            |
| STD          | 184.228           |
| CV           | 25.017            |
+--------------+-------------------+
"""

def to_float_num(s: str) -> float:
    s = s.strip()
    s = s.replace(",", "")
    s = re.sub(r"%", "", s).strip()
    return float(s)

def parse_table(s: str) -> dict:
    data = {}
    for m in re.finditer(r"^\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*$", s, flags=re.M):
        key = m.group(1).strip()
        val = m.group(2).strip()
        data[key] = val
    return data

d = parse_table(text)

total_rounds = to_float_num(d["Total Rounds"])
total_rtp_pct = to_float_num(d["Total RTP"])         # 例如 1020.21 (百分比數字)
total_bet = to_float_num(d["Total Bet"])
base_win = to_float_num(d["Base Win"])
free_win = to_float_num(d["Free Win"])
nowin_rounds = to_float_num(d["NoWin Rounds"])
trigger = to_float_num(d["Trigger"])
std = to_float_num(d["STD"])

# RTP 相關：Base/Free RTP 用「倍數」(win/bet)，通常轉成百分比會 * 100
fg_rtp_pct = (base_win / total_bet) * 100.0
bg_rtp_pct = (free_win / total_bet) * 100.0

hit_rate = 1.0 - (nowin_rounds / total_rounds)
trigger_rate = trigger / total_rounds

# 你指定：CV = STD / Total RTP（注意 Total RTP 這裡是百分比數字，如 1020.21）
cv_calc = std / total_rtp_pct

print(f"Total RTP     : {total_rtp_pct:.2f} %")
print(f"BG RTP        : {fg_rtp_pct:.6f} %")
print(f"FG RTP        : {bg_rtp_pct:.6f} %")
print(f"Hit Rate      : {hit_rate:.8f}")
print(f"Trigger Rate  : {trigger_rate:.8f}")
print(f"CV (STD/RTP)  : {cv_calc:.6f}")
