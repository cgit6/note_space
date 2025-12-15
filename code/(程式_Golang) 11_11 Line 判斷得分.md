## 計畫書 v1

### 結構

```go=
Config struct            // 遊戲靜態設定 (輪帶 / 符號 / 線表 / 賠率 / 模式…) 與合法性檢查
ScreenGenerator struct   // 生成隨機盤面 (spin)
SpinCalculator struct    // 計算一個盤面的得分 (支援 Line / Ways 模式)
LineResult struct        // 每條線的結果
ScreenResult struct      // 單一盤面的算分結果
SlotGame                 // 封裝 Generator + Calculator，對外提供 Spin()
Simulator                // 執行模擬
Stat struct              // 統計模擬結果 (RTP / Std / CV…)
```

### 注意事項

1. ScreenResult、LineResult 作為接收結果的資料結構
2. 將 SlotGame、Simulator、Stat 獨立出來

- Simulator：不需要關心是 Line 還是 Ways，永遠只呼叫 game.Spin()。
- SlotGame：內部用 ScreenGenerator + SpinCalculator，對外提供 Spin()。

1. ==如果 `SpinCalculator` 需要兼容計算 way game 在不改變函數調用的狀態下==

- `Config` struct 定義模式。
- `SpinCalculator` struct 依據模式不同算分方法不同。

`Config` struct 負責處理遊戲不會變動的靜態設定。

```go=
type GameMode int

const (
    ModeLine GameMode = iota  // Line
    ModeWays                  // Ways
)

type Config struct {
    ReelStrips [][]uint8    // 輪帶表 [Cols][reelLen]
    Symbols []string        // 符號清單
    Lines [][]int           // 線獎組合
    PayTable [][]int        // 賠率表 [symbolId][0..4] = 1~5 連賠率

    Rows int                // 盤面列數
    Cols int                // 盤面軸數
    Mode GameMode           // 算分模式 Lines / Ways (enum)
}
```

`Init` struct 提供共用的基本屬性與合法性檢查

```go=
// Init 承載所有「靜態且可驗證」的機台資訊（由 Config 建立展開）
// - 只做資料承載與合法性檢查，不含隨機或動態狀態
type Init struct {
    Config     *Config      // 從 Config 展開的核心參數
    Rows       int          // 盤面列數
    Cols       int          // 盤面軸數
    ScreenSize int          // Rows * Cols
    ReelStrips [][]uint8    // 各軸輪帶（每條長度可不同）
    ReelLens   []int        // 每條輪帶長度（由 ReelStrips 衍生）
    Symbols    []string     // 符號名稱表
    Lines      [][]int      // 線獎定義（Line 模式必填；Ways 可為空）
    PayTable   [][]int      // 賠率表 [symbol][1..5 連]
    Mode       GameMode     // ModeLine / ModeWays
}

// NewInit 根據 Config 建立 Init 並做完整驗證
func NewInit(cfg *Config) (*Init, error) {
    // 1) 將 Config 的靜態資料複製/展開到 Init
    // 2) 依 ReelStrips 計算 ReelLens（每條輪帶長度）
    // 3) 呼叫 init.Valid() 做資料合法性檢查
    //    - 通過：回傳 *Init
    //    - 失敗：回傳 error
    //
    // 回傳：(*Init, error)
    return nil, nil
}

// Valid 針對 Init 內部資料做「一次性」合法性檢查
func (i *Init) Valid() error {
    // 一、基本結構檢查
    // 1) Rows / Cols 必須 > 0
    // 2) len(ReelStrips) 必須 == Cols

    // 二、輪帶內容檢查
    // 3) 每條輪帶長度必須 >= Rows
    // 4) 每個輪帶內的 symbol index 必須落在 [0 .. len(Symbols)-1]

    // 三、線獎檢查（依模式分流）
    // 5) 若 Mode == ModeLine：
    //      - Lines 不可為空
    //      - 每條 line 的長度必須 == Cols
    //      - 每個 line 的 row index 必須落在 [0 .. Rows-1]
    //    若 Mode == ModeWays：
    //      - Lines 可為空（不使用線獎）
    //      - 若 Lines 非空，仍需滿足「長度 == Cols、row index 在界內」以利除錯

    // 四、賠率表檢查
    // 6) len(PayTable) 必須 == len(Symbols)
    // 7) 每列賠率長度必須 == 5（目前假設 1~5 連）

    // 以上有任何不符，回傳對應錯誤；否則回傳 nil
    return nil
}
```

`ScreenGenerator` struct 負責生成隨機盤面(spin)

```go=
type ScreenGenerator struct {
    Init      *Init      // 共用靜態資訊
    ScreenBuf []uint8    // 盤面緩衝區 (一維：長度 Rows*Cols)
    rng       *rand.Rand // 亂數生成器
}

func NewScreenGenerator(init *Init, seed int64) *ScreenGenerator {
    // 建立 rng、初始化 ScreenBuf...
    return &ScreenGenerator{Init: init, ...}
}

// GenScreen 產生一個隨機盤面 (一維 []uint8, 每格是 symbolID)
func (g *ScreenGenerator) GenScreen() []uint8 {
    // 對每一軸：
    //   1) 隨機決定一個起始 index
    //   2) 連續取 Rows 個 symbolID
    //   3) 塞進 ScreenBuf
    return g.ScreenBuf
}

func (g *ScreenGenerator) ViewRowsCols() [][]uint8 {
    // 把一維 ScreenBuf reshape 成 Rows x Cols (用 slice / index 計算)
    return nil
}

func (g *ScreenGenerator) AsSymbolNames() [][]string {
    // 把 ViewRowsCols() 的每個 symbolID 換成對應的 Symbols[name]
    return nil
}

```

`LineResult` 單條線的得分結果。

```go=
type LineResult struct {
    LineIndex int // 線號 (0-based)
    SymbolID  int // 中獎符號 ID；-1 表示沒中
    Count     int // 連線數
    Pay       int // 該線賠率 (尚未乘 line bet)
}
```

`ScreenResult` 一次盤面計算的結果。

```go=
type ScreenResult struct {
    Screen       []uint8      // 原始盤面 (一維 symbolID)
    C1Count      int          // 盤面中 C1 (scatter) 出現次數
    LineResults  []LineResult // 每條線結果 (Line 模式用)
    TotalLinePay int          // 線獎賠率總和
    TotalWin     int          // 最終贏分
}
```

`SpinCalculator` struct 在「給定一個盤面（screen）」的前提下，計算連線賠率 / C1，在這裡添加利用，回傳 `ScreenResult` struct ，另外這裡會受 `Config` struct 的影響採取不同的算賠率與算分方式 (前面注意事項第三點提到)

```go=
// calcFn 型別：給定盤面與 Bet
type CalcFunc func(screen []uint8, Bet int) ScreenResult


type SpinCalculator struct {
    Init *Init                 // 指向 Init


    TotalWins float64          // 累積總贏分
    TotalBets float64          // 累積總下注

    calcFn CalcFunc            //  真正執行算分的函數 (依 Init.Mode 決定)
}

func NewSpinCalculator(init *Init) *SpinCalculator {
    c := &SpinCalculator{Init: init}
    c.initCalcFunc()
    return c
}


// 根據 Init.Mode 決定要用哪一個算分函式
func (c *SpinCalculator) initCalcFunc() {
    switch c.Init.Mode {
    case ModeLine:
        c.calcFn = c.calcLineGame
    case ModeWays:
        c.calcFn = c.calcWaysGame
    default:
        panic("未知 mode")
    }
}


// 對外統一調用 CalcScreen：不管是 Line 還是 Ways，都呼叫 CalcScreen
func (c *SpinCalculator) CalcScreen(screen []uint8, Bet int) *ScreenResult {
    // 計算一次 spin 生成的盤面得分結果，根據 c.calcFn() 的算分策略
    return c.calcFn(screen, Bet)
}

// ------- 下方是不同模式的內部實作 -------

// Lines Game 算法
func (c *SpinCalculator) calcLineGame(screen []uint8, Bet int) ScreenResult {
// 1) 計算 C1 數量
    // 2) 對每條線，用單一迴圈算 wildCount / symId / symCount / pay，累加 TotalLinePay
    // 這邊計算怪怪的要在確認一下
    // 3) TotalWin = TotalLinePay * Bet / 線數 (❗剛剛改的， Bet 是一次 spin 下注金額)
    // 4) 回傳 ScreenResult
    return ScreenResult{}
}

// Ways Game 算法 (目前可以先留空)
func (c *SpinCalculator) calcWaysGame(screen []uint8, Bet int) ScreenResult {
    // 之後再實作 Ways Game 算法
    // ...
    // 計算 TotalWin = Bet *
    return ScreenResult{}
}
```

`SlotGame` 這是對外的「遊戲」物件，之後 Free Game、Bonus Game、累積次數 功能就從這裡操作

