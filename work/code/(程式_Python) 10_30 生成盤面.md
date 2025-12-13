## 任務

* 產生 3×5 盤面（rows=3, cols=5），盤面元素以整數代碼（0～11）表示 None、H1-H4、L1-L5、Wild、Scatter。
* 每條 reel 由程式內的變數定義，生成時依各 reel 的起始點取連續 rows 個符號。(固定輪帶作法)
<!-- * 大量、高效生成盤面，結果依序寫入預先配置的大型陣列。 -->
<!-- * 亂數來源需同時滿足：可重現（同種子與參數 > 同結果）、安全（CSPRNG，不可預測）、效率。 -->

## 定義輪帶與符號

陣列中 0 對應符號清單的 "None"，在生成盤面的過程中應該要排除。

```python=
REELSTRIPS = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 2, 3, 4, 5, 6, 7, 8, 9, 10], # 第一輪
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 2, 3, 4, 5, 6, 7, 8, 9, 10], # 第二輪
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 2, 3, 4, 5, 6, 7, 8, 9, 10], # 第三輪
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 2, 3, 4, 5, 6, 7, 8, 9, 10], # 第四輪
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 2, 3, 4, 5, 6, 7, 8, 9, 10], # 第五輪
]

SYMBOLS = ["None", "Scatter", "Wild", "H1", "H2", "H3", "H4", "L1", "L2", "L3", "L4", "L5"] # 符號清單
```

## 盤面生成

定義一個物件裡面定義屬性值，包括列數(Rows)、行數(Cols)、盤面大小(ScreenSize)、輪帶表(ReelStrips)、輪帶長度(ReelLens)、符號清單(Symbols)、緩存生成結果(ScreenBuf)、隨機種子(rng)。方法是 gen_screen 函數用來生成盤面。

```python=

class ScreenGenerator:

    def __init__(
        self,
        rows: int = 3,                                                            # 列數預設 3
        cols: int = 5,                                                            # 行數預設 5
        reel_strips: Optional[List[List[int]]] = None,                            # Optional 做型別檢查用的必須是 2 維 list
        symbols: Optional[List[str]] = None,                                      # 同上
        seed: Optional[int] = None,                                               # 同上
    ):
        self.Rows = rows                                                          # 列數
        self.Cols = cols                                                          # 行數
        self.ScreenSize = rows * cols                                             # 盤面大小
        self.ReelStrips = np.asarray(reel_strips, dtype=np.uint8)                 # 輪帶表，轉成 np 陣列，型別用 uint8
        self.ReelLens = np.asarray([len(r) for r in reel_strips], dtype=np.int32) # 每條 reel 的長度
        self.Symbols = np.asarray(symbols,dtype=str)                              # 符號清單
        self.ScreenBuf = np.zeros(self.ScreenSize, dtype=np.uint8)                # 一次 spin 的輸出緩衝，初始 0 陣列狀態
        self.rng = np.random.Generator(np.random.PCG64(seed))                     # numpy 的亂數生成(帶種子固定結果)
        self._row_offsets = np.arange(rows, dtype=np.int64)                       # 第一列、第二列、第三列
```


## 生成盤面

在物件中 ScreenGenerator 中定義 gen_screen 函數。 用來生成盤面然後緩存在 self.ScreenBuf

```python=

    def gen_screen(self) -> np.ndarray:

        for i in range(self.Cols):
            reel = self.ReelStrips[i]                                   # 第 i 條輪帶
            L = reel.size                                               # 第 i 條輪帶的長度
            idx = self.rng.integers(L)                                  # 生成範圍內的整數隨機值
            take_idx = (idx + self._row_offsets) % L                    # 重複利用，不再配置
            start = i * self.Rows                                       # 因為是一維陣列要找存放的起始點
            self.ScreenBuf[start:start+self.Rows] = reel[take_idx]      # 存放
        return self.ScreenBuf
```

## 執行

```python=

if __name__ == "__main__":
    gen = ScreenGenerator(rows=3, cols=5, reel_strips=REELSTRIPS, symbols=SYMBOLS, seed=None) # 創建實例
    buf = gen.gen_screen()                # 一維 uint8，長度 15
    mat = gen.view_rows_cols()              # 形狀 (3, 5)
    print(buf)
    print(mat)
    print(gen.as_symbol_names())
```


## 全部程式碼

多了 view_cols_rows 跟 as_symbol_names 函數，view_cols_rows 將 1 維 1\*15 轉成 2 維 3\*5；as_symbol_names 函數將數字代號轉成文字符號

