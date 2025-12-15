## 1. 概述

以下分為計算 Base Game 和 Free Game 的計算過程

## 2. Base Game

### 2.1. 定義輪帶，進行 slice 分割

**實作:**
利用 ... 定義輪帶表(Reel Bank) 以及權重表(==這有什麼用?==)

<div style="text-align:center">
  <img src="https://hackmd.io/_uploads/rJql2xMkZe.png" style="width:50%;">
    <p>輪帶表和權重表</p>
</div>

這個 Slice table 又有什麼用?

<div style="text-align:center">
  <img src="https://hackmd.io/_uploads/BkJypgGk-e.png" style="width:50%;">
    <p>Slice 分割結果</p>
</div>

建立 slice 公式，

```excel
=IF($Q5>INDEX($D$3:$H$3,1,R$3),
   0,
   INDEX($D$5:$H$104,
         MOD(($Q5-1)+(R$4-1), INDEX($D$3:$H$3,1,R$3))+1,
         R$3)
)
```

上面這個公式作用是，把第 `R3` 條輪帶，從第 `Q5` 個開始，往後數第 `R4−1` 個的位置，拿到那個符號；如果 `Q5` 已經超過這條輪帶的長度，就回傳 `0`。

拆成三步看，首先，找這條輪帶的長度 `INDEX($D$2:$H$2,1,R$2)` 會到 `D2:H2` 去拿第 `R2` 欄的數字，這就是該輪帶的長度（len）。

第二步驟，超過該輪帶的長度就填 0 `IF($Q4>len, 0, …)` 如果你要的起點列 `Q4` 比該輪帶的長度還大，代表這一列沒東西，直接回 0。

最後，算出要拿第幾個、而且會環回開頭 `MOD(($Q4-1)+(R$3-1)` 。`Q4-1` 把列序改成從 0 開始算；`+(R3-1)` 代表 R/S/T 第 1/2/3 欄要往後偏移 0/1/2 個；`MOD(..., len)` 超過尾端就繞回到開頭；最後 `+1` 把索引改回從 1 起算給 `INDEX` 用。

<div style="text-align:center">
  <img src="https://hackmd.io/_uploads/HyiB-jSJZx.png" style="width:100%;">
    <p>Slice 分割</p>
</div>

**‼️驗證:** 如何驗證?

### 2.2. 計算一次盤面中 C1 出現 n 顆的機率

#### **實作:**

計算 `C1` 觸發 Free Game 的次數，根據遊戲規則:

> Base Game 中 {3, 4, 5} 顆 C1 觸發 {7, 10, 15} 局 Free Game（FG）

##### 統計 C1 出現在盤面上的次數

符號 C1 可以出現在盤面的任意位置，先統計 C1 出現在盤面上的次數

<div style="text-align:center">
  <img src="https://hackmd.io/_uploads/Byl-UjSy-e.png" style="width:30%;">
    <p>C1 出現的次數</p>
</div>

##### 統計 {3,4,5} C1 組合數

盤面出現 {3, 4, 5} 顆 C1 的所有組合，利用公式去建立組合

```excel
=ARRAYFORMULA(
 QUERY(
   {
     IF(MID(DEC2BIN(SEQUENCE(32,1,31,-1),5), SEQUENCE(1,5), 1)="1","C1","-"),
     LEN(SUBSTITUTE(DEC2BIN(SEQUENCE(32,1,31,-1),5),"0",""))
   },
   "select Col1,Col2,Col3,Col4,Col5,Col6 where Col6>=3",
   0
 )
)
```

進一步簡化， `FILTER()` 本身就有陣列運算了

```excel
=FILTER(
  {
    IF(MID(DEC2BIN(SEQUENCE(32,1,31,-1),5), SEQUENCE(1,5), 1)="1","C1","-"),
    LEN(SUBSTITUTE(DEC2BIN(SEQUENCE(32,1,31,-1),5),"0",""))
  },
  LEN(SUBSTITUTE(DEC2BIN(SEQUENCE(32,1,31,-1),5),"0",""))>=3
)
```

最後對重複運算進行優化，在公式中 `LEN(SUBSTITUTE(DEC2BIN(SEQUENCE(32,1,31,-1),5),"0",""))` 進行了兩次的重複計算，利用 LET() 函數保存變數值後只需要算一次就行了。