```go=
// SlotGame 負責把「共用靜態資料 + 盤面生成 + 算分」包成一個對外介面。
// 對外只需要呼叫：
//     result := game.Spin()

type SlotGame struct {
    Init       *Init            // 共用靜態資訊（Rows/Cols/ReelStrips/Symbols/Lines/PayTable/Mode...）
    Generator  *ScreenGenerator // 產生隨機盤面
    Calculator *SpinCalculator  // 根據盤面計算得分（內部依 Mode 決定 Line/Ways 算法）

    Bet      int // 總下注
    NumLines int // 線數，只給 Line 模式用（len(Lines)）；Ways 模式可忽略或設 0
}

// NewSlotGame 建立一個可以直接「Spin」的遊戲物件。
func NewSlotGame(cfg *Config, seed int64, bet int) *SlotGame {
    // 1. 用 cfg 建立 Init，並做合法性檢查（Rows/Cols/reel 長度/符號索引/Lines/...）
    //    init, err := NewInit(cfg)
    //    if err != nil { ... }

    // 2. 用 Init 建立 ScreenGenerator（內部持有 Init，建立 rng、ScreenBuf）
    //    gen := NewScreenGenerator(init, seed)

    // 3. 用 Init 建立 SpinCalculator（內部持有 Init，依 Init.Mode 綁定 calcFn：
    //    - ModeLine → calcLineGame
    //    - ModeWays → calcWaysGame）
    //    calc := NewSpinCalculator(init)

    // 4. 如果是 Line 模式，計算 NumLines = len(init.Lines)，
    //    如果是 Ways 模式，NumLines 可設為 0 或忽略。
    //    numLines := 0
    //    if init.Mode == ModeLine {
    //        numLines = len(init.Lines)
    //    }

    // 5. 組合成 SlotGame 並回傳。
    //    return &SlotGame{
    //        Init:       init,
    //        Generator:  gen,
    //        Calculator: calc,
    //        Bet:        bet,
    //        NumLines:   numLines,
    //    }

    return nil // 計畫書階段先放佔位
}

// Spin 執行一次遊戲流程：產生盤面 + 算分，回傳結果。
func (g *SlotGame) Spin() ScreenResult {
    // 1. 呼叫 Generator.GenScreen() 取得一個隨機盤面（[]uint8, 長度=Rows*Cols）
    //    screen := g.Generator.GenScreen()

    // 2. 呼叫 Calculator.CalcScreen(screen, g.Bet)
    //    - 內部會依 calcFn 決定用 Line 算法或 Ways 算法
    //    - 回傳 ScreenResult（含 totalWin / lineResults / C1Count...）
    //    return g.Calculator.CalcScreen(screen, g.Bet)

    return ScreenResult{} // 計畫書階段先放佔位
}

```

`Simulator` struct 執行模擬

```go=
// Simulator 負責執行多輪模擬，並把每一把的結果丟給 Stat 做統計。
type Simulator struct {
    Game   *SlotGame // 遊戲物件（內含 Init / Generator / Calculator）
    Rounds int       // 要跑的模擬局數
}

// NewSimulator 建立一個模擬器，綁定遊戲與總局數。
func NewSimulator(game *SlotGame, rounds int) *Simulator {
    // 1. 檢查 game 是否為 nil（必要時回傳錯誤或 panic）
    // 2. 設定 Game 與 Rounds
    // 3. 回傳 *Simulator
    return nil
}

// Run 依照 Game 的 Mode (Line / Ways) 決定每把下注金額，
// 連續跑 Rounds 把，並將每把結果記錄到 Stat 物件中。
func (s *Simulator) Run(stat *Stat) *Stat {
    // 1. 如果呼叫端沒有傳入 Stat，就建立一個新的 Stat
    //    if stat == nil { stat = NewStat() }

    // 2. 依 Game.Init.Mode 決定「每把總下注金額」：
    //    switch s.Game.Init.Mode {
    //    case ModeLine:
    //        // ❗這邊應該不用 * s.Game.NumLines(剛剛改的)
    //        // Line 模式：單線下注 * 線數
    //        betPerSpin = float64(s.Game.Bet)
    //    case ModeWays:
    //        // Ways 模式：Bet 直接視為「每把總下注」
    //        betPerSpin = float64(s.Game.Bet)
    //    }

    // 3. 迴圈跑 s.Rounds 次：
    //    for i := 0; i < s.Rounds; i++ {
    //        3-1. 呼叫 s.Game.Spin() 取得一次 spin 的 ScreenResult
    //        3-2. 從 result 取出 TotalWin
    //        3-3. 呼叫 stat.Record(result.TotalWin, betPerSpin)
    //        3-4. （選用）若 i == 0，可呼叫某個 debug 函數印出第一把的盤面與得分細節
    //    }

    // 4. 回傳累積好統計數據的 stat
    return stat
}


```

`Stat` struct 統計物件（期望值、波動、標準差）

```go=
type Stat struct {
    SpinCount   int     // 模擬次數
    TotalBet    float64 // 總下注
    TotalWin    float64 // 總贏分
}

// NewStat 建立並回傳一個初始化的 Stat 物件
func NewStat() *Stat {
    // 所有欄位預設為 0
    return &Stat{}
}


func (s *Stat) Record(spinWin, spinBet float64) {
    // - 輸入本局贏分 spinWin、下注 spinBet
    // 計算 RTP
}


func (s *Stat) RTP() float64 {
    // RTP 回傳整體 RTP = TotalWin / TotalBet（若 TotalBet 為 0 則回傳 0）
    return 0
}
```

## 計劃書 v1 反饋

### Config、Init合併

```go
type Config struct {
    // ... // table value
    // ... // my value
    initFlag bool // 初始化旗標
}


func NewConfig(gameName enum) *Config {
    // 1. cfg := new(Config)
    // 2. 讀取設定檔 對Config 賦值
    // 3. cfg.Init()
    // return cfg
}

func (c *Config) Init() error {
    if cfg.initFlag {
        return nil
    }
    defer cfg.initFlag = true
    // 1. if err:= cfg.valid; err!=nil {...}
    // 2. 對cfg做預處理
    return nil
}

func (c *Config) Reset() {
    if cfg.initFlag {
        cfg.initFlag = false
    }
    cfg.Init()
}

func (c *Config) valid() error {

}
```

### ScreenGenerator

```go
type ScreenGenerator struct {
    // Init      *Init      // 共用靜態資訊
    Config *Config
    ScreenBuf []uint8    // 盤面緩衝區 (一維：長度 Rows*Cols)
    view [][]uint8 // 平時不寫，調用View的時候才修改回傳(避免重複創建)
    viewBySymbol [][]string // 平時不寫，調用ViewBySymbol的時候才修改回傳(避免重複創建)
    rng       *rand.Rand // 亂數生成器
}

// Rng由外部傳入才能保證用的是同一顆Rng
func NewScreenGenerator(init *Init, rng *Rng) *ScreenGenerator {
    sg := new(ScreenGenerator)
    // rng、初始化 ScreenBuf...
    return sg
}

// GenScreen 產生一個隨機盤面 (一維 []uint8, 每格是 symbolID)
func (g *ScreenGenerator) GenScreen() []uint8 {
    // 對每一軸：
    //   1) 隨機決定一個起始 index
    //   2) 連續取 Rows 個 symbolID
    //   3) 塞進 ScreenBuf
    return g.ScreenBuf
}

func (g *ScreenGenerator) View() [][]uint8 {
    // 把一維 ScreenBuf reshape 成 Rows x Cols (用 slice / index 計算) 塞進view
    return g.view
}

func (g *ScreenGenerator) ViewBySymbol() [][]string {
    // 把 ViewRowsCols() 的每個 symbolID 換成對應的 Symbols[name]
    return g.viewBySymbol
}
```

### ScreenCalculator

```go=
// calcFn 型別：給定盤面與 Bet
type CalcFunc func(screen []uint8, Bet int) *ScreenResult // <- 回傳指標

type SpinCalculator struct {
    Config *Config
    ScreenResult *ScreenResult // buf
    // ... inside values ...
    calcFn CalcFunc
    initflag // protect init behavior
}

func NewSpinCalculator(init *Init) *SpinCalculator {
    c := &SpinCalculator{Init: init}
    c.initCalcFunc()
    return c
}

// 維護一個map註冊表
var calcFnMap = map[Mode]CalcFunc{
    ModeLine: calcLineGame,
    ModeWays: calcWaysGame,
    // 註冊
}

// 綁定
func (c *SpinCalculator) initCalcFunc() {
    if fn, ok := calcFnMap[c.Init.Mode]; ok{
        c.calcFn = fn
        return
    }
    log.Fatal("未知 mode") // 無法對到就不能算分 設定檔失敗直接fatal 機台無法init完成
}



// 對外統一調用 CalcScreen：不管是 Line 還是 Ways，都呼叫 CalcScreen
func (c *SpinCalculator) CalcScreen(screen []uint8, Bet int) *ScreenResult {
    return c.calcFn(screen, Bet)
}

// ------- 下方是不同模式的內部實作 -------

// Lines Game 算法
func (c *SpinCalculator) CalcLineGame(screen []uint8, Bet int) *ScreenResult {
// 1) 計算 C1 數量
    // 2) 對每條線，用單一迴圈算 wildCount / symId / symCount / pay，累加 TotalLinePay
    // 3) TotalWin = TotalLinePay * Bet / 線數 (❗剛剛改的， Bet 是一次 spin 下注金額)
    // 4) 回傳 ScreenResult
    return c.ScreenResult
}

// Ways Game 算法
func (c *SpinCalculator) CalcWaysGame(screen []uint8, Bet int) *ScreenResult {
    // 之後再實作 Ways Game 算法
    return c.ScreenResult
}

```

