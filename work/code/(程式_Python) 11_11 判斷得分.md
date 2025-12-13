
最下方有完整腳本

<!-- ## 一、遊戲規格與資料結構

### 1.1 盤面規格

- 列數（Rows）：3
- 行數（Cols）：5
- 盤面用 **一維陣列** 表示：長度 `Rows * Cols = 15`，裡面存放「符號 ID」（整數）




### 1.2 靜態表格

- `REELSTRIPS`：輪帶表  
  - 型別：`Tuple[np.ndarray, ...]`  
  - 每條輪帶是一個一維 `np.ndarray[uint8]`，長度可不同  
  - 值為「符號 ID」

- `SYMBOLS`：符號清單  
  - 型別：`List[str]`  
  - index = 符號 ID，例如 `0:"Z1", 1:"C1", 2:"W1", ...`

- `LINES`：線獎組合  
  - 型別：`np.ndarray[uint8]`，shape = `(num_lines, Cols)`  
  - 每一列為一條線，內容是「row index」（0, 1, 2）

- `PAYTABLE`：賠率表  
  - 型別：`np.ndarray[int64]`，shape = `(num_symbols, 5)`  
  - 第 i 列 = 第 i 個符號，欄位對應「1 ～ 5 連」的賠率

### 1.3 物件架構

- `SlotConfig`  
  - 負責保存靜態資料：`reel_strips / symbols / lines / pay_table / rows / cols`

- `SlotInit`（基底類別）  
  - 共用屬性：`Rows, Cols, ScreenSize, ReelStrips, ReelLens, Symbols, lines, PayTable, Bet`  
  - 提供 `_valid()` 做參數合法性檢查

- `ScreenGenerator(SlotInit)`  
  - 負責：亂數生成單一盤面  
  - 主要方法：
    - `gen_screen() -> np.ndarray`：回傳一維盤面（長度 15）
    - `view_rows_cols() -> np.ndarray`：轉成 (Rows, Cols) 視圖
    - `as_symbol_names() -> np.ndarray`：轉成符號名稱矩陣

- `SpinCalculator(SlotInit)`  
  - 負責：對單一盤面做數學計算與統計  
  - 主要成員：
    - 模擬統計：`TotalWins, TotalBets, baseRtp`
    - 亂數不在這裡處理，只吃外部給的 `screen`
  - 主要方法（對應任務 2）：
    - `transPayLine(screen)`
    - `hitCheck(line_values)`
    - `countC1(screen)` -->

## 二、任務拆解

前面已經生成盤面了，上次提到可以再調整的地方

```
1.資料合法性的檢查 def _valid(self) : 這裡可以再做一些驗證
2.REELSTRIPS 跟 SYMBOLS 可以改成放進一個物件裡面
3.每個物件內要說明清楚，用 """...""" 這個來做，然後一個功能寫一個 function
4.Python 用駝峰命名法


接下來，判斷線的中獎
1.依照當前盤面獲取每一條線的狀態(e.g. 11111,22222,33333...)
2.判斷每條線上是否有中獎組合出現
3. 獲取賠率
```

<!-- 然後我會想要驗證一個是用 for loop 跑檢查另一個是查表的方式哪個比較快

 ### **概況**

目前的程式碼已經完成了遊戲初始化以及生成盤面的操作，詳情見 [[程式/Python] 10/30 生成盤面](/Ymdww3_8TnuYu5Dcl8kCEQ)
 -->


### **任務1:** 初始化與資料驗證（SlotInit / SlotConfig）


創建一個遊戲參數的物件 `SlotConfig`，裡面包含輪帶表、符號表、線獎組合與賠率表；
`SlotInit` 則拿 `SlotConfig` 來建立共用屬性，並在 `_valid()` 中做合法性檢查。

<!-- 這裡記得要做資料格式檢查再做數值合法性檢查。
先初始化一個儲存所有生成結果的三維 0 陣列 (e.g. 3\*5\*1,000,000)  -->

**目標：**  
在程式啟動時，正確載入並驗證所有靜態遊戲參數。

``` python=

```

<!-- 接下來要嘗試檢查參數的資料型態(逐一列舉出來) -->

### **任務2:**
`SpinCalculator` 在「給定一個盤面（screen）」的前提下，完成整個得分計算流程。

<!-- ==每一個子任務在 SpinCalculator 物件中獨立建立一個 Function==。 -->

<!-- 可能的改進: 先在某個地方儲存所有盤面生成的結果(比如生成了 100 萬個盤面後再進到判斷中獎階段) -->

首先，會需要對應每個線獎提取出在這個盤面中每個線獎組合對應的數值(符號)，先轉換成一個二維陣列清單。

任務 2.1: 根據當前盤面（一維 np array）與線獎組合，取得每條線上的實際數值。
``` python

```

<!-- 
具體的功能是在盤面生成完了之後(盤面的數值用一維 np array 儲存)利用當前盤面上的數值，與線獎組合(是一個二維 np array 儲存了每一條線獎的索引值比如說 [2, 2, 2, 2, 2] 就是 第一軸索引位置 2) ，在 SpinCalculator 物件中會有一個 self.transToLine 參數用於緩存這個轉換後的結果

因為現在生成的盤面是 1\*15 的一維 np array 所以在利用線獎的索引的時候那個索引值應該是 第 i軸，第 j 列比如說第 3 組線獎 [2, 2, 2, 2, 2] 陣列中第 1 個 2 代表第 1 軸第 2 列的這個位置，陣列中第 2 個 2 代表第 2 軸第 2 列的這個位置等等，所以實際上在獲取數值的時候因為是 1 維 np array 所以需要 index 數 + row index 位置當作索引值。然後 迴圈的跑完所有線獎組合後會有一個與線獎組合大小相同的 2 維度陣列，裡面的數值就是當前盤面上對應的數值，這個功能寫在 SpinCalculator 物件的 transPayLine func 中。

