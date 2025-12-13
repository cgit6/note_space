
## 遊戲規格

>[Line Game]
>
>[基本規格]
盤面：3×5，固定 20 條線，左起連線結算。
符號：C1、SS、S2（僅 FG 第 5 軸）、Wild、H1\~H4、L1\~L4。
>
>Wild：可代替 {H1~H4, L1~L4}，不可代替 {C1, SS, S2}。同一條線若同時可視為 Wild 連線或目標符號連線，僅取較高賠付，不重複計付。全 Wild 連線使用 Wild 賠表，其餘使用目標符號賠表。
>
>Base Game 中 {3, 4, 5} 顆 C1 觸發 {7, 10, 15} 局 Free Game（FG），Free Game 內不會出現 C1
>
>[特色]
>a. SS(Super Stack)，Base Game 以及 Free Game 都會出現在盤面生成前，SS 會每局、每軸各自隨機抽一個目標符號，該軸所有 SS 在該局皆轉為該目標。
>BG 中：SS 有機會隨機轉為 H1~H4, L1~L4 目標符號
>FG 中：SS 只會隨機轉為 H1~H4 等高分目標符號
>
>b. C1(在 BG 中)，出現 {3,4,5} 觸發 {7,10,15} 次 FG；FG 中不出現 C1。
>
>c. S2 只會在 Free Game 中出現，且只出現在第 5 軸。如果 Free Game 中累積出現 S2 滿足以下條件，對應發生效果：
>
>累積出現 2 次 S2： FG 局數 +3 之後將各軸輪帶上所有 L4 轉為 SS（效果自下一局生效）
>累積出現 5 次 S2： FG 局數 +3 之後將各軸輪帶上所有 L3 轉為 SS（效果自下一局生效）
>累積出現 8 次 S2： FG 局數 +3 之後將各軸輪帶上所有 L2 轉為 SS（效果自下一局生效）
>累積出現 10 次 S2： FG 局數 +3 之後將各軸輪帶上所有 L1 轉為 SS（效果自下一局生效）
>
>

## 動機

雖然遊戲內容大部分相似於之前的延伸 Line Game，其實就是 Mystery Symbols 換成 Super Stack 然後從沒有 Wild 新增為有 Wild 的機制，因為我想花點時間把==混合 wild 組合的公式==寫一次看看，然後有時間可以想一下上次說的基礎的驗證該怎麼做。之後我對 parsheet 表格在遊戲發想的部分會朝著每次改一點點然後有機會可以探討細節為主。不管是數學邏輯還是表格的設計都是我想練習的重點。

## Base Game 計算方法

### 第一步: 定義輪帶，進行 slice 分割

建立 5 條輪帶，並以每軸連續 3 格為一個 slice（含環狀） 進行切分。

### 第二步: 計算 C1 出現的機率

利用 slice 統計 C1，在一次盤面中出現 {3,4,5} 顆 C1 的組合數與機率，並計算期望值（以本局總押注計算）。

利用 excel 公式排列出 C5 取 5、C5 取 4、C5 取 3 的組合。然後統計數量計算組合數。

### 第三步: 定義 Super Stack 的轉換機率

<!-- 我想出兩種方法我想都做看看，看會不會有誤差。 -->

**方法(用期望數量直接算組合):**
設定 Super Stack 在每一軸轉為成每一個符號的機率。例如有 5 軸，SS 可轉為 8 種符號，所以共需定義 40 個數值。

<div style="text-align:center">
  <img src="https://hackmd.io/_uploads/B1muXWf1bl.png" style="width:100%;">
    <p></p>
</div>

這麼做會有問題，r1 ~ r5 連續出現相同的符號機率太低了(下方模式優化遊戲體驗)，透過定義由左至右出現相同符號的機率來解決上面遇到的問題，定義幾軸符號鎖定。 0 代表保持原本 Super Stack 的設定，3 表示前三軸保持一致。

<div style="text-align:center">
  <img src="https://hackmd.io/_uploads/Byesm-GJ-e.png" style="width:80%;">
    <p>定義連線機率</p>
</div>

### 第四步: 計算符號數量