![image](https://hackmd.io/_uploads/SyO14G_xbe.png)

## 計劃書 v2

### 結構

```go=
Config struct            // 遊戲靜態設定 (輪帶 / 符號 / 線表 / 賠率 / 模式…) 與合法性檢查
ScreenGenerator struct   // 生成隨機盤面 (spin)
LineResult struct        // 每條線的結果
ScreenResult struct      // 單一盤面的算分結果
SpinCalculator struct    // 計算一個盤面的得分 (支援 Line / Ways 模式)
runner func                // 執行模擬
```

### 注意事項

1. ScreenResult、LineResult 作為接收結果的資料結構
2. ==如果 `SpinCalculator` 需要兼容計算 way game 在不改變函數調用的狀態下==

- `Config` struct 定義模式。
- `SpinCalculator` struct 依據模式不同算分方法不同。

`Config` struct 負責處理遊戲不會變動的靜態設定與資料驗證，`initFlag` 用於處理初始化狀態。

這裡做了兩個函數(Init、Reset) 這個 Config struct 基本上只允許初始化一次，對設定檔做 read only 的操作。

<!--
為什麼 type GameMode int 不能直接是 int? -->

```go
type GameMode int

const (
    ModeLine GameMode = iota  // Line
    ModeWays                  // Ways
)

type Config struct {
    // table value
    ReelStrips [][]uint8    // 輪帶表 [Cols][reelLen]
    Symbols []string        // 符號清單
    Lines [][]int           // 線獎組合
    PayTable [][]int        // 賠率表 [symbolId][0..4] = 1~5 連賠率
    Rows int                // 盤面列數
    Cols int                // 盤面軸數
    Mode GameMode           // 算分模式 Lines / Ways (enum)

    // my value
    ScreenSize int          // Rows * Cols
    ReelLens   []int        // 每條輪帶長度（由 ReelStrips 衍生）

    // 初始化狀態
    initFlag bool // 初始化旗標
}


func NewConfig(gameName enum) *Config {
    // 1. cfg := new(Config)
    // 2. 讀取設定檔 對Config 賦值
    // 3. cfg.Init()
    // return cfg
}

func (c *Config) Init() error {
    if cfg.initFlag {
        return nil
    }
    defer cfg.initFlag = true
    // 1. if err:= cfg.valid; err!=nil {...}
    // 2. 對cfg做預處理
    return nil
}

func (c *Config) Reset() {
    if cfg.initFlag {
        cfg.initFlag = false
    }
    cfg.Init()
}

func (c *Config) valid() error {

}
```

<!--
``` go=
// 原本的 Valid 改成 receiver 是 *Init
func (i *Init) Valid() error {
    if i.Rows <= 0 {
        return fmt.Errorf("rows must > 0")
    }
    if i.Cols <= 0 {
        return fmt.Errorf("cols must > 0")
    }
    if len(i.ReelStrips) != i.Cols {
        return fmt.Errorf("reelStrips length must == Cols")
    }
    symLen := len(i.Symbols)

    for idx, reel := range i.ReelStrips {
        if len(reel) < i.Rows {
            return fmt.Errorf("reel %d length must >= rows", idx)
        }
        for _, s := range reel {
            if int(s) < 0 || int(s) >= symLen {
                return fmt.Errorf("reel %d has invalid symbol index %d", idx, s)
            }
        }
    }

    if len(i.Lines) > 0 {
        if len(i.Lines[0]) != i.Cols {
            return fmt.Errorf("each line length must == Cols")
        }
        for _, line := range i.Lines {
            for _, row := range line {
                if row < 0 || row >= i.Rows {
                    return fmt.Errorf("line has invalid row index %d", row)
                }
            }
        }
    }

    if len(i.PayTable) != symLen {
        return fmt.Errorf("payTable row must == symbol length")
    }
    for _, row := range i.PayTable {
        if len(row) != 5 {
            return fmt.Errorf("payTable col must == 5")
        }
    }
    return nil
}

``` -->

`ScreenGenerator` struct 負責生成隨機盤面(spin)，這裡 `rng` 由外部傳入，然後 view 跟 viewBySymbol 屬性用來儲存 `view` 和 `viewBySymbol` 方法處理後的值。(省配置、降 GC、零拷貝 reshape)`view` 和 `viewBySymbol` 方法需要 `return` 用於讓外部環境接收

```go
type ScreenGenerator struct {
    // Init      *Init      // 共用靜態資訊
    Config *Config
    ScreenBuf []uint8    // 盤面緩衝區 (一維：長度 Rows*Cols)
    view [][]uint8 // 平時不寫，調用View 方法的時候才修改回傳(避免重複創建)
    viewBySymbol [][]string // 平時不寫，調用ViewBySymbol 方法的時候才修改回傳(避免重複創建)
    rng       *rand.Rand // 亂數生成器
}

// Rng由外部傳入才能保證用的是同一顆Rng
func NewScreenGenerator(init *Init, rng *Rng) *ScreenGenerator {
    sg := new(ScreenGenerator)
    // rng、初始化 ScreenBuf...
    return sg
}

// GenScreen 產生一個隨機盤面 (一維 []uint8, 每格是 symbolID)
func (g *ScreenGenerator) GenScreen() []uint8 {
    // 對每一軸：
    //   1) 隨機決定一個起始 index
    //   2) 連續取 Rows 個 symbolID
    //   3) 塞進 ScreenBuf
    return g.ScreenBuf
}

func (g *ScreenGenerator) View() [][]uint8 {
    // 把一維 ScreenBuf reshape 成 Rows x Cols (用 slice / index 計算) 塞進view
    return g.view
}

func (g *ScreenGenerator) ViewBySymbol() [][]string {
    // 把 ViewRowsCols() 的每個 symbolID 換成對應的 Symbols[name]
    return g.viewBySymbol
}
```

`LineResult` 單條線的得分結果。

```go=
type LineResult struct {
    LineIndex int // 線號 (0-based)
    SymbolID  int // 中獎符號 ID；-1 表示沒中
    Count     int // 連線數
    Pay       int // 該線賠率 (尚未乘 line bet)
}
```

`ScreenResult` 一次盤面計算的結果。==有些參數放哪裡可能要想一下==

```go=
type ScreenResult struct {
    Screen       []uint8      // 原始盤面 (一維 symbolID)
    C1Count      int          // 盤面中 C1 (scatter) 出現次數
    LineResults  []LineResult // 每條線結果 (Line 模式用)
    TotalPay int              // 線獎賠率總和
    TotalWins     int         // 最終贏分 (TotalLinePay * lineBet)
    TotalBets                 // 累積總下注
}
```

`SpinCalculator` struct 在「給定一個盤面（screen）」的前提下，計算連線賠率 / C1，在這裡添加利用，回傳 `ScreenResult` struct ，另外這裡會受 `Config` struct 的影響採取不同的算賠率與算分方式 (前面注意事項第三點提到)

- CalcFunc 的返回指向 `ScreenResult` struct 對同一個 struct 做改值操作。
- 維護一個map註冊表，用來控制算分策略
- 如果有一天同時要使用兩種算分策略要怎麼搞? 那就把 `SpinCalculator` struct 利用 pointer 傳遞進 `CalcScreen` 函數中然後呼叫 `SpinCalculator` struct 的 `CalcLineGame` 函數跟 `CalcWaysGame` 函數。

==有些參數放哪裡可能要想一下==

```go=
// calcFn 型別：給定盤面與 Bet(一次 spin 下注金額)
type CalcFunc func(screen []uint8, Bet int) *ScreenResult // <- 回傳指標

type SpinCalculator struct {
    Config *Config                      // 指向 Config
    ScreenResult *ScreenResult          // buf

    // ... inside values ...
    calcFn CalcFunc                     // 真正執行算分的函數(依 Config.Mode 決定)
    initflag                            // protect init behavior
}

func NewSpinCalculator(init *Init) *SpinCalculator {
    c := &SpinCalculator{Init: init}
    c.initCalcFunc()
    return c
}

// 維護一個map註冊表
var calcFnMap = map[Mode]CalcFunc{
    ModeLine: calcLineGame,
    ModeWays: calcWaysGame,
    // 註冊
}

// 綁定
func (c *SpinCalculator) initCalcFunc() {
    if fn, ok := calcFnMap[c.Init.Mode]; ok{
        c.calcFn = fn
        return
    }
    log.Fatal("未知 mode") // 無法對到就不能算分 設定檔失敗直接fatal 機台無法init完成
}



// 對外統一調用 CalcScreen：不管是 Line 還是 Ways，都呼叫 CalcScreen
func (c *SpinCalculator) CalcScreen(screen []uint8, Bet int) *ScreenResult {
    return c.calcFn(screen, Bet)
}

// ------- 下方是不同模式的內部實作 -------

// Lines Game 算法
func (c *SpinCalculator) CalcLineGame(screen []uint8, Bet int) *ScreenResult {
// 1) 計算 C1 數量
    // 2) 對每條線，用單一迴圈算 wildCount / symId / symCount / pay，累加 TotalLinePay
    // 3) TotalWin = TotalLinePay * Bet / 線數 (❗剛剛改的， Bet 是一次 spin 下注金額)
    // 4) 回傳 ScreenResult
    return c.ScreenResult
}

// Ways Game 算法
func (c *SpinCalculator) CalcWaysGame(screen []uint8, Bet int) *ScreenResult {
    // 之後再實作 Ways Game 算法
    return c.ScreenResult
}
```

`runner` func 執行

<!-- // runner 做的事情：
// 1. 建立 Config（可以是硬編 or 從檔案讀取），並做初始化與驗證。
// 2. 建立亂數 rng。
// 3. 用 Config / Init 建立 ScreenGenerator、SpinCalculator。
// 4. 宣告統計用變數（總下注、總贏分、sum(r)、sum(r^2)）。
// 5. 迴圈跑 rounds 次：
//      a. 用 ScreenGenerator.GenScreen() 產生一個盤面。
//      b. 呼叫 SpinCalculator.CalcScreen(screen, bet) 得到 ScreenResult。
//      c. 把這一把的贏分 + 下注記錄進統計變數。
//      d. 第一把可以印 Debug：盤面 / 符號 / 每條線結果。
// 6. 迴圈結束後，用統計變數計算：
//      RTP = 總贏分 / 總下注
// 7. 印出統計結果。
 -->

```go=
func runner() {
    // 1. 建立 Config（靜態資料）

    // 2. 建立亂數
    // 3. 建立核心物件：
    //    gen  := NewScreenGenerator(cfg, rng)
    //    calc := NewSpinCalculator(cfg)

    // 5. 模擬迴圈：
    //    for i := 0; i < rounds; i++ {
    //        screen := gen.GenScreen()
    //        result := calc.CalcScreen(screen, betPerSpin)
    //
    //        win := float64(result.TotalWin)
    //        bet := float64(betPerSpin)
    //
    //        totalBet += bet
    //        totalWin += win
    //
    //        r := win / bet
    //
    //        if i == 0 {
    //            // 印第一把的 Debug：盤面 ID / Symbol / 各線結果...
    //        }
    //    }

    // 6. 計算統計值：
    // 7. 印出結果
}
```

## 實作 v1

上次討論完後簡化結構:

```go=
Config struct
ScreenGenerator struct
SpinCalculator struct
LineResult struct
ScreenResult struct
runner func
```

目前都在 `main` package，相關功能放在同一個檔案中。

#### config.go

`config` struct 處理讀取設定的動作

```go=
package main

import "errors"

// type SymbolID uint8 // 之後可以統一使用
type GameMode int

const (
 ModeUnknown GameMode = iota // 0 -> unknown
 ModeLines                   // 1 -> Line
 ModeWays                    // 2 -> Ways
)

// 輪帶表
var REELSTRIPS = [][]uint8{
 {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 2, 3, 4, 5, 6, 7, 8, 9, 10}, // 第 1 軸
 {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 2, 3, 4, 5, 6, 7, 8, 9, 10}, // 第 2 軸
 {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 2, 3, 4, 5, 6, 7, 8, 9, 10}, // 第 3 軸
 {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 2, 3, 4, 5, 6, 7, 8, 9, 10}, // 第 4 軸
 {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 2, 3, 4, 5, 6, 7, 8, 9, 10}, // 第 5 軸
}

// 11 個有效符號
var SYMBOLS = []string{"None", "C1", "W1", "H1", "H2", "H3", "H4", "L1", "L2", "L3", "L4", "L5"}

// 20 線路表
var LINES = [][]int{
 {1, 1, 1, 1, 1}, // 線路 1
 {0, 0, 0, 0, 0}, // 線路 2
 {2, 2, 2, 2, 2}, // ...
 {0, 1, 2, 1, 0},
 {2, 1, 0, 1, 2},
 {1, 0, 0, 0, 1},
 {1, 2, 2, 2, 1},
 {0, 0, 1, 2, 2},
 {2, 2, 1, 0, 0},
 {1, 0, 1, 2, 1},
 {1, 2, 1, 0, 1},
 {0, 1, 1, 1, 0},
 {2, 1, 1, 1, 2},
 {0, 1, 0, 1, 0},
 {2, 1, 2, 1, 2},
 {1, 1, 0, 1, 1},
 {1, 1, 2, 1, 1},
 {0, 0, 2, 0, 0},
 {2, 2, 0, 2, 2},
 {0, 2, 2, 2, 0}, // 線路 20
}

// 賠率表
var PAYTABLE = [][]int{
 {0, 0, 0, 0, 0},       // Z1
 {0, 0, 0, 0, 0},       // C1 (Scatter)
 {0, 0, 100, 200, 300}, // W1 (Wild)
 {0, 0, 10, 50, 200},   // H1
 {0, 0, 10, 50, 200},   // H2
 {0, 0, 10, 50, 200},   // H3
 {0, 0, 10, 50, 200},   // H4
 {0, 0, 5, 20, 100},    // L1
 {0, 0, 5, 20, 100},    // L2
 {0, 0, 5, 20, 100},    // L3
 {0, 0, 5, 20, 100},    // L4
 {0, 0, 5, 20, 100},    // L5
}

var ROWS, COLS int = 3, 5 // 列數, 行數

type Config struct {
 // 設定檔的數值
 ReelStrips [][]uint8 // 輪帶表
 Symbols    []string  // 符號清單
 Lines      [][]int   // 線獎組合
 Paytable   [][]int   // 賠率表
 Rows       int       // 列數
 Cols       int       // 軸數
 Mode       GameMode  // 算分模式(enum)

 // 輔助的數值
 ScreenSize int   // 盤面大小
 ReelLens   []int // 每一軸輪帶長度
 C1Id       uint8 // scatter 索引值
 W1Id       uint8 // wild 索引值
 minLen     int   // 最小連線長度

 // 初始化狀態
 initFlag bool // 初始化旗標

}

// 建構函數: 創建 instance 時調用
func NewConfig(reelStrips [][]uint8, symbols []string, lines [][]int, payTable [][]int, rows int, cols int, mode GameMode) (*Config, error) {
 // 1. 創建 Config instance & 賦值
 cfg := &Config{
  ReelStrips: reelStrips, // 輪帶表
  Symbols:    symbols,    // 符號清單
  Lines:      lines,      // 線路清單
  Paytable:   payTable,   // 賠率表
  Rows:       rows,       // 列數
  Cols:       cols,       // 行數
  minLen:     3,          // 最小連線長度
  Mode:       mode,       // 算分模式
 }

 // 2. 執行初始化
 if err := cfg.Init(); err != nil {
  return nil, err
 }
 // 3. 返回值, 錯誤訊息
 return cfg, nil

}

// 初始化方法
func (c *Config) Init() error {
 // 1. 先檢查 initFlag
 if c.initFlag {
  return nil
 }

 // 2. 執行設定檔驗證
 if err := c.validate(); err != nil {
  return err
 }

 // 3. 計算盤面大小、輪帶長度清單
 c.ScreenSize = c.Rows * c.Cols   // 盤面大小
 c.ReelLens = make([]int, c.Cols) // 輪帶長度清單
 for col := 0; col < c.Cols; col++ {
  c.ReelLens[col] = len(c.ReelStrips[col])
 }

 // 4. 找到特殊符號索引
 var i uint8 = 0
 for i < uint8(len(c.Symbols)) {
  if c.Symbols[i] == "C1" {
   c.C1Id = i
  }

  if c.Symbols[i] == "W1" {
   c.W1Id = i
  }

  i++
 }

 // 4. 更新初始化狀態
 c.initFlag = true
 return nil
}

func (c *Config) Reset() error {

 // 檢查 initFlag 狀態
 if !c.initFlag {
  return errors.New("not yet init")
 }

 // 重新初始化
 c.initFlag = false
 c.Init()

 return nil
}

func (c *Config) validate() error {

 // 1. Rows/Cols
 if c.Rows <= 0 {
  return errors.New("rows must > 0")
 }

 if c.Cols <= 0 {
  return errors.New("cols must > 0")
 }
 // 2. 輪帶
 if len(c.ReelStrips) != c.Cols {
  return errors.New("reelStrips length  must equal Cols")
 }

 // 3. 符號清單，這邊怪怪的感覺有很多例外
 symLen := len(c.Symbols)
 if symLen == 0 {
  return errors.New("symbols must not be empty")
 }

 // 4. Line Mode
 if c.Mode == ModeLines {
  if len(c.Lines) == 0 {
   return errors.New("line must not be emypt")
  }
 }

 if c.Mode == ModeWays {
  return errors.New("未實作")
 }

 // 5. PayTable： 每個符號 5 欄（1~5 連）
 if len(c.Paytable) != symLen {
  return errors.New("paytable size not correct")
 }

 // 6. 模式檢查
 // 這邊應該改成不存在於 GameMode enum 清單中，或是 =0
 if c.Mode != ModeLines && c.Mode != ModeWays {
  return errors.New("invalid mode")
 }

 return nil
}
```

#### screenGenerator.go

`screenGenerator` struct 生成一維陣列的盤面

```go=
package main

import "math/rand"

type ScreenGenerator struct {
 *Config              // 匿名嵌入 Config
 ScreenBuf []uint8    // 盤面緩存
 rng       *rand.Rand // RNG
}

// 建構函數: 創建 ScreenGenerator instance 時調用
func NewScreenGenerator(cfg *Config, rng *rand.Rand) *ScreenGenerator {

 // 創建 ScreenGenerator instance & 賦值
 return &ScreenGenerator{
  Config:    cfg,                           // 嵌入 Config
  ScreenBuf: make([]uint8, cfg.ScreenSize), // 盤面緩存
  rng:       rng,                           // RNG
 }
}

// 盤面生成
func (g *ScreenGenerator) GenScreen() []uint8 {

 // 對每一軸操作
 for i := 0; i < g.Cols; i++ {
  idx := g.rng.Intn(g.ReelLens[i])
  for j := 0; j < g.Rows; j++ {
   g.ScreenBuf[i*g.Rows+j] = g.ReelStrips[i][(idx+j)%g.ReelLens[i]]
  }
 }

 return g.ScreenBuf
}

```

#### spinCalculator.go

`spinCalculator` struct 根據 config Mode 選擇算分方法

```go=
package main

import (
 "log"
)

type LineResult struct {
 sym    uint8 // 符號 ID
 cnt    int   // 連線數量
 win    int   // 賠分
 lineId int   // 線路 ID
}

// 一次 spin 的結果
type ScreenResult struct {
 C1Win      int          // 盤面中 C1 (scatter) 出現次數
 Win        int          // 累積賠分
 LineResult []LineResult // 線路結果
}

// input SpinCalculator、screen 與 1 次 spin 下注分數
type CalcFunc func(*SpinCalculator, []uint8, int) *ScreenResult // 接收 *SpinCalculator

type SpinCalculator struct {
 *Config                // 匿名嵌入
 *ScreenResult          // 結果緩存
    calcFn    CalcFunc // 算分函數

 // 輔助參數
 filterIds []uint8 // 特殊符號
}

// 建構函數: 創建 NewSpinCalculator instance 時調用
func NewSpinCalculator(cfg *Config) *SpinCalculator {
 sc := &SpinCalculator{
  Config:       cfg,
  ScreenResult: &ScreenResult{},
 }
 sc.initCalcFn()
 sc.filterIds = deriveFilterIDs(cfg.Paytable, cfg.W1Id) // ← 自動算不計分符號
 return sc
}

// 選擇算分方式
func (s *SpinCalculator) initCalcFn() {

 // 選擇算分策略
 if fn, ok := calcFnMap[s.Mode]; ok {
  s.calcFn = fn // 選擇算分方式存到 s.calcFn

  return // 必要，不然會往外跳執行 log.Fatal("未知 mode")
 }
 log.Fatal("未知 mode")
 // panic 表示還有救，但這個沒救了(設定檔錯誤)，類似 try ... catch ...

}

// 不計分符號清單
func deriveFilterIDs(pay [][]int, wildID uint8) []uint8 {
 out := make([]uint8, 0, len(pay))
 for sid, row := range pay {
  allZero := true
  for _, p := range row {
   if p != 0 {
    allZero = false
    break
   }
  }
  if allZero && uint8(sid) != wildID {
   out = append(out, uint8(sid))
  }
 }
 return out
}

// 計算盤面中特定符號出現次數
func countSymbol(screen []uint8, id uint8) int {
 n := 0
 for _, v := range screen {
  if v == id {
   n++
  }
 }
 return n
}

// 判斷 slice 中是否包含某 uint8 元素
func containsU8(arr []uint8, x uint8) bool {
 for _, v := range arr {
  if v == x {
   return true
  }
 }
 return false
}

// 維護一個map註冊表
var calcFnMap = map[GameMode]CalcFunc{
 ModeLines: CalcLinesGame, // lines 算法
 ModeWays:  CalcWaysGame,  // ways 算法

}

// ------- 不同算分模式的內部函數 -------

// lines 算分模式
func CalcLinesGame(s *SpinCalculator, screen []uint8, bet int) *ScreenResult {

 // 初始化結果
 r := s.ScreenResult

 r.C1Win, r.Win = 0, 0
 linesLen := len(s.Lines)                       // 線路數量
 r.LineResult = make([]LineResult, 0, linesLen) // 清空線路結果

 totalLinePay := 0 // 累積線路賠分

 // 計算 C1 出現次數
 r.C1Win = countSymbol(screen, s.C1Id)

 // 逐條線計分
 for i := 0; i < linesLen; i++ {
  // 單條線的狀態
  wildCount := 0
  wildContinue := true

  var symId uint8     // 得分符號ID
  symStarted := false // 是否已確定得分符號
  symCount := 0       // 符號連線數量
  pendingWilds := 0   // 在算得分符號連線時先算前面累積的 W1 數量，如果後面遇到得分符號就加進去

  // 從左到右掃這條線
  for j := 0; j < s.Cols; j++ {

   // 1. 獲取該位置符號
   sid := screen[j*s.Rows+s.Lines[i][j]]

   // 2. 開頭連續 Wild 數
   if wildContinue && sid == s.W1Id {
    wildCount++
   } else {
    wildContinue = false
   }

   // 3. 計算得分符號連線

   // 3.1. 尚未決定得分符號
   if !symStarted {
    if sid == s.W1Id {
     pendingWilds++ // 預先累積 Wild ，後面可能會替代為得分符號
     continue
    }
    // 第一個非 Wild：若是不計分符號（Z1/C1 等），此線只能靠純 Wild
    if containsU8(s.filterIds, sid) {
     break
    }
    // 合法得分符號確立
    symId = sid
    symStarted = true
    symCount = pendingWilds + 1
    continue
   }

   // 3.2. 已決定得分符號，延伸連線：同符號或 Wild 都可
   if sid == symId || sid == s.W1Id {
    symCount++
   } else {
    break // 如果開頭直接是 C1 直接結束
   }
  }

  // 4. 未達最小連線長度 → 0 分 該條線沒中
  if symCount < s.minLen && wildCount < s.minLen {
   r.LineResult = append(r.LineResult, LineResult{
    sym:    0, // 無得分
    cnt:    0,
    win:    0,
    lineId: i,
   }) // 更新結果
   continue
  }

  // 5. 計算兩種賠率

  // 5.1. 得分符號賠率
  symPay := 0
  if symStarted && symCount >= s.minLen { // 只做「是否該算」的必要判斷
   symPay = s.Paytable[int(symId)][symCount-1]
  }

  // 5.2.Wild 賠率

  wildPay := 0 // W1 賠率
  if wildCount >= s.minLen {
   wildPay = s.Paytable[int(s.W1Id)][wildCount-1]
  }

  // 6. 取較大者
  winSym := symId
  winCnt := symCount
  winPay := symPay

  if wildPay > symPay {
   winSym = s.W1Id
   winCnt = wildCount
   winPay = wildPay
  }

  // 7. 更新結果
  totalLinePay += winPay
  r.LineResult = append(r.LineResult, LineResult{
   sym:    winSym, // 得分符號
   cnt:    winCnt, // 連線數量
   win:    winPay, // 賠分
   lineId: i,      // 線路 ID
  }) // 更新結果
 }

 // 一次 spin 盤面得結果
 r.Win = totalLinePay * bet / linesLen // 總賠分
 return r
}

// ways 算分模式
func CalcWaysGame(s *SpinCalculator, screen []uint8, bet int) *ScreenResult {
 // 未實做
 return s.ScreenResult
}
```

#### runner.go

`runner` func 執行

```go=
package main

import (
 "fmt"
 "math/rand"
 "time"
)

func runner() error {

 // 1. 創建 Config 實例
 cfg, err := NewConfig(REELSTRIPS, SYMBOLS, LINES, PAYTABLE, ROWS, COLS, ModeLines)
 // 錯誤檢查
 if err != nil {
  return err
 }

 // 2. 建立亂數生成
 randSeed := rand.NewSource(123456789) // 固定 randSeed
 // randSeed := rand.NewSource(time.Now().UnixNano())
 rng := rand.New(randSeed) // 返回 pointer

 // 3. 建立 生成盤面、算分實例
 sg := NewScreenGenerator(cfg, rng)
 sc := NewSpinCalculator(cfg)

 // 4. 初始化模擬參數
 rounds := 1_000_000 // 模擬次數
 bet := 1000         // Bet: 一次 spin 下注分數
 totalBet := 0
 totalWin := 0
 start := time.Now() // 起始時間

 // 5. 執行模擬
 for i := 0; i < rounds; i++ {
  // 執行模擬
  screen := sg.GenScreen()
  result := sc.calcFn(sc, screen, bet)
  // fmt.Println("Result:", result)

  // 更新狀態
  totalBet += bet        // 總下注
  totalWin += result.Win // 總贏分

  // 顯示進度
        if (i+1)%100000 == 0 {
   fmt.Printf("Completed %d spins...\n", i+1)
  }
 }

 if totalBet == 0 {
  return nil
 }

 elapsed := time.Since(start)

 fmt.Printf("Elapsed time: %.6f seconds\n", elapsed.Seconds())

 // 6. 計算統計值
 rtp := float64(totalWin) / float64(totalBet)
 fmt.Printf("TotalBet=%d TotalWin=%d RTP=%.6f\n", totalBet, totalWin, rtp)
 return nil

}
```

最後在 `main` func 呼叫 `runner` func 執行模擬。

## 實作 v1 反饋

1. 整體結構良好，運算邏輯正確且清晰高效
2. 避免熱點運算中新建物件或即時運算不需浪費時間運算的內容

```go=

func CalcLinesGame(...) {
    // r.LineResult = make([]LineResult, 0, linesLen) // 清空線路結果
    r.LineResult = r.LineResult[:0] // 清空邏輯長度，保留原指針與空間
}
```

1. 走線表轉換slice of slice 2D -> 1D 　`screen[s.FlatLines[i*s.Cols+j]]`，並預先建立走線表空間

```go=

// ------- Config -------

type Config struct {
 // ... Other Data ...
 Lines      [][]int   // 線獎組合

 // 輔助的數值
 FlatLines  []int // 平坦化線路清單
}

func (c *Config) Init() {
    // ... Other Things ...
    // 平坦化線路清單
 c.FlatLines = make([]int, len(c.Lines)*c.Cols)
 for i, line := range c.Lines {
  for j, pos := range line {
   c.FlatLines[i*c.Cols+j] = j*c.Rows + pos
  }
 }
}

// ------- Calc -------

func NewSpinCalculator(cfg *Config) *SpinCalculator {
 sc := &SpinCalculator{
  cfg:       cfg,
  ScreenResult: &ScreenResult{},
 }
 sc.initCalcFn()

    // 預先建立走線表空間
    sc.ScreenResult.LineResult = make([]LineResult, 0, len(cfg.Lines))
    return sc
}



func CalcLinesGame(...) {
    // ...
    for i := 0; i < linesLen; i++ {
        // ...
        for j := 0; j < s.Cols; j++ {
            // 1. 獲取該位置符號
            sid := screen[s.FlatLines[i*s.Cols+j]]
            // ...
        }
    }
}

```

1. 匿名嵌入會有變數遮蔽問題，盡量不用

```go=
type SpinCalculator struct {
 cfg *Config                // 設定檔：不使用匿名嵌入
 sr *ScreenResult          // 結果緩存：不使用匿名嵌入
 calcFn        CalcFunc // 算分函數

 // 輔助參數
 filterIds []uint8 // 特殊符號
}

```

1. 不計分符號使用bitmask : 影響較小 (從原來O(n) -> O(1) 判斷，影響較小是因為一條線只會檢查最多1次)(比較不直覺，可以之後再學著應用)

```go=
type SpinCalculator struct {
 cfg *Config                // 設定檔：不使用匿名嵌入
 sr *ScreenResult          // 結果緩存：不使用匿名嵌入
 calcFn        CalcFunc // 算分函數

 // 輔助參數
 filter uint64
}

// 不計分符號清單
func deriveFilter(pay [][]int, wildID uint8) uint64 {
 out := uint64(0) // 0x00000000000000
 for sid, row := range pay {
  allZero := true
  for _, p := range row {
   if p != 0 {
    allZero = false
    break
   }
  }
  if allZero && uint8(sid) != wildID {
   out |= 1 << uint64(sid)
  }
 }
 return out
}

func NewSpinCalculator(cfg *Config) *SpinCalculator {
 sc := &SpinCalculator{
  cfg:       cfg,
  sr: &ScreenResult{},
 }
 sc.initCalcFn()

    // 預先建立走線表空間
    sc.ScreenResult.LineResult = make([]LineResult, 0, len(cfg.Lines))

    // 使用bitmask判斷是否得分符號
    sc.filter = deriveFilter(cfg.Paytable, cfg.W1Id)
    return sc
}


func CalcLinesGame(...) {
    // ...
    for i := 0; i < linesLen; i++ {
        // ...
        for j := 0; j < s.Cols; j++ {
            // 1. 獲取該位置符號
            sid := screen[s.FlatLines[i*s.Cols+j]]
            // 2. 開頭連續 Wild 數
            // 3.1. 尚未決定得分符號
            if !symStarted {
                // sid != wild
                if s.filter&(1<<uint64(sid)) != 0 { // bitmask 操作
                    break
                }
                symId = sid
                symStarted = true
                symCount = wildCount+1
                continue
            }
            // 3.2. 已決定得分符號，延伸連線：同符號或 Wild 都可
            // ...
        }
    }
}

```

1. 建議：只傳必要的贏分結果

```go=
func CalcLinesGame(...) {
    // ...
    // 4. 未達最小連線長度 → 0 分 該條線沒中
    if symCount < s.minLen && wildCount < s.minLen {
        continue
    }
    // ...
}

```

1. 若要將LineResult擴增為通用算分細項(只包含基本算分結果)

```go=

type ScreenResult struct {
    C1Win      int          // 盤面中 C1 (scatter) 出現次數
    Win        int          // 累積賠分
    Mode       GameMode     // 算分模式
    WinDetails []WinDetail  // 細項
}

// 細項
type WinDetail {
    win    int     // 得分
    symbol uint8   // 得分圖標
    hitmap []bool  // 中獎圖

    lineId int     // 得分線 (Line)
    length int     // 長度 (Line Way)
    comb   int     // 組合數 (Way)
    cnt    int     // 數量(Cluster Count)
}
```

## 實作 v2

### config.go

```go=
package main

import "errors"

// type SymbolID uint8 // 之後可以統一使用
type GameMode int

const (
 ModeUnknown GameMode = iota // 0 -> unknown
 ModeLines                   // 1 -> Line
 ModeWays                    // 2 -> Ways
)

// 輪帶表
var REELSTRIPS = [][]uint8{
 {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 2, 3, 4, 5, 6, 7, 8, 9, 10}, // 第 1 軸
 {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 2, 3, 4, 5, 6, 7, 8, 9, 10}, // 第 2 軸
 {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 2, 3, 4, 5, 6, 7, 8, 9, 10}, // 第 3 軸
 {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 2, 3, 4, 5, 6, 7, 8, 9, 10}, // 第 4 軸
 {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 2, 3, 4, 5, 6, 7, 8, 9, 10}, // 第 5 軸
}

// 11 個有效符號
var SYMBOLS = []string{"None", "C1", "W1", "H1", "H2", "H3", "H4", "L1", "L2", "L3", "L4", "L5"}

// 20 線路表
var LINES = [][]int{
 {1, 1, 1, 1, 1}, // 線路 1
 {0, 0, 0, 0, 0}, // 線路 2
 {2, 2, 2, 2, 2}, // ...
 {0, 1, 2, 1, 0},
 {2, 1, 0, 1, 2},
 {1, 0, 0, 0, 1},
 {1, 2, 2, 2, 1},
 {0, 0, 1, 2, 2},
 {2, 2, 1, 0, 0},
 {1, 0, 1, 2, 1},
 {1, 2, 1, 0, 1},
 {0, 1, 1, 1, 0},
 {2, 1, 1, 1, 2},
 {0, 1, 0, 1, 0},
 {2, 1, 2, 1, 2},
 {1, 1, 0, 1, 1},
 {1, 1, 2, 1, 1},
 {0, 0, 2, 0, 0},
 {2, 2, 0, 2, 2},
 {0, 2, 2, 2, 0}, // 線路 20
}

// 賠率表
var PAYTABLE = [][]int{
 {0, 0, 0, 0, 0},       // Z1
 {0, 0, 0, 0, 0},       // C1 (Scatter)
 {0, 0, 100, 200, 300}, // W1 (Wild)
 {0, 0, 10, 50, 200},   // H1
 {0, 0, 10, 50, 200},   // H2
 {0, 0, 10, 50, 200},   // H3
 {0, 0, 10, 50, 200},   // H4
 {0, 0, 5, 20, 100},    // L1
 {0, 0, 5, 20, 100},    // L2
 {0, 0, 5, 20, 100},    // L3
 {0, 0, 5, 20, 100},    // L4
 {0, 0, 5, 20, 100},    // L5
}

var ROWS, COLS int = 3, 5 // 列數, 行數

type Config struct {
 // 設定檔的數值
 ReelStrips [][]uint8 // 輪帶表
 Symbols    []string  // 符號清單
 Lines      [][]int   // 線獎組合
 Paytable   [][]int   // 賠率表
 Rows       int       // 列數
 Cols       int       // 軸數
 Mode       GameMode  // 算分模式(enum)

 // 輔助的數值
 ScreenSize int   // 盤面大小
 ReelLens   []int // 每一軸輪帶長度
 C1Id       uint8 // scatter 索引值
 W1Id       uint8 // wild 索引值
 minLen     int   // 最小連線長度
 FlatLines  []int // 平坦化線路清單

 // 初始化狀態
 initFlag bool // 初始化旗標

}

// 建構函數: 創建 instance 時調用
func NewConfig(reelStrips [][]uint8, symbols []string, lines [][]int, payTable [][]int, rows int, cols int, mode GameMode) (*Config, error) {
 // 1. 創建 Config instance & 賦值
 cfg := &Config{
  ReelStrips: reelStrips, // 輪帶表
  Symbols:    symbols,    // 符號清單
  Lines:      lines,      // 線路清單
  Paytable:   payTable,   // 賠率表
  Rows:       rows,       // 列數
  Cols:       cols,       // 行數
  minLen:     3,          // 最小連線長度
  Mode:       mode,       // 算分模式
 }

 // 2. 執行初始化
 if err := cfg.Init(); err != nil {
  return nil, err
 }
 // 3. 返回值, 錯誤訊息
 return cfg, nil

}

// 初始化方法
func (c *Config) Init() error {
 // 1. 先檢查 initFlag
 if c.initFlag {
  return nil
 }

 // 2. 執行設定檔驗證
 if err := c.validate(); err != nil {
  return err
 }

 // 3. 計算盤面大小、輪帶長度清單
 c.ScreenSize = c.Rows * c.Cols   // 盤面大小
 c.ReelLens = make([]int, c.Cols) // 輪帶長度清單
 for col := 0; col < c.Cols; col++ {
  c.ReelLens[col] = len(c.ReelStrips[col])
 }

 // 4. 找到特殊符號索引
 var i uint8 = 0
 for i < uint8(len(c.Symbols)) {
  if c.Symbols[i] == "C1" {
   c.C1Id = i
  }

  if c.Symbols[i] == "W1" {
   c.W1Id = i
  }

  i++
 }

 // 5. 平坦化線路清單
 c.FlatLines = make([]int, len(c.Lines)*c.Cols)
 for i, line := range c.Lines {
  for j, pos := range line {
   c.FlatLines[i*c.Cols+j] = j*c.Rows + pos
  }
 }

 // 6. 更新初始化狀態
 c.initFlag = true
 return nil
}

func (c *Config) Reset() error {

 // 檢查 initFlag 狀態
 if !c.initFlag {
  return errors.New("not yet init")
 }

 // 重新初始化
 c.initFlag = false
 c.Init()

 return nil
}

func (c *Config) validate() error {

 // 1. Rows/Cols
 if c.Rows <= 0 {
  return errors.New("rows must > 0")
 }

 if c.Cols <= 0 {
  return errors.New("cols must > 0")
 }
 // 2. 輪帶
 if len(c.ReelStrips) != c.Cols {
  return errors.New("reelStrips length  must equal Cols")
 }

 // 3. 符號清單，這邊怪怪的感覺有很多例外
 symLen := len(c.Symbols)
 if symLen == 0 {
  return errors.New("symbols must not be empty")
 }

 // 4. Line Mode
 if c.Mode == ModeLines {
  if len(c.Lines) == 0 {
   return errors.New("line must not be emypt")
  }
 }

 if c.Mode == ModeWays {
  return errors.New("未實作")
 }

 // 5. PayTable： 每個符號 5 欄（1~5 連）
 if len(c.Paytable) != symLen {
  return errors.New("paytable size not correct")
 }

 // 6. 模式檢查
 // 這邊應該改成不存在於 GameMode enum 清單中，或是 =0
 if c.Mode != ModeLines && c.Mode != ModeWays {
  return errors.New("invalid mode")
 }

 return nil
}


```

### runner.go

```go=
package main

import (
 "fmt"
 "math/rand"
 "time"
)

func runner() error {

 // 1. 創建 Config 實例
 cfg, err := NewConfig(REELSTRIPS, SYMBOLS, LINES, PAYTABLE, ROWS, COLS, ModeLines)

 // 錯誤檢查
 if err != nil {
  return err
 }

 // 2. 建立亂數生成
 randSeed := rand.NewSource(123456789) // 固定 randSeed
 // randSeed := rand.NewSource(time.Now().UnixNano())
 rng := rand.New(randSeed) // 返回 pointer

 // 3. 建立 生成盤面、算分實例
 sg := NewScreenGenerator(cfg, rng)
 sc := NewSpinCalculator(cfg)

 // 4. 初始化模擬參數
 rounds := 1_000_000_0 // 模擬次數
 bet := 1000           // Bet: 一次 spin 下注分數
 totalBet := 0
 totalWin := 0
 start := time.Now() // 起始時間

 // 5. 執行模擬
 for i := 0; i < rounds; i++ {
  // 執行模擬
  screen := sg.GenScreen()
  result := sc.calcFn(sc, screen, bet)

  // 更新狀態
  totalBet += bet        // 總下注
  totalWin += result.Win // 總贏分

  // // 顯示進度
  // if (i+1)%100000 == 0 {
  //  fmt.Printf("Completed %d spins...\n", i+1)
  // }
 }

 if totalBet == 0 {
  return nil
 }

 elapsed := time.Since(start)

 fmt.Printf("Elapsed time: %.6f seconds\n", elapsed.Seconds())

 // 6. 計算統計值
 rtp := float64(totalWin) / float64(totalBet)
 fmt.Printf("TotalBet=%d TotalWin=%d RTP=%.6f\n", totalBet, totalWin, rtp)
 return nil

}
```

### screenGenerator.go

```go=
package main

import "math/rand"

type ScreenGenerator struct {
 *Config              // 匿名嵌入 Config
 ScreenBuf []uint8    // 盤面緩存
 rng       *rand.Rand // RNG
}

// 建構函數: 創建 ScreenGenerator instance 時調用
func NewScreenGenerator(cfg *Config, rng *rand.Rand) *ScreenGenerator {

 // 創建 ScreenGenerator instance & 賦值
 return &ScreenGenerator{
  Config:    cfg,                           // 嵌入 Config
  ScreenBuf: make([]uint8, cfg.ScreenSize), // 盤面緩存
  rng:       rng,                           // RNG
 }
}

// 盤面生成
func (g *ScreenGenerator) GenScreen() []uint8 {

 // 對每一軸操作
 for i := 0; i < g.Cols; i++ {
  idx := g.rng.Intn(g.ReelLens[i])
  for j := 0; j < g.Rows; j++ {
   g.ScreenBuf[i*g.Rows+j] = g.ReelStrips[i][(idx+j)%g.ReelLens[i]]
  }
 }

 return g.ScreenBuf
}

```

### spinCalculator.go

```go=
package main

import (
 "log"
)

// 細項
type WinDetail struct {
 win    int    // 得分
 symbol uint8  // 得分圖標
 hitmap []bool // 中獎圖

 lineId int // 得分線 (Line)
 length int // 長度 (Line Way)
 comb   int // 組合數 (Way)
 cnt    int // 數量(Cluster Count)
}

// 一次 spin 的結果
type ScreenResult struct {
 C1Win      int         // 盤面中 C1 (scatter) 出現次數
 Win        int         // 累積賠分
 Mode       GameMode    // 算分模式
 WinDetails []WinDetail // 細項
}

// input SpinCalculator、screen 與 1 次 spin 下注分數
type CalcFunc func(*SpinCalculator, []uint8, int) *ScreenResult // 接收 *SpinCalculator

type SpinCalculator struct {
 cfg    *Config       // 匿名嵌入
 sr     *ScreenResult // 結果緩存
 calcFn CalcFunc      // 算分函數

 // 輔助參數
 filter uint64 // 特殊符號
}

// 不計分符號清單
func deriveFilter(pay [][]int, wildID uint8) uint64 {
 out := uint64(0) // 0x00000000000000
 for sid, row := range pay {
  allZero := true
  for _, p := range row {
   if p != 0 {
    allZero = false
    break
   }
  }
  if allZero && uint8(sid) != wildID {
   out |= 1 << uint64(sid)
  }
 }
 return out
}

// 建構函數: 創建 NewSpinCalculator instance 時調用
func NewSpinCalculator(cfg *Config) *SpinCalculator {
 sc := &SpinCalculator{
  cfg: cfg,
  sr:  &ScreenResult{},
 }
 sc.initCalcFn()

 // 預先建立走線表空間
 sc.sr.WinDetails = make([]WinDetail, 0, len(cfg.Lines))

 // 使用bitmask判斷是否得分符號
 sc.filter = deriveFilter(cfg.Paytable, cfg.W1Id)
 return sc
}

// 選擇算分方式
func (s *SpinCalculator) initCalcFn() {

 // 選擇算分策略
 if fn, ok := calcFnMap[s.cfg.Mode]; ok {
  s.calcFn = fn // 選擇算分方式存到 s.calcFn

  return // 必要，不然會往外跳執行 log.Fatal("未知 mode")
 }
 log.Fatal("未知 mode")
 // panic 表示還有救，但這個沒救了(設定檔錯誤)，類似 try ... catch ...

}

// 計算盤面中特定符號出現次數
func countSymbol(screen []uint8, id uint8) int {
 n := 0
 for _, v := range screen {
  if v == id {
   n++
  }
 }
 return n
}

// 維護一個map註冊表
var calcFnMap = map[GameMode]CalcFunc{
 ModeLines: CalcLinesGame, // lines 算法
 ModeWays:  CalcWaysGame,  // ways 算法

}

// ------- 不同算分模式的內部函數 -------

// lines 算分模式
func CalcLinesGame(s *SpinCalculator, screen []uint8, bet int) *ScreenResult {

 // 初始化結果
 r := s.sr

 r.C1Win, r.Win = 0, 0
 linesLen := len(s.cfg.Lines)    // 線路數量
 r.WinDetails = r.WinDetails[:0] // 清空邏輯長度，保留原指針與空間

 totalLinePay := 0 // 累積線路賠分

 // 計算 C1 出現次數
 r.C1Win = countSymbol(screen, s.cfg.C1Id)

 // 逐條線計分
 for i := 0; i < linesLen; i++ {
  // 單條線的狀態
  wildCount := 0
  wildContinue := true

  var symId uint8     // 得分符號ID
  symStarted := false // 是否已確定得分符號
  symCount := 0       // 符號連線數量

  // 從左到右掃這條線
  for j := 0; j < s.cfg.Cols; j++ {

   // 1. 獲取該位置符號
   sid := screen[s.cfg.FlatLines[i*s.cfg.Cols+j]] // 平坦化線路清單

   // 2. 開頭連續 Wild 數
   if wildContinue && sid == s.cfg.W1Id {
    wildCount++
   } else {
    wildContinue = false
   }

   // 3. 計算得分符號連線

   // 3.1. 尚未決定得分符號
   if !symStarted {
    if sid == s.cfg.W1Id {
     continue
    }
    // 第一個非 Wild：若是不計分符號（Z1/C1 等），此線只能靠純 Wild
    if s.filter&(1<<uint64(sid)) != 0 {
     break
    }
    // 合法得分符號確立
    symId = sid
    symStarted = true
    symCount = wildCount + 1 // 包含前面的 Wild
    continue
   }

   // 3.2. 已決定得分符號，延伸連線：同符號或 Wild 都可
   if sid == symId || sid == s.cfg.W1Id {
    symCount++
   } else {
    break // 如果開頭直接是 C1 直接結束
   }
  }

  // 4. 未達最小連線長度 → 0 分 該條線沒中
  if symCount < s.cfg.minLen && wildCount < s.cfg.minLen {
   continue
  }

  // 5. 計算兩種賠率

  // 5.1. 得分符號賠率
  symPay := 0
  if symStarted && symCount >= s.cfg.minLen { // 只做「是否該算」的必要判斷
   symPay = s.cfg.Paytable[int(symId)][symCount-1]
  }

  // 5.2.Wild 賠率

  wildPay := 0 // W1 賠率
  if wildCount >= s.cfg.minLen {
   wildPay = s.cfg.Paytable[int(s.cfg.W1Id)][wildCount-1]
  }

  // 6. 取較大者
  winSym := symId
  winCnt := symCount
  winPay := symPay

  if wildPay > symPay {
   winSym = s.cfg.W1Id
   winCnt = wildCount
   winPay = wildPay
  }

  // 7. 更新結果
  totalLinePay += winPay
  r.WinDetails = append(r.WinDetails, WinDetail{
   symbol: winSym, // 得分符號
   cnt:    winCnt, // 連線數量
   win:    winPay, // 賠分
   lineId: i,      // 線路 ID
  }) // 更新結果
 }

 // 一次 spin 盤面得結果
 r.Win = totalLinePay * bet / linesLen // 總賠分
 return r
}

// ways 算分模式
func CalcWaysGame(s *SpinCalculator, screen []uint8, bet int) *ScreenResult {
 // 未實做
 return s.sr
}
```

## 筆記

1. "熱點運算" 要注意如果是靜態值比如說固定值的變數就不要在熱點運算的路徑上處理因為會出現重複計算相同值的情況。所以 如果在 `CalcLinesGame` func 中使用 `make([]LineResult, 0, linesLen)` 並且 `linesLen>0` 就會==建立一個新的底層陣列==。> `make([]T, 0, C)` : 建立一個長度 0、容量 C 的新切片

        唯一不會有底層陣列的情況 `linesLen == 0`
        這時 make([]T, 0, 0) 會產生一個長度 0、容量 0 的切片，底層指標為 nil （但切片本身不是 nil）所以利用以下作法==清空邏輯長度，保留原指針與空間==
        > r.LineResult[:0]

        當 slice 長度超過 cap 時，會觸發擴容
        r.LineResult = make([]LineResult, 0, 0) 會等於 r.LineResult = r.LineResult[:0] 嗎? 不等於。

    ![image](https://hackmd.io/_uploads/SJcwi8Kx-l.png)

2. `走線表轉換 slice of slice 2D -> 1D 　screen[s.FlatLines[i*s.Cols+j]]，並預先建立走線表空間` 將 2 維走線索引表儲存成 1 維索引表。

![image](https://hackmd.io/_uploads/rkTg7wFxWx.png)

```
Line: [1 1 1 1 1]
i: 0
FlatLines[0]=1
FlatLines[1]=4
FlatLines[2]=7
FlatLines[3]=10
FlatLines[4]=13
Line: [0 0 0 0 0]

Line: [0 0 0 0 0]
i: 1
FlatLines[5]=0
FlatLines[6]=3
FlatLines[7]=6
FlatLines[8]=9
FlatLines[9]=12
```

調用的時候，`screen` 本身就已經是 1 維的了。所以獲取該位置符號值用:

```
sid := screen[s.cfg.FlatLines[i*s.cfg.Cols+j]] // 平坦化線路清單
```

第 i 條路線，第 j 軸的索引。s.cfg.Cols 是 5 的情況下，就會每 5 格一組。如同上面

1. 變數遮蔽

```go=
type Config struct{ Rows int }
type ScreenResult struct{ Win int }

type SpinCalculator struct {
    *Config        // 匿名嵌入：Rows 被提升
    *ScreenResult  // 匿名嵌入：Win 被提升
    Rows int       // ← 外層定義了同名欄位
}

func f(s *SpinCalculator) {
    s.Rows = 5          // 寫到外層的 Rows（遮蔽 Config.Rows）
    s.Config.Rows = 10  // 只有這樣才是改到 Config.Rows
}
```

除此之外，也可能出現多`重嵌入同名` 的問題

```go=
type C1 struct{ Rows int }
type C2 struct{ Rows int }

type S struct {
    *C1
    *C2
}

func g(s *S) {
    _ = s.Rows   // ❌ 編譯錯：ambiguous selector: Rows
}

```

1. ==不計分符號使用 bitmask==

## 參考連結

- [生成盤面](https://hackmd.io/@chiSean/r1koA2y1bx)
- [github repo](https://github.com/cgit6/go_slot)
- [實作筆記](https://hackmd.io/@chiSean/Hy1Z5MQeWl)
- [PARsheet](https://docs.google.com/spreadsheets/d/1WncTL93uOFgXVq_zC1yJQky_ZsAkpolA5LZoVFo4OuE/edit?usp=sharing)