```py=
import numpy as np
from typing import List, Optional

# 輪帶表
# 如果輪帶長度不一怎搞? 後面補 0 吧
REELSTRIPS = [
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 3, 4, 5, 6, 7, 8, 9, 10,11], # 第一輪
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 3, 4, 5, 6, 7, 8, 9, 10,11], # 第二輪
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 3, 4, 5, 6, 7, 8, 9, 10,11], # 第三輪
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 3, 4, 5, 6, 7, 8, 9, 10,11], # 第四輪
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 3, 4, 5, 6, 7, 8, 9, 10,11], # 第五輪
]

SYMBOLS = ["None", "Scatter", "Wild", "H1", "H2", "H3", "H4", "L1", "L2", "L3", "L4", "L5"] # 符號清單

class ScreenGenerator:

    def __init__(
        self,
        rows: int = 3,                                                            # 列數預設 3
        cols: int = 5,                                                            # 行數預設 5
        reel_strips: Optional[List[List[int]]] = None,                            # Optional 做型別檢查用的必須是 2 維 list
        symbols: Optional[List[str]] = None,                                      # 同上
        seed: Optional[int] = None,                                               # 同上
    ):
        self.Rows = rows                                                          # 列數
        self.Cols = cols                                                          # 行數
        self.ScreenSize = rows * cols                                             # 盤面大小
        self.ReelStrips = np.asarray(reel_strips, dtype=np.uint8)                 # 輪帶表，轉成 np 陣列，型別用 uint8
        self.ReelLens = np.asarray([len(r) for r in reel_strips], dtype=np.int32) # 每條 reel 的長度
        self.Symbols = np.asarray(symbols,dtype=str)                              # 符號清單
        self.ScreenBuf = np.zeros(self.ScreenSize, dtype=np.uint8)                # 一次 spin 的輸出緩衝，初始 empty 狀態
        self.rng = np.random.Generator(np.random.PCG64(seed))                     # numpy 的亂數生成(帶種子固定結果)
        self._row_offsets = np.arange(rows, dtype=np.int64)                       # 第一列、第二列、第三列

    def gen_screen(self) -> np.ndarray:

        for i in range(self.Cols):
            reel = self.ReelStrips[i]                                   # 第 i 條輪帶
            L = reel.size                                               # 第 i 條輪帶的長度
            idx = self.rng.integers(L)                                  # 生成範圍內的整數隨機值
            take_idx = (idx + self._row_offsets) % L                    # 重複利用，不再配置
            start = i * self.Rows                                       # 因為是一維陣列要找存放的起始點
            self.ScreenBuf[start:start+self.Rows] = reel[take_idx]      # 存放
        return self.ScreenBuf

    def view_rows_cols(self) -> np.ndarray:
        """
        返回: 形狀 (Rows, Cols) 的視圖（一般視覺化較直觀）。
        """
        return self.ScreenBuf.reshape(self.Cols, self.Rows).T

    def as_symbol_names(self) -> np.ndarray:
        """
        返回: 以符號名稱矩陣（Rows x Cols）回傳，方便除錯或輸出。
        """
        names = np.asarray(self.Symbols, dtype=object)
        return names[self.view_rows_cols()]


if __name__ == "__main__":
    gen = ScreenGenerator(rows=3, cols=5, reel_strips=REELSTRIPS, symbols=SYMBOLS, seed=None) # 創建實例
    buf = gen.gen_screen()                # 一維 uint8，長度 15
    mat = gen.view_rows_cols()              # 形狀 (3, 5)
    print(buf)
    print(mat)
    print(gen.as_symbol_names())

```


