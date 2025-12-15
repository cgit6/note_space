1. 「建構器／工廠函式」 是什麼?
   Go 沒有真正的 class constructor，所以大家用 `NewXxx` 這種慣例命名來「建立並初始化一個可用的實例」。

2. `make()` 是什麼?

3. 簡寫

```go=
 // 2. 執行初始化
 err := cfg.Init()
 if err != nil {
  return nil, err
 }

    // 等同於以下
 if err := cfg.Init(); err != nil {
  return nil, err
 }
```

1. `return errors.New("reelStrips length (%d) must == Cols (%d)", len(c.ReelStrips), c.Cols)` 這樣寫不對嗎?
   這樣寫不對。`errors.New` 只接受一個純字串參數，不支援 `%d` 這種格式化

2. for loop 在跑「slice of slice」的典型用法。

```go=
for i, line := range c.Lines {
    if len(line) != c.Cols {
        return fmt.Errorf("line[%d] length (%d) must == Cols (%d)", i, len(line), c.Cols)
    }
    for _, r := range line {
        if r < 0 || r >= c.Rows {
            return fmt.Errorf("line[%d] has invalid row index %d (Rows=%d)", i, r, c.Rows)
        }
    }
}

// 相同寫法
for i := 0; i < len(c.Lines); i++ {
    rowIndices := c.Lines[i]
    if len(rowIndices) != c.Cols {
        return fmt.Errorf("line %d: length=%d, want %d", i, len(rowIndices), c.Cols)
    }
    for col := 0; col < len(rowIndices); col++ {
        row := rowIndices[col]
        if row < 0 || row >= c.Rows {
            return fmt.Errorf("line %d, col %d: row index %d out of range [0,%d)", i, col, row, c.Rows)
        }
    }
}


```

1. 為什麼需要 New...() func 來創建 instance? 不是可以直接創建嗎?

```go=
// 建構函數: 創建 instance 時調用
func NewConfig(reelStrips [][]int, symbols []string, lines [][]int, payTable [][]int, rows, cols int, mode GameMode) (*Config, error) {
 // 1. 創建 Config instance & 賦值
 cfg := &Config{
  ReelStrips: reelStrips, // 輪帶表
  Symbols:    symbols,    // 符號清單
  Lines:      lines,      // 線路清單
  Paytable:   payTable,   // 賠率表
  Rows:       rows,       // 列數
  Cols:       cols,       // 行數
  Mode:       mode,       // 算分模式
 }

 // 2. 執行初始化
 if err := cfg.Init(); err != nil {
  return nil, err
 }
 // 3. 返回值, 錯誤訊息
 return cfg, nil

}
```

**理由1:** 參數在作為函數輸入值的時候會自動複製一份
**理由2:** 錯誤處理、Init 驗證...
**理由3:** API 穩定、可維護
**理由4:** 不對外公布實作細節

什麼時候可以「不寫 New」？
這個型別零值即可用、沒有必填欄位／沒有複雜初始化（例如 bytes.Buffer）。

小示例對比

A. 沒有 constructor：

```go=
cfg := &Config{ReelStrips: reels, Symbols: symbols, Rows: 3, Cols: 5, Mode: ModeWays}
if err := cfg.Init(); err != nil { return err } // 每處都要記得呼叫
```

B. 有 NewConfig（建議）：

```go=
cfg, err := NewConfig(reels, symbols, lines, pay, 3, 5, ModeWays)
if err != nil { return err } // 一行檢查，之後放心用
```

C. 進階：選項模式

```go=
cfg, err := NewConfig(reels, symbols, 3, 5, WithLines(lines), WithPayTable(pay), WithMode(ModeWays))
```

D. 防止呼叫端亂建：
將必要欄位改成未匯出，或把型別做成未匯出、只暴露 NewConfig。這樣大家只能透過 constructor 走正確流程。