**方法:**
先用 COUNTIF() 計算每個符號在每一軸出現的數量，並且每一軸的 SS 轉為 H1\~H4, L1\~L4 後更新符號的數量。
> SS 有 20 顆 換成 H1 有 30% 機率， H1 原本有 4 顆所以更新的 H1 期望數量是 10 顆。

再處理 Wild 對各符號顆數的影響；例如計算 H1（含 Wild 與 SS 轉為 H1 的量） 的有效顆數。

> H1 的期望顆數=10、Wild=5 → H1（含 Wild）有效顆數=15。
> 非（H1 或 Wild）的顆數 = 輪帶長度 − 15。

<!-- **方法2:**
一樣是先用 COUNTIF() 計算每個符號在每一軸出現的具體數量。然後分別列出如果 SS 轉為某個符號後的符號數量，例如 SS 能轉為 8 種符號，那就列出每個替代後的數量組合共 8 組。

<div style="text-align:center">
  <img src="https://hackmd.io/_uploads/HyK-BcbJZx.png" style="width:80%;">
    <p>計算替代後每個符號的數量</p>
</div>

然後排列出所有轉為目標符號的可能組合，共 8 的 5 次方種可能

<div style="text-align:center">
  <img src="https://hackmd.io/_uploads/rJ-4U9-kWl.png" style="width:80%;">
    <p>排列出所有 SS 替代的可能</p>
</div> -->

### 第五步: 計算組合數與期望值

**方法**
對應第四步方法1，利用更新後的每個符號的期望數量來計算純 Normal Symbol、混和 Wild、純 Wild 組合數。後結算 Base Game 的期望值。

<!-- **方法2**
對應第四步方法2，利用排列出所有替代的可能 所對應的組合去計算每個組合的期望值，再乘以這個組合出現的機率。 -->

### 驗證

利用公式寫後面的組合

<div style="text-align:center">
  <img src="https://hackmd.io/_uploads/SJBE4ogy-x.png" style="width:60%;">
    <p>混和 Wild 的組合</p>
</div>

驗算各項數值

<div style="text-align:center">
  <img src="https://hackmd.io/_uploads/BJ6a4oxJbx.png" style="width:25%;">
    <p>成立線數</p>
</div>

如果還有想到可以做驗算的再做補充。

## Free Game（FG）計算方法

前置規格：FG 內不出現 C1；S2 僅出現在第 5 軸；累積 S2 命中達 {2,5,8,10} 時，各自 +3 局，並將 {L4,L3,L2,L1} 依序轉為 SS（效果自下一局生效）。SS 在 FG 僅能轉為 H1~H4。

### S2 命中機率

以第 5 軸的輪帶做 slice 統計，計算「三格視窗內至少 1 顆 S2」的機率。

### S2 特色計算

先計算 S2 第 t 局出現 n 顆 S2 的機率，再計算每一局累積機率(採用馬可夫鏈)，再處理 SS(Super Stack) 每一個符號的影響。來更新符號的期望數量然後再分別計算 SS 轉為各目標符號後的期望值，最後與第 t 局出現 n 顆 S2 的機率與所對應的期望值做相乘，最後再加總為整個 Free Game 的期望值。

### S2 加局計算

起始局數 r0 由 BG 的 C1={3,4,5} 決定為 {7,10,15}；FG 內不出現 C1，僅由 S2 達門檻時各 +3 局。

* 3 顆 C1 觸發 7 局 FG 的 S2 會另外再觸發加 3 局
* 4 顆 C1 觸發 10 局 FG 的 S2 會另外再觸發加 3 局
* 5 顆 C1 觸發 15 局 FG 的 S2 會另外再觸發加 3 局

所以現在變成要分開計算 {3,4,5} 顆 C1 的期望值乘以 P({3,4,5} 顆 C1) 後加總。

### 驗證

這部分大致上跟 Base Game 雷同，所以我可以做的除了上面提到的數值驗證之外，嘗試將表格整理得更乾淨。

## 其他

[改善建議](https://hackmd.io/@chiSean/By7iWsWJZg)

[細節描述](https://hackmd.io/@chiSean/rkJdSJfybg)