## 修改後
```python
from typing import Optional, List
import numpy as np
from time import time

REELSTRIPS = [
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], # 第一輪
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], # 第二輪
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], # 第三輪
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], # 第四輪
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], # 第五輪
]

SYMBOLS = ["Z1", "C1", "W1", "H1", "H2", "H3", "H4", "L1", "L2", "L3", "L4", "L5"] # 符號清單


class ScreenGenerator:

    def __init__(
        self,
        rows: int = 3,                                                            # 列數預設 3
        cols: int = 5,                                                            # 行數預設 5
        reel_strips: List[List[int]] = REELSTRIPS,                                # 做型別檢查用的必須是 2 維 list
        symbols: List[str] = SYMBOLS,                                             # 同上
        seed: Optional[int] = None,                                               # 同上
    ):
        self._valid()                                                             # 檢查合法性
        self.Rows = rows                                                          # 列數
        self.Cols = cols                                                          # 行數
        self.ScreenSize = rows * cols                                             # 盤面大小
        self.ReelStrips = np.asarray(reel_strips, dtype=np.uint8)                 # 輪帶表，轉成 np 陣列，型別用 uint8
        self.ReelLens = np.asarray([len(r) for r in reel_strips], dtype=np.int32) # 每條 reel 的長度
        self.Symbols = np.asarray(symbols,dtype=str)                              # 符號清單
        self.ScreenBuf = np.zeros(self.ScreenSize, dtype=np.uint8)                # 一次 spin 的輸出緩衝，初始 0 陣列狀態
        self.rng = np.random.Generator(np.random.PCG64(seed))                     # numpy 的亂數生成(帶種子固定結果)
        self._row_offsets = np.arange(rows, dtype=np.int64)                       # 第一列、第二列、第三列


    def gen_screen(self) -> np.ndarray:
        for i in range(self.Cols):
            reel = self.ReelStrips[i]                                   # 第 i 條輪帶
            L = reel.size                                               # 第 i 條輪帶的長度
            idx = self.rng.integers(L)                                  # 生成範圍內的整數隨機值
            take_idx = (idx + self._row_offsets) % L                    # 重複利用，不再配置
            start = i * self.Rows                                       # 因為是一維陣列要找存放的起始點
            self.ScreenBuf[start:start+self.Rows] = reel[take_idx]      # 存放
        return self.ScreenBuf

    # 檢查合法性
    def _valid(self) : 
        # 判斷 rows > 0
        # 判斷 cols > 0
        # REELSTRIPS[i].__len__() > rows
        # REELSTRIPS.__len__() == cols
        # REELSTRIPS[i][j] > 0 && REELSTRIPS[i][j] < len(symbols)
        return
    
    def view_rows_cols(self) -> np.ndarray:
        """
        返回: 形狀 (Rows, Cols) 的視圖（一般視覺化較直觀）。
        """
        return self.ScreenBuf.reshape(self.Cols, self.Rows).T
    
    def as_symbol_names(self) -> np.ndarray:
        """
        返回: 以符號名稱矩陣（Rows x Cols）回傳，方便除錯或輸出。
        """
        names = np.asarray(self.Symbols, dtype=object)
        return names[self.view_rows_cols()]

def runner(rounds: int = 1_000_000, seed : int | None = None) :
    gener = ScreenGenerator(seed=seed)
    print(f"running ScreenGenerator : gen {rounds:,d} screens")
    start = time()
    for i in range(1,rounds+1) :
        gener.gen_screen()
        if i%100000 == 0 :
            print(f"\r{i:,d} / {rounds:,d}",end="",flush=True)
    elapsed = time()-start
    print()
    print(f'used {elapsed:.2f} sec : gen {rounds:,d} screens')

def gen_screen_printer(seed: int | None = None) :
    gener = ScreenGenerator(seed=seed)
    gener.gen_screen()
    print(gener.view_rows_cols())
    print(gener.as_symbol_names())

if __name__ == "__main__" :
    # runner()
    gen_screen_printer()

```
### 回顧
Nex 提供的建議以下幾點
1. 第一個 `if __name__ == "__main__" :` 這裡的內容需要用一個 `runner()` 函數去包，然後只需要調用 `runner()` 就可以比較乾淨。
2. 目前缺少資料合法性的檢查 `def _valid(self) :` 這裡可以再做一些驗證
3. 或許 `REELSTRIPS`  跟 `SYMBOLS` 可以改成放進一個物件裡面
4. 每個物件內要說明清楚，用 `"""..."""` 這個來做，然後一個功能寫一個 function
5. 如果每個輪帶的長度不一樣，用 `tuple(nparray1,nparray2,...,nparray5)` 去包 
6. Python 用駝峰命名法

==所以下次我在 coding 前我應該怎麼思考？==

需要先釐清這個物件具體的工作內容是什麼先規劃出來，還有就是說一些程式實作的規範比如說實際執行的內容要包再一個 main 或是 run function 裡面，然後一定要做一個對輸入數值合法性的數值驗證(比如說判斷是不是正數之類的)，初始設定也可以另外建立一個獨立的物件。註解要說明清楚。

驗證的部分就是先驗證數值傳入 input 的資料型態，這個物件中會有一個 vaild 函數去檢查數值是否正確或是合理。