> 在 Go 裡，「未匯出（unexported）」就是指名稱是小寫開頭的識別字。未匯出的東西只在同一個 package 內可見；跨 package 就看不到 / 不能用。相對地，大寫開頭的是「已匯出（exported）」，其他 package 可以用。適用範圍：型別、函式、方法、變數、常數、struct 欄位都一樣遵守這個規則。

<!-- 7. 錯誤處理 -->

1. 建構函數中，如果要引入其他的 struct 要怎麼做?

```go=
 cfg, err := NewConfig(REELSTRIPS, SYMBOLS, LINES, PAYTABLE, ROWS, COLS, ModeLine)
```

這個 cfg 是 pointer?

因為 go 中沒有物件導向所以就沒有繼承的概念

```
兩個 struct A, B
1. 傳入 A instance 的 pointer -> B 建構函數
2. 在 B 建構函數創建 B instance 的時候將 A pointer 添加其中當然， B struct 在宣告的時候也需要宣告 *A (至少是匿名函數)
```

1. 什麼是 receiver?

這裡的 **receiver（接收者）** 指的是 Go 裡面「方法」前面那個特別參數，就是你看到的這段：

```go
func (p Point) Move(dx, dy int) { ... }
     ^^^^^^^
     這一坨叫 receiver
```

拆開講會比較清楚：

---

## 1. 在 Go 裡，receiver 是什麼？

一個完整的 method 長這樣：

```go
func (p Point) Move(dx, dy int) {
    p.X += dx
    p.Y += dy
}
```

結構：

- `func`：宣告函式 / 方法
- `(p Point)`：👉 **receiver**
  - `p`：這個方法裡，用來指代那個物件的「變數名稱」
  - `Point`：這個方法「掛在」哪一個型別上（也就是 receiver type）

- `Move`：方法名字
- `(dx, dy int)`：一般參數
- `{ ... }`：方法本體

所以可以說：

> **receiver = 方法的「隱藏第一個參數」＋「這個方法是屬於哪個型別」的宣告。**

呼叫時：

```go
var p Point
p.Move(3, 4)  // 這裡的 p 就會被當成 receiver 傳進去
```

編譯器其實會幫你轉成類似：

```go
Move(p, 3, 4)
```

只不過你寫的是物件風格：`p.Move(...)`，
而不是 C 風格：`Move(&p, ...)`。

---

## 2. value receiver vs pointer receiver

Go 裡 receiver 也可以是指標：

```go
func (p *Point) Move(dx, dy int) {
    p.X += dx
    p.Y += dy
}
```

這兩種：

- `func (p Point) ...`：**值 receiver**（複製一份）
- `func (p *Point) ...`：**指標 receiver**（可以改到原本那個）

概念上就跟 C 的：

```c
void Point_Move(struct Point *p, int dx, int dy);
```

很像。

---

## 3. 跟 C 的對照

在 C 裡沒有方法、沒有 receiver，所以你通常會這樣寫：

```c
struct Point {
    int x;
    int y;
};

void Point_Move(struct Point *p, int dx, int dy) {
    p->x += dx;
    p->y += dy;
}
```

呼叫時：

```c
struct Point p = {0, 0};
Point_Move(&p, 3, 4);
```

對照到 Go：

```go
type Point struct {
    X int
    Y int
}

func (p *Point) Move(dx, dy int) {  // p 就是 receiver
    p.X += dx
    p.Y += dy
}

p.Move(3, 4)  // 編譯器幫你轉成 Move(&p, 3, 4)
```

所以你可以把 **receiver 想成：**

> 「寫在函式名字前面的那個特別參數，用來代表『這個方法所屬的那個物件』。」

只是在 Go 語法裡它被放在 `( ... )` 和方法名中間，而不是像 C 一樣放在參數列表裡。

1. spinCalculator 的算分策略選擇看不太懂
   現在看起來是

   10.如果像是 S2 這種特殊符號會影響到得分符號呢?
   之後會拆分成 slotGame struct 裡面先生成盤面 -> 計算得分結果 ->