* transPayLine 函數中的 screen 要怎麼確保是 uint8 怎麼驗證?
* 那 transPayLine 函數的結果要怎麼確保正確? 
-->



接下來，判斷每個清單中是否中獎:

#### **方法1:**


任務2.2: 得分符號: 判斷是否中獎，中獎的組合是哪一個(什麼符號，連現數多少) 的流程

1. 找「得分符號」的連線數與 W1 符號的連線數

> 對當前組合 self.transToLine[i] 逐一做檢查，分成得分符號跟 W1 符號的連線計算，然後比較是得分符號的賠率比較高還是 Wild 連線的賠率比較高，如果是 得分符號賠率比較高則這條線用得分符號的賠率計算，否則就用 Wild 連線的賠率計算。

流程

```

```

實作

``` python=

    
```


<!-- **賠率 \* 下注金額** 這件事要在哪裡做? -->





任務2.3: C1 符號: 檢查目前盤面上的 C1 符號數量

> 直接計算 C1 連線數，就是直接統計這條一維陣列中有多少個 C1 符號。

``` python=

```

任務2.4: 再來去看目前所有線獎結果的賠率是多少



<!-- #### **方法2:**
在 `SpinCalculator` 物件建立中獎清單，枚舉所有中獎組合，實現快速查詢。

**任務 3:**
任務 3.1: 在 `SpinCalculator` 的初始化階段枚舉出所有中獎條件 ==(未實做)==

任務 3.2: 在 `SpinCalculator` 利用查找該中獎清單的方式確認有沒有中獎，如果有找到就會返回一個賠率 ==(未實做)==
 -->

<!-- ### **任務4:**
最後，計算期望值，利用 總中獎金額/下注金額 計算期望值

任務4.1: 計算每個盤面中獎金額

任務4.2: 更新總中獎金額

任務4.3: 計算期望值 -->


## 可能會遇到什麼問題

資料結構的選擇，上面這些參數中那些東西的資料結構可以更好讓效能更佳? ==(未實做)==
<!-- * 更高級的亂數生成方式 -->


## 要怎麼驗證每一步的數值是正確的

首先，建立一個 PAR sheet 計算理論期望值，了解最終計算的數值有沒有錯誤。 ==(未實做)==

## 目前程式碼

[github 連結](https://github.com/cgit6/slot/blob/master/ScreenGenerator.py)


## 反饋

1. 正確性OK
2. `calculator` 對外應該只暴露一個 `calcScreen(screen)` 不需要對外暴露太多自組的內容:`countC1` `transPayLine` `hitCheck` ...
3. 少設計了一個盤面結果的 class : `calcScreen(screen) -> ScreenResult` 讓計算盤面的結果是一個物件(所有對結果的處理和取值、輸出應該對`ScreenResult`實作)


4. 原則: 外部做完檢查後，內部不用再做檢查: 現在很多地方接收 `screen` 之後又轉一次`asarray() -> np.ndarray` 不需要的(2.3.有做到的話:不要把其他內部API暴露對外)
5. 計算上的建議
    - 不需要建立線表: 直接算出screen[pos] -> 該位置的symbol
    - from i:0->col check:
        1. symbol = screen[line[i]]
        2. symbol == wild and wildcontinue (wildcount++) else wildcontinue = false
        3. symbol in winSymbols : symId = symbol else: break
    - 就可以一次收集完所有 wildcnt 和 symId symcnt -> 接回取得各自得分



### Spin 流程

 #### 創建機台
    
     1. 開哪台
     2. [v]吃哪個config
     3. [v]實例化哪個遊戲邏輯
     4. 暴露Spin(SpinRequest) -> SpinResult
 
 #### 一個 Spin
 
     1. 發起Spin請求(SpinRequest)(帶上 bet int)
     2. 對應機台收到Spin請求 (對SpinRequest 作 valid)
     3. [ing]機台內部流程(gen calc...)
     4. Spin結果(SpinResult) (有total_win int)
     
 #### 序列化＆ svr -> 可以對外部提供服務 (不處理)
 
 #### Simulator (也是 class)
 
     1. rounds=100萬, totalwin=0, total_bet=0 —>
     2. for i in range(rounds) : 
         result = game.Spin(SpinRequest)
         st.record(result)
     3. rtp = st.rtp , cv = st.cv std=st.std
     
### Stat (統計 class)
... 會需要一個 stat 物件用來評估模擬結果的統計值。期望值、波動率、標準差...


## 需要思考到的點


<div style="text-align:center">
  <img src="https://hackmd.io/_uploads/Bk5uoIlebx.png" style="width:80%;">
    <p>圖 1 架構圖</p>
</div>

<!-- 

如何寫計畫書?
大致架構 -> 首先，我會需要哪些功能? 再來這些功能需要什麼樣的資料結構 (需要哪些變數這些變數又是什麼資料型態)? 最後裡面的 Function 要怎麼實現? 他的流程是什麼? 

有哪些物件會因為遊戲規則變動而產生變化? 
```
 Config 不會
 Init 不會
 ScreenGenerator 不會
 SpinCalculator 會
 ScreenResult 不會
```

因此 `SpinCalculator` 需要針對兼容不同遊戲規則做處理。


 -->