```excel
=LET(
  n, 5, //                                            // 參數
  nums, SEQUENCE(2^n,1,2^n-1,-1),
  bins, ARRAYFORMULA(DEC2BIN(nums, n)),
  bits, ARRAYFORMULA(MID(bins, SEQUENCE(1,n), 1)),
  combo, MAP(bits, LAMBDA(x, IF(x="1","C1","-"))),
  cnt, ARRAYFORMULA(LEN(SUBSTITUTE(bins,"0",""))),
  FILTER({combo, cnt}, cnt>=3)
)
```

##### 計算 {3,4,5} C1 組合機率

#### **‼️驗證:**

利用驗算求
組合出來的所有可能是否有遺漏?怎麼檢查?
計算出來的組合數是否有錯誤?怎麼檢查?

### 2.3. 定義 Super Stack 的轉換機率

![image](https://hackmd.io/_uploads/HJY6QRrybg.png)

定義前 r 輪一樣的機率
![image](https://hackmd.io/_uploads/Hy7CX0BJ-l.png)

### 2.4. 統計數量

原始符號出現的數量直接統計就好

```excel
=COUNTIF(R$4:R$103,$BI5)
```

接下來先計算加上 SS 的期望值再處理加上 Wild，這樣就完成了

```excel
=LET(
  sym, $BI6,                                                                 // 當前符號
  base_cnt, COUNTIF(R$4:R$103, sym),                                         // 當前符號在該輪的數量
  ss_cnt, COUNTIF(R$4:R$103, "SS"),                                          // SS 符號數量
  reel_no, BJ$2,                                                             // 第幾軸
  p, IFERROR(INDEX($BB$4:$BF$11, MATCH(sym, $BA$4:$BA$11,0), reel_no), 0),   // 利用當前符號查找轉換機率表的轉換機率

  base_cnt + ss_cnt * p    // 當前符號的數量 + SS 轉換的期望值
)

```

<!-- 因為 SS 轉換成某個特定的符號，所以需要計算轉換後的更新數量。為什麼要這麼做? 因為這樣只需要修改當前預計要被替換的值就好不用手動去調整這個公式的每一個參數，減少人工錯誤的機會，這樣的架構適用於 具有替代特色，需要更新數量的統計。

current_symbol_count、target_symbol_count、super_stack_count 應該要變成給 current_symbol、SS、target_symbol 就要可以查找對應數量的狀態實現 只需要動三個參數就完成更新。

``` excel
=LET(
  current_symbol,  $CA5,       // 當前的符號
  SS,  "SS",                   // Super Stack
  target_symbol,  "H1",        // SS 要被替換成的符號
  current_symbol_count, BJ5,   // 當前符號的數量
  target_symbol_count, BJ$9,   // SS 要被替換成的符號數量
  super_stack_count, BJ$6,     // SS 的數量

  // 如果當前符號是 "SS" 或是 "要被替換成的符號" 那在判斷他是 "SS" 還是 "要被替換成的符號" 如果是 SS 直接等於 0 如果是 "要被替換成的符號" 那就 SS 數量加上他原本的數量，如果不是 "SS" 或是 "要被替換成的符號" 那就等於他原本自己
  IF(
    OR(current_symbol=SS, current_symbol=target_symbol),
      IF(current_symbol=SS, 0, super_stack_count+target_symbol_count),
      current_symbol_count
  )
)
``` -->

### 2.5. 計算計算組合數與期望值

#### 情況1: 5 軸的 SS 轉換機率皆獨立

因為 Wild 有無首輪的兼容性問題，因此在設計計算組合數的部分需要拆分成 純 Symbol、混和 Wild、純 Wild。

純 Symbol 需要先枚舉出所有符號的組合(H1~H4,L1~L4)，然後排出 5 軸中 5 連線、4 連線、3 連線的所有組合，然後 4 連線跟 3 連線皆要在下一軸設置斷軸，然後後面接 Any (任意 symbol) 這樣的組合。

**解釋:** mini_len 最短長度；filter_sym 所有需要過濾的特殊符號(e.g. C1、SS、S2...)；sym_check 進行檢查；sym_count 計算這個符號的數量；wild_count 計算 Wild 數量；sym_pay 符號賠率；wild_pay wild 賠率。

```excel
=LET(
mini_len,$DM$2,
filter_sym,$CA$6:$CA$8,
  sym, IF(DK4="Wild",IF(DL4="Wild",IF(DM4="Wild",IF(DN4="Wild",IF(OR(DO4="Wild",DO4="ANY"),"",DO4),DN4),DM4),DL4), DK4),
sym_check,IF(COUNTIF(filter_sym,sym)>0,"",sym),

sym_count, IF(sym_check="",0,IF(OR(DL4=sym,DL4="Wild"),IF(OR(DM4=sym,DM4="Wild"),IF(OR(DN4=sym,DN4="Wild"),IF(OR(DO4=sym,DO4="Wild"),5,4),3),2),1)),
  wild_count, IF(DK4="Wild",IF(DL4="Wild",IF(DM4="Wild",IF(DN4="Wild",IF(DO4="Wild",5,4),3),2),1),0),
  sym_pay,  IF(sym_count=0,0,OFFSET(Paytable!$B$3,MATCH(sym,Paytable!$B$4:$B$15,0),sym_count)),
  wild_pay, IF(wild_count=0,0,OFFSET(Paytable!$B$3,MATCH("Wild",Paytable!$B$4:$B$15,0),wild_count)),

  win_sym, IF(AND(sym_count<mini_len,wild_count<mini_len),"",IF(sym_pay>=wild_pay,sym,"Wild"))  ,
  win_count,    IF(AND(sym_count<mini_len,wild_count<mini_len),"",IF(sym_pay>=wild_pay,sym_count,wild_count)),
  win_pay,  IF(AND(sym_count<mini_len,wild_count<mini_len),"", IF(sym_pay>=wild_pay,sym_pay,wild_pay)),
win_hit,PRODUCT(VLOOKUP(DK4,$CA$5:$CP$56,2,False()),VLOOKUP(DL4,$CA$5:$CP$56,5,False()),VLOOKUP(DM4,$CA$5:$CP$56,8,False()),VLOOKUP(DN4,$CA$5:$CP$56,11,False()),VLOOKUP(DO4,$CA$5:$CP$56,14,False())),
win_prob, win_hit/$DS$3,
win_rtp,win_prob*win_pay,

  {win_sym,win_count,win_pay,win_hit,win_prob,win_rtp}
)
```

#### 情況2: 前 3 軸綁定，後 2 軸獨立

#### 情況3: 前 4 軸綁定，後 1 軸獨立

#### 情況4: 所有 5 軸綁定

這東西就相當於 `Mystery Symbol`，計算方法就是先建立轉換機率矩陣(SS->H1、SS->H2、...、SS->L4)後分別計算當 SS 變成 {H1,H2,...,L4} 的期望值，最後加總。所以在實作上會需要定義一個機率矩陣，然後在計算 SS 轉換成某個符號後的符號數量(e.g. SS 全部變成 H1 後 H1 就等於原本的 H1 數量 + SS 數量) 最後利用這個符號數量去計算組合數、機率，期望值。

<!--
``` excel
=LET(
  syms, $BI$9:$BI$16,        /* 這裡放 H1~H4,L1~L4，一欄 8 格 */
  n, ROWS(syms),
  totalRows, n*5,
  MAKEARRAY(
    totalRows, 5,            /* 每個 symbol 5 列 × 5 軸 */
    LAMBDA(r,c,
      LET(
        groupRow, MOD(r-1,5)+1,          /* 每個 symbol 內的第幾列 1~5 */
        symIdx,  INT((r-1)/5)+1,         /* 第幾個 symbol */
        s, INDEX(syms, symIdx),
        IF(
          groupRow=1,                    /* 第一列：全都是 S */
          s,
          LET(
            wildPos, 7-groupRow,         /* #(...+WILD) 要放的軸位置：5,4,3,2 */
            IF(
              c < wildPos,
              s,                         /* 左邊都是 S */
              IF(
                c = wildPos,
                "#(" & s & " + WILD)",   /* 這一軸是 #(S+WILD) */
                "ANY(所有)"              /* 後面通通 ANY */
              )
            )
          )
        )
      )
    )
  )
)

``` -->

## 3. Free Game

## 4. Paytable

## 5. Question

FG 隨著 S2 累積數量越多中獎率越低，這樣顯然不合理。
