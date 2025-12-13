
## 建立遊戲邏輯

需要滿足以下條件
```
1. BG 50~65% RTP
2. 得分率介於 30%~40%
3. FG 平均約 120 轉左右左右觸發一次
4. FG 中要有破千倍的得分
5. 總體 RTP 介於 96%~97%
6. CV 大於 9
```

### 結果
執行 `make run GAME=DemoLine SPINS=100000000 MODE=0` 模擬結果
理論值詳見 [excel](https://docs.google.com/spreadsheets/d/1ZZUYusikSiQDiVpgFvjWn6BTJfpeQmHp8YFo_HBsEkw/edit?usp=sharing)
``` 
+--------------------------------+
|            Summary             |
+--------------+-----------------+
| Game Name    | DemoLine        |
| Total Rounds | 100,000,000     |
| Total RTP    | 97.00 %         |
| RTP 95% CI   | [96.82%,97.18%] |
| Total Bet    | 2,000,000,000   |
| Total Win    | 1,940,048,517   |
| Base Win     | 1,259,368,800   |
| Free Win     | 680,679,717     |
| Win Counts   | 30,375,292      |
| Trigger      | 856,596         |
| STD          | 9.248           |
| CV           | 9.534           |
+--------------+-----------------+
```

configs/game_2_demoline.yaml
設定檔
```yaml=
# [文件網址] None
# [玩法說明] None

# 遊戲設定
GameSetting:
    
    # 遊戲名稱 : 2 | DemoLine | 基本遊戲範例
    GameName: DemoLine
    
    # 押注基本單位
    BetUnit : [20]
    
    # 最大贏分(對應BetUnit)
    MaxWinLimit : 4000000
    
    # 遊戲模式設定列表，一個遊戲模式相當於一個狀態，遊戲將在各狀態間轉換
    GameModeSettingList:
        - # GameModeSetting : BaseGame 設定
          # 盤面設定
          ScreenSetting:
              columns: 5
              rows: 3
              damp: 1
          # 生成盤面設定
          GenScreenSetting:
              GenReelType: GenReelByReelIdx
              ReelStripsGroup:  
                  - # ReelStrip[0]
                    weight : 1
                    reels :
                        - # Reel[0] 
                          symbols : [6, 10, 7, 5, 9, 7, 6, 10, 9, 4, 8, 10, 1, 9, 10, 2, 8, 7, 4, 8, 3, 9, 6, 9, 6, 10, 3, 9, 5, 10]
                          weights : [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
                        - # Reel[1]
                          symbols : [10, 7, 5, 8, 7, 2, 9, 10, 6, 8, 9, 5, 8, 3, 9, 4, 10, 3, 10, 1, 7, 2, 10, 8, 4, 8, 9, 6, 9, 6]
                          weights : [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
                        - # Reel[2]
                          symbols : [8, 7, 6, 10, 5, 9, 10, 2, 9, 8, 5, 10, 10, 4, 7, 10, 6, 7, 8, 3, 9, 8, 4, 9, 10, 6, 8, 6, 9, 1]
                          weights : [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
                        - # Reel[3]
                          symbols : [8, 7, 6, 7, 4, 10, 3, 10, 6, 8, 5, 9, 6, 10, 8, 6, 7, 9, 1, 10, 8, 5, 10, 6, 10, 7, 4, 9, 7, 2]
                          weights : [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
                        - # Reel[4]
                          symbols : [5, 7, 8, 4, 8, 10, 2, 8, 10, 3, 10, 6, 7, 10, 1, 10, 7, 6, 9, 7, 6, 10, 6, 9, 5, 10, 2, 10, 4, 9]
                          weights : [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
          # 圖標設定
          SymbolSetting:
              symbolUsed : [Z1,C1,W1,H1,H2,H3,H4,L1,L2,L3,L4]
              payTable : 
                  - [0, 0, 0, 0, 0]
                  - [0, 0, 0, 0, 0]
                  - [0, 0, 150, 800, 7000]
                  - [0, 0, 40, 200, 1000]
                  - [0, 0, 30, 160, 700]
                  - [0, 0, 20, 110, 400]
                  - [0, 0, 15, 90, 250]
                  - [0, 0, 1, 30, 140]
                  - [0, 0, 1, 30, 140]
                  - [0, 0, 0, 22, 120]
                  - [0, 0, 0, 12, 80]
          # 中獎設定
          HitSetting:
              betType: BetTypeLineLTR # 由左至右連線
              lineTable: 
                  - [1, 1, 1, 1, 1]
                  - [0, 0, 0, 0, 0]
                  - [2, 2, 2, 2, 2]
                  - [0, 1, 2, 1, 0]
                  - [2, 1, 0, 1, 2]
                  - [1, 0, 0, 0, 1]
                  - [1, 2, 2, 2, 1]
                  - [0, 0, 1, 2, 2]
                  - [2, 2, 1, 0, 0]
                  - [1, 0, 1, 2, 1]
                  - [1, 2, 1, 0, 1]
                  - [0, 1, 1, 1, 0]
                  - [2, 1, 1, 1, 2]
                  - [0, 1, 0, 1, 0]
                  - [2, 1, 2, 1, 2]
                  - [1, 1, 0, 1, 1]
                  - [1, 1, 2, 1, 1]
                  - [0, 0, 2, 0, 0]
                  - [2, 2, 0, 2, 2]
                  - [0, 2, 2, 2, 0]


        - # GameModeSetting : FreeGame 模式設定
            # 盤面設定
            ScreenSetting:
                columns: 5
                rows: 3
                damp: 1
            # 生成盤面設定
            GenScreenSetting:
                GenReelType: GenReelByReelIdx
                ReelStripsGroup:
                    - # ReelStrip[0]
                      weight : 1
                      reels : 
                            - # Reel[0]
                              symbols : [6, 10, 7, 5, 9, 2, 2, 10, 9, 4, 8, 10, 1, 9, 3, 7, 8, 7, 4, 8, 1, 9, 6, 8, 6, 10, 1, 9, 5, 6]
                              weights : [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
                            - # Reel[1]
                              symbols : [10, 7, 5, 8, 7, 2, 2, 2, 6, 8, 9, 5, 1, 9, 9, 4, 10, 3, 10, 8, 7, 10, 10, 8, 4, 8, 9, 6, 9, 3]
                              weights : [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
                            - # Reel[2]
                              symbols : [8, 7, 6, 10, 5, 9, 2, 2, 10, 8, 5, 10, 1, 4, 7, 10, 9, 7, 8, 3, 3, 8, 4, 9, 10, 6, 8, 6, 9, 10]
                              weights : [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
                            - # Reel[3]
                              symbols : [8, 7, 6, 7, 4, 2, 3, 2, 3, 8, 5, 9, 1, 10, 8, 6, 7, 9, 10, 10, 8, 5, 10, 6, 10, 7, 4, 9, 7, 10]
                              weights : [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
                            - # Reel[4]
                              symbols : [5, 7, 8, 4, 2, 2, 2, 2, 2, 2, 10, 10, 1, 10, 7, 8, 7, 6, 9, 7, 6, 9, 6, 9, 5, 10, 8, 10, 4, 10]
                              weights : [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
            # 圖標設定
            SymbolSetting:
                symbolUsed : [Z1,C1,W1,H1,H2,H3,H4,L1,L2,L3,L4]
                payTable : 
                  - [0, 0, 0, 0, 0]
                  - [0, 0, 0, 0, 0]
                  - [0, 0, 150, 800, 7000]
                  - [0, 0, 40, 200, 1000]
                  - [0, 0, 30, 160, 700]
                  - [0, 0, 20, 110, 400]
                  - [0, 0, 15, 90, 250]
                  - [0, 0, 1, 30, 140]
                  - [0, 0, 1, 30, 140]
                  - [0, 0, 0, 22, 120]
                  - [0, 0, 0, 12, 80]
            # 中獎設定
            HitSetting:
                betType: BetTypeLineLTR # 由左至右連線
                lineTable: 
                  - [1, 1, 1, 1, 1] # 連線1
                  - [0, 0, 0, 0, 0] # 連線2
                  - [2, 2, 2, 2, 2]
                  - [0, 1, 2, 1, 0]
                  - [2, 1, 0, 1, 2]
                  - [1, 0, 0, 0, 1]
                  - [1, 2, 2, 2, 1]
                  - [0, 0, 1, 2, 2]
                  - [2, 2, 1, 0, 0]
                  - [1, 0, 1, 2, 1]
                  - [1, 2, 1, 0, 1]
                  - [0, 1, 1, 1, 0]
                  - [2, 1, 1, 1, 2]
                  - [0, 1, 0, 1, 0]
                  - [2, 1, 2, 1, 2]
                  - [1, 1, 0, 1, 1]
                  - [1, 1, 2, 1, 1]
                  - [0, 0, 2, 0, 0]
                  - [2, 2, 0, 2, 2]
                  - [0, 2, 2, 2, 0] # 連線20
            
    # 額外設定
    Fixed: 
      FreeGameRounds: 10
      RetriggerRounds: 5
      Multipilers: [3]
      C1Pay: [0, 0, 5, 28, 110]
        
```


internal/engine/game/game_2_demoline.go
實作遊戲邏輯

```go=
//game_2_demoline.go
// game_2_demoline.go
package game

import (
	"problab/internal/spec/enum"
	"problab/internal/spec/res"
	"problab/internal/spec/settings"
)

// ============================================================
// ** 註冊 **
// ============================================================

// 會自動執行
func init() {
	gameRegister[*NoExtend](
		enum.DemoLine,
		buildGame0002,
	)
}

// ============================================================
// ** 遊戲介面 **
// ============================================================

type game0002 struct {
	fixed *fixed0002
	hits  []int16
	c1Idx int16
	w1Idx int16
}

func buildGame0002(gh *GameHandler) gameLogic {
	// 建立 game0002 實例，讀取設定檔的 Fixed 區段到 fixed0002
	g := &game0002{
		fixed: new(fixed0002),
		c1Idx: 1,
		w1Idx: 2,
	}
	settings.DecodeFixed(gh.gameSetting, g.fixed)

	screenSize := gh.gameSetting.GameModeSettingList[0].ScreenSetting.ScreenSize
	g.hits = make([]int16, 0, screenSize)
	return g
}

// ============================================================
// ** 此遊戲 Fixed 設定宣告 **
// ============================================================

// fixed
type fixed0002 struct {
	FreeGameRounds  int   `yaml:"FreeGameRounds"`  // BG 觸發 FG
	RetriggerRounds int   `yaml:"RetriggerRounds"` // FG 觸發加局
	Multipilers     []int `yaml:"Multipilers"`     // 乘數
	C1Pay           []int `yaml:"C1Pay"`           // C1 賠率
}

// ============================================================
// ** 此遊戲需要的額外結構宣告: extend拓展結果格式宣告 **
// ============================================================

// ============================================================
// ** 遊戲主邏輯入口 **
// ============================================================

// getResult 主要介面函數 回傳遊戲結果 *res.SpinResult

// 一把 spin 的入口。
func (g *game0002) getResult(betMode int, betMult int, gh *GameHandler) *res.SpinResult {
	// 先 gh.StartNewSpin 重置共用 SpinResult
	betUnit := gh.BetUnit[betMode]
	sr := gh.StartNewSpin(betMode, betMult)

	base := g.getBaseResult(betUnit, betMult, gh) // 跑 base mode
	sr.AppendModeResult(base)

	// 觸發 FG
	if base.Trigger != 0 {
		free := g.getFreeResult(betUnit, betMult, gh) // 跑 free mode
		sr.AppendModeResult(free)
	}
	sr.End()
	return sr
}

// ============================================================
// ** 遊戲中各模式內部邏輯實作 **
// ============================================================

func (g *game0002) getBaseResult(betUnit int, betMult int, gh *GameHandler) *res.GameModeResult {
	mode := gh.GameModeHandlerList[0] // 對應 yaml game mpde 0
	sg := mode.ScreenGenerator
	sc := mode.ScreenCalculator
	gmr := mode.GameModeResult // base game 結果

	// 1. 生成盤面
	screen := sg.GenScreen()

	// 2. 得分符號算分
	_ = sc.CalcScreen(betMult, screen, gmr)

	// 3. C1 符號算分
	findC1(screen, betUnit, betMult, gmr, g)

	// 4. Act完成
	gmr.FinishAct("GenAndCalcScreen", screen, nil)

	// 5. 判斷觸發
	gmr.Trigger = g.trigger(screen)

	// 6. Round提交
	gmr.FinishRound()

	return mode.YieldResult()
}

func (g *game0002) getFreeResult(betUnit int, betMult int, gh *GameHandler) *res.GameModeResult {
	mode := gh.GameModeHandlerList[1] // 對應 yaml game mpde 1
	sg := mode.ScreenGenerator
	sc := mode.ScreenCalculator
	gmr := mode.GameModeResult

	nowLimitRounds := g.fixed.FreeGameRounds // 初始 FG 局數

	i := 0 // 當前 FG 次數
	for i < nowLimitRounds {
		detailStart := len(gmr.GetDetails()) // 本次 Act 新增的 CalcScreen detail，避免改到前一 Act 的紀錄。

		// 1. 生成盤面
		screen := sg.GenScreen()

		// 2. 算分
		_ = sc.CalcScreen(betMult, screen, gmr)

		// 3. 判斷有沒有 W1 如果有 分數 x3
		applyW1Multiplier(screen, gmr, detailStart, g)
		// 4. C1 符號算分
		findC1(screen, betUnit, betMult, gmr, g)

		// 5. 判斷 FG 加局
		if g.trigger(screen) != 0 {

			nowLimitRounds += g.fixed.RetriggerRounds
		}

		// 6. Act完成
		gmr.FinishAct("GenAndCalcScreen", screen, nil)
		gmr.FinishRound()

		// 更新
		i++
	}

	return mode.YieldResult()
}

// ============================================================
// ** 遊戲內部輔助函數實作 **
// ============================================================

// 0 代表不觸發 > 0 各自觸發
func (g *game0002) trigger(screen []int16) int {
	count := 0
	for i := 0; i < len(screen); i++ {
		if screen[i] == 1 {
			count++
		}
	}
	if count > 2 {
		return 1
	}
	return 0
}

// 1. 任意位置 3+ 個 C1 依 scatter 表計分
func findC1(screen []int16, betUnit int, betMult int, gmr *res.GameModeResult, g *game0002) {

	// 數量與命中位置
	hits := g.hits[:0]
	for i, v := range screen {
		if v == g.c1Idx {
			hits = append(hits, int16(i))
		}
	}

	count := len(hits)
	if count < 3 {
		return
	}

	// C1Pay 是 C1 的 pay
	idx := count
	if idx >= len(g.fixed.C1Pay) {
		idx = len(g.fixed.C1Pay)
	}

	win := betMult * g.fixed.C1Pay[idx-1] * betUnit

	if win > 0 {
		// lineID = -1 代表散佈，不走線表
		gmr.RecordDetail(win, int16(g.c1Idx), -1, count, 0, 0, hits)
	}
}

// 2. 判斷 W1 是否出現在中獎線上的函數，如果有獎金 x3
func applyW1Multiplier(screen []int16, gmr *res.GameModeResult, detailStart int, g *game0002) {
	// w1Idx := 2 // W1 index value

	details := gmr.GetDetails()
	if detailStart >= len(details) {
		return
	}

	extraWin := 0 // 維護一個乘數部份的 win，用於更新

	for i := detailStart; i < len(details); i++ {

		// 以下是判斷 W1 是否出現在路線上的邏輯
		start := details[i].HitsFlatStart
		end := start + details[i].HitsFlatLen
		if end > len(gmr.HitsFlat) {
			continue
		}
		hits := gmr.HitsFlat[start:end]

		hasW1 := false
		for _, pos := range hits {
			if screen[pos] == g.w1Idx {
				hasW1 = true
				break
			}
		}

		if !hasW1 {
			continue
		}

		// 更新數值
		win := details[i].Win          // 基礎贏分
		mult := g.fixed.Multipilers[0] // 乘數
		details[i].Win = win * mult    // 更新
		extraWin += win * (mult - 1)   // x3 多出的部分，也就是 x2
	}
	if extraWin > 0 {
		gmr.UpdateTmpWin(gmr.GetTmpWin() + extraWin) // 更新累積的 win
	}
}

```

internal/spec/enum/gamename.go 
在 GameNameMap 新增遊戲名稱

```go=
// gamename.go
package enum

import (
	"log"
)

func init() {
	for gns, gn := range GameNameMap {
		if _, ok := gamemap[gn]; ok {
			log.Fatalf("%v is redeclared", gn)
		}
		gamemap[gn] = gns
	}
}

// GameName 機台Enum
type GameName int

// 範例slot
const (
	// DemoNormal [老虎機] 0 基本機台
	DemoNormal GameName = iota
	DemoCascade
	DemoLine
)

const (
	StormOfSeth GameName = 1234 + iota
)

// 正式:cluster
const (
	VikingAge GameName = 1310 + iota
)

// GameNameMap: 註冊名稱與 enum 關係對應表
var GameNameMap = map[string]GameName{
	"DemoNormal":  DemoNormal,
	"DemoCascade": DemoCascade,
	"StormOfSeth": StormOfSeth,
	"VikingAge":   VikingAge,
	// 練習
	"DemoLine": DemoLine, // 新增註冊
}

// 反查表
var gamemap = map[GameName]string{}

// GameName -> GameNameStr
func GameNameStr(gn GameName) (string, bool) {
	str, ok := gamemap[gn]
	return str, ok
}
```

### 效能
 火焰圖
![image](https://hackmd.io/_uploads/SJYAa3cWZx.png)

### 反饋
- [x] 1. 處理當前這款遊戲邏輯內的函數都要掛在 `game0002` struct 的 method 中，避免相同 package 命名衝突
- [x] 2. 累積 C1 獎金的地方放在 `game0002` 多維護一個 `C1Win` 屬性不要放在 `gmr.RecordDetail()` 因為這兩種算分方式是不同的
- [x] 3. `win := betMult * g.fixed.C1Pay[idx-1] * betUnit` 不需要 `betUnit`，直接在 yaml 檔的參數中處理好就好了，因為是靜態的
- [x] 4. `trigger()` 跟 `findC1()` 函數功能有重疊的部分
    4.1. 函數名稱調整成 `findC1()` -> `CountC1()` 功能是計算當前盤面 C1 符號的數量
    4.2. `trigger()` 獲取 `CountC1()` 計算後的 `g.C1Count` 判斷是否觸發 FG
- [x] 5. 判斷 "是否是某個符號" 的做法?
    5.1. 方法1: 適用場景只需要判斷一種 Scatter 或 Wild 時使用，具體做法是用 SymbolSetting.SymbolTypes 判斷類型
    5.2. 方法2: 適用場景 Scatter 有兩種(`C1`, `C2`) 需要分別去統計，不同符號分別觸發不同的遊戲邏輯。
- [x] 6. Multipilers 只需是 `int` 不需要 `[]int`

### 調整
模擬結果各項數值與修改前無異
```
+--------------------------------+
|            Summary             |
+--------------+-----------------+
| Game Name    | DemoLine        |
| Total Rounds | 100,000,000     |
| Total RTP    | 97.00 %         |
| RTP 95% CI   | [96.82%,97.18%] |
| Total Bet    | 2,000,000,000   |
| Total Win    | 1,940,048,517   |
| Base Win     | 1,259,368,800   |
| Free Win     | 680,679,717     |
| Win Counts   | 30,375,292      |
| Trigger      | 856,596         |
| STD          | 9.248           |
| CV           | 9.534           |
+--------------+-----------------+
```


反饋內容修正完畢，下方是調整過的 code 內容

1. yaml 移除 `GameSetting layer` 以及對 Fixed layer 做調整
```yaml=
# 額外設定
Fixed: 
  FreeGameRounds: 10
  RetriggerRounds: 5
  Multipilers: 3 # [3] -> 3 只有一個元素，所以改變型別
  C1Pay: [0, 0, 100, 560, 2200] # 直接乘 BetUnit，所以這個元素的意義是獲取的獎金(BetUnit * pay)
        
```

2. 遊戲邏輯部分
```go=
// internal/engine/game/game_2_demoline.go
// game_2_demoline.go
package game

import (
	"problab/internal/spec/enum"
	"problab/internal/spec/res"
	"problab/internal/spec/settings"
)

// ============================================================
// ** 註冊 **
// ============================================================

// 會自動執行
func init() {
	gameRegister[*NoExtend](
		enum.DemoLine,
		buildGame0002,
	)
}

// ============================================================
// ** 遊戲介面 **
// ============================================================

type game0002 struct {
	fixed *fixed0002
	hits  []int16
	types []enum.SymbolType
    
        // 維護 C1 相關統計參數
	C1Wins  int // C1 累積獎金，緩存可重複調用
	C1Count int // 盤面 C1 數量，緩存可重複調用
}

func buildGame0002(gh *GameHandler) gameLogic {
	// 建立 game0002 實例，讀取設定檔的 Fixed 區段到 fixed0002
	g := &game0002{
		fixed:   new(fixed0002),
		types:   []enum.SymbolType{}, // 先初始化一個空 slice
		C1Wins:  0,
		C1Count: 0,
	}

	settings.DecodeFixed(gh.gameSetting, g.fixed)

	// 直接調用，需要確保後面不會再改
	// g.types = gh.gameSetting.GameModeSettingList[0].SymbolSetting.SymbolTypes

	// 所以我選擇複製一份比較安全
	types := gh.gameSetting.GameModeSettingList[0].SymbolSetting.SymbolTypes
	g.types = append(g.types, types...)

	screenSize := gh.gameSetting.GameModeSettingList[0].ScreenSetting.ScreenSize
	g.hits = make([]int16, 0, screenSize)
	return g
}

// ============================================================
// ** 此遊戲 Fixed 設定宣告 **
// ============================================================

// fixed
type fixed0002 struct {
	FreeGameRounds  int   `yaml:"FreeGameRounds"`  // BG 觸發 FG
	RetriggerRounds int   `yaml:"RetriggerRounds"` // FG 觸發加局
	Multipiler      int   `yaml:"Multipilers"`     // 乘數
	C1Pay           []int `yaml:"C1Pay"`           // C1 賠率
}

// ============================================================
// ** 此遊戲需要的額外結構宣告: extend拓展結果格式宣告 **
// ============================================================

// ============================================================
// ** 遊戲主邏輯入口 **
// ============================================================

// getResult 主要介面函數 回傳遊戲結果 *res.SpinResult

// 一把 spin 的入口。
func (g *game0002) getResult(betMode int, betMult int, gh *GameHandler) *res.SpinResult {
	// 先 gh.StartNewSpin 重置共用 SpinResult
	sr := gh.StartNewSpin(betMode, betMult)

	base := g.getBaseResult(betMult, gh) // 跑 base mode
	sr.AppendModeResult(base)

	// 觸發 FG
	if base.Trigger != 0 {
		free := g.getFreeResult(betMult, gh) // 跑 free mode
		sr.AppendModeResult(free)
	}
	sr.End()
	return sr
}

// ============================================================
// ** 遊戲中各模式內部邏輯實作 **
// ============================================================

func (g *game0002) getBaseResult(betMult int, gh *GameHandler) *res.GameModeResult {
	mode := gh.GameModeHandlerList[0] // 對應 yaml game mpde 0
	sg := mode.ScreenGenerator
	sc := mode.ScreenCalculator
	gmr := mode.GameModeResult // base game 結果

	// 1. 生成盤面
	screen := sg.GenScreen()

	// 2. 得分符號算分
	_ = sc.CalcScreen(betMult, screen, gmr)

	// 3. C1 符號算分
	g.countC1(screen, betMult, gmr)

	// 4. Act完成
	gmr.FinishAct("GenAndCalcScreen", screen, nil)

	// 5. 判斷觸發
	gmr.Trigger = g.trigger()

	// 6. Round提交
	gmr.FinishRound()

	return mode.YieldResult()
}

func (g *game0002) getFreeResult(betMult int, gh *GameHandler) *res.GameModeResult {
	mode := gh.GameModeHandlerList[1] // 對應 yaml game mpde 1
	sg := mode.ScreenGenerator
	sc := mode.ScreenCalculator
	gmr := mode.GameModeResult

	nowLimitRounds := g.fixed.FreeGameRounds // 初始 FG 局數

	i := 0 // 當前 FG 次數
	for i < nowLimitRounds {
		detailStart := len(gmr.GetDetails()) // 本次 Act 新增的 CalcScreen detail，避免改到前一 Act 的紀錄。

		// 1. 生成盤面
		screen := sg.GenScreen()

		// 2. 算分
		_ = sc.CalcScreen(betMult, screen, gmr)

		// 3. 判斷有沒有 W1 如果有 分數 x3
		g.applyW1Multiplier(screen, gmr, detailStart)
		// 4. C1 符號算分
		g.countC1(screen, betMult, gmr)

		// 5. 判斷 FG 加局
		if g.trigger() != 0 {
			nowLimitRounds += g.fixed.RetriggerRounds
		}

		// 6. Act完成
		gmr.FinishAct("GenAndCalcScreen", screen, nil)
		gmr.FinishRound()

		// 更新
		i++
	}

	return mode.YieldResult()
}

// ============================================================
// ** 遊戲內部輔助函數實作 **
// ============================================================

// 0 代表不觸發 > 0 各自觸發
func (g *game0002) trigger() int {

	if g.C1Count > 2 {
		return 1
	}
	return 0
}

// 1. 任意位置 3+ 個 C1 依 scatter 表計分
func (g *game0002) countC1(screen []int16, betMult int, gmr *res.GameModeResult) {
	// 1.初始化
	g.C1Count = 0
	g.C1Wins = 0

	// 2.計算 C1 符號數量
	for _, sym := range screen {
		if g.types[sym] == enum.SymbolTypeScatter {
			g.C1Count++
		}
	}

	// 3.早退機制
	if g.C1Count < 3 {
		return
	}

	// 4.上邊界處理
	if g.C1Count >= len(g.fixed.C1Pay) {
		g.C1Count = len(g.fixed.C1Pay)
	}

	// 5.更新 C1 累積獎金
	g.C1Wins = betMult * g.fixed.C1Pay[g.C1Count-1]
	gmr.UpdateTmpWin(gmr.GetTmpWin() + g.C1Wins)
}

// 2. 判斷 W1 是否出現在中獎線上的函數，如果有獎金 x3
func (g *game0002) applyW1Multiplier(screen []int16, gmr *res.GameModeResult, detailStart int) {
	details := gmr.GetDetails()
	if detailStart >= len(details) {
		return
	}

	extraWin := 0 // 維護一個乘數部份的 win，用於更新

	for i := detailStart; i < len(details); i++ {

		// 以下是判斷 W1 是否出現在路線上的邏輯
		start := details[i].HitsFlatStart
		end := start + details[i].HitsFlatLen
		if end > len(gmr.HitsFlat) {
			continue
		}
		hits := gmr.HitsFlat[start:end]

		hasW1 := false
		for _, pos := range hits {
			if g.types[screen[pos]] == enum.SymbolTypeWild {
				hasW1 = true
				break
			}
		}

		if !hasW1 {
			continue
		}

		// 更新數值
		win := details[i].Win        // 基礎贏分
		mult := g.fixed.Multipiler   // 乘數
		details[i].Win = win * mult  // 更新
		extraWin += win * (mult - 1) // x3 多出的部分，也就是 x2
	}

	if extraWin > 0 {
		gmr.UpdateTmpWin(gmr.GetTmpWin() + extraWin) // 更新累積的 win
	}
}
```

## extend 拓展結果格式宣告

### 結果 1
假設情境: C1 wins 跟 C1 count 需要暴露到 api 上

```json=
{
  "win": 0,
  "game": "DemoLine",
  "betunits": [20],
  "betmode": 0,
  "betmult": 1,
  "gamemodes": [
    {
      "win": 0,
      "modeid": 0,
      "isend": true,
      "trigger": 0,
      "rounds": [
        {
          "Round": 0,
          "RoundWin": 0,
          "NowTotalWin": 0,
          "StepsStart": 0,
          "StepsEnd": 0,
          "ActStart": 0,
          "ActEnd": 1
        }
      ],
      "acts": [
        {
          "round": 0,
          "step": 0,
          "act": 0,
          "acttype": "GenAndCalcScreen",
          "actwin": 0,
          "stepaccwin": 0,
          "roundaccwin": 0,
          "nowtotalwin": 0,
          "detailsstart": 0,
          "detailsend": 0,
          "screenstart": 0,
          "ext": {
            "c1wins": 0, // C1 贏分
            "c1count": 1 // C1 數量
          }
        }
      ],
      "screensize": 15,
      "screens": [4, 10, 2, 6, 10, 8, 1, 9, 10, 6, 10, 7, 8, 7, 9]
    }
  ],
  "isend": true
}
```

調整後的 code

```go=
// game_2_demoline.go
package game

import (
	"problab/internal/spec/enum"
	"problab/internal/spec/res"
	"problab/internal/spec/settings"
)

// ============================================================
// ** 註冊 **
// ============================================================

func init() {
	gameRegister[*extend0002](
		enum.DemoLine,
		buildGame0002,
	)
}

// ============================================================
// ** 遊戲介面 **
// ============================================================

type game0002 struct {
	fixed *fixed0002
	hits  []int16

	types []enum.SymbolType // 符號類別
	exts  *extend0002
}

func buildGame0002(gh *GameHandler) gameLogic {

	// 創建 fixed0002 實例
	g0002 := &game0002{
		fixed: new(fixed0002),                                                  // 額外需要的設定
		types: gh.gameSetting.GameModeSettingList[0].SymbolSetting.SymbolTypes, // 先初始化一個空 slice
	}

	// 讀設定檔
	settings.DecodeFixed(gh.gameSetting, g0002.fixed)
	g0002.exts = buildExtend0002() // 創建 extend0002 實例

	screenSize := gh.gameSetting.GameModeSettingList[0].ScreenSetting.ScreenSize // 盤面大小
	g0002.hits = make([]int16, 0, screenSize)                                    //

	return g0002
}

// ============================================================
// ** 此遊戲 Fixed 設定宣告 **
// ============================================================

// fixed
type fixed0002 struct {
	FreeGameRounds  int   `yaml:"FreeGameRounds"`  // BG 觸發 FG
	RetriggerRounds int   `yaml:"RetriggerRounds"` // FG 觸發加局
	Multipiler      int   `yaml:"Multipilers"`     // 乘數
	C1Pay           []int `yaml:"C1Pay"`           // C1 賠率
}

// ============================================================
// ** 此遊戲需要的額外結構宣告: extend 拓展結果格式宣告 **
// ============================================================
type extend0002 struct {
	C1Wins  int `json:"c1wins"`
	C1Count int `json:"c1count"`
}

func buildExtend0002() *extend0002 {
	return &extend0002{
		C1Wins:  0,
		C1Count: 0,
	}
}

func (ext *extend0002) reset() {
	ext.C1Wins = 0
	ext.C1Count = 0
}

// ============================================================
// ** 遊戲主邏輯入口 **
// ============================================================

// getResult 主要介面函數 回傳遊戲結果 *res.SpinResult

// 一把 spin 的入口。
func (g *game0002) getResult(betMode int, betMult int, gh *GameHandler) *res.SpinResult {
	// 先 gh.StartNewSpin 重置共用 SpinResult
	sr := gh.StartNewSpin(betMode, betMult)

	//
	base := g.getBaseResult(betMult, gh) // 跑 base mode
	sr.AppendModeResult(base)

	// 觸發 FG
	if base.Trigger != 0 {
		free := g.getFreeResult(betMult, gh) // 跑 free mode
		sr.AppendModeResult(free)
	}
	sr.End()
	return sr
}

// ============================================================
// ** 遊戲中各模式內部邏輯實作 **
// ============================================================

func (g *game0002) getBaseResult(betMult int, gh *GameHandler) *res.GameModeResult {
	mode := gh.GameModeHandlerList[0] // 對應 yaml game mpde 0
	sg := mode.ScreenGenerator
	sc := mode.ScreenCalculator
	gmr := mode.GameModeResult // base game 結果
	// g.exts.reset()             // 重置

	// 1. 生成盤面
	screen := sg.GenScreen()

	// 2. 得分符號算分
	_ = sc.CalcScreen(betMult, screen, gmr)

	// 3. C1 符號算分
	g.countC1(screen, betMult, gmr)

	// 4. Act完成
	gmr.FinishAct("GenAndCalcScreen", screen, g.exts)

	// 5. 判斷觸發
	if g.exts.C1Count > 2 {
		gmr.Trigger = 1
	}

	// 6. Round提交
	gmr.FinishRound()

	return mode.YieldResult()
}

func (g *game0002) getFreeResult(betMult int, gh *GameHandler) *res.GameModeResult {
	mode := gh.GameModeHandlerList[1] // 對應 yaml game mpde 1
	sg := mode.ScreenGenerator
	sc := mode.ScreenCalculator
	gmr := mode.GameModeResult

	nowLimitRounds := g.fixed.FreeGameRounds // 初始 FG 局數

	round := 0 // 當前 FG 次數
	for round < nowLimitRounds {
		detailStart := len(gmr.GetDetails()) // 本次 Act 新增的 CalcScreen detail，避免改到前一 Act 的紀錄。

		// 1. 生成盤面
		screen := sg.GenScreen()

		// 2. 算分
		_ = sc.CalcScreen(betMult, screen, gmr)

		// 3. 判斷有沒有 W1 如果有 分數 x3
		g.applyW1Multiplier(screen, gmr, detailStart)
		// 4. C1 符號算分
		g.countC1(screen, betMult, gmr)

		// 5. 判斷 FG 加局
		if g.exts.C1Count > 2 {
			nowLimitRounds += g.fixed.RetriggerRounds
		}

		// 6. Act完成
		gmr.FinishAct("GenAndCalcScreen", screen, g.exts)
		gmr.FinishRound()

		// 更新
		round++
	}

	return mode.YieldResult()
}

// ============================================================
// ** 遊戲內部輔助函數實作 **
// ============================================================
// 1. 任意位置 3+ 個 C1 依 scatter 表計分
func (g *game0002) countC1(screen []int16, betMult int, gmr *res.GameModeResult) {
	g.exts.reset() // 重置
	if len(g.types) == 0 || len(g.fixed.C1Pay) == 0 {
		return
	}

	// 2.計算 C1 符號數量
	for _, sym := range screen {
		if sym >= 0 && int(sym) < len(g.types) && g.types[sym] == enum.SymbolTypeScatter {
			g.exts.C1Count++
		}
	}

	// 3.早退機制
	if g.exts.C1Count < 3 {
		return
	}

	// 4.上邊界處理
	if g.exts.C1Count >= len(g.fixed.C1Pay) {
		g.exts.C1Count = len(g.fixed.C1Pay)
	}

	// 5.更新 C1 累積獎金
	g.exts.C1Wins = betMult * g.fixed.C1Pay[g.exts.C1Count-1]
	gmr.UpdateTmpWin(gmr.GetTmpWin() + g.exts.C1Wins)
}

// 2. 判斷 W1 是否出現在中獎線上的函數，如果有獎金 x3
func (g *game0002) applyW1Multiplier(screen []int16, gmr *res.GameModeResult, detailStart int) {
	details := gmr.GetDetails()
	if detailStart >= len(details) || len(g.types) == 0 {
		return
	}

	mult := g.fixed.Multipiler // 乘數
	if mult <= 1 {
		return
	}

	extraWin := 0 // 維護一個乘數部份的 win，用於更新

	for i := detailStart; i < len(details); i++ {

		// 以下是判斷 W1 是否出現在路線上的邏輯
		start := details[i].HitsFlatStart
		end := start + details[i].HitsFlatLen
		if end > len(gmr.HitsFlat) {
			continue
		}
		hits := gmr.HitsFlat[start:end]

		hasW1 := false
		for _, pos := range hits {
			if screen[pos] >= 0 && int(screen[pos]) < len(g.types) && g.types[screen[pos]] == enum.SymbolTypeWild {
				hasW1 = true
				break
			}
		}

		if !hasW1 {
			continue
		}

		// 更新數值
		win := details[i].Win        // 基礎贏分
		details[i].Win = win * mult  // 更新
		extraWin += win * (mult - 1) // x3 多出的部分，也就是 x2
	}

	if extraWin > 0 {
		gmr.UpdateTmpWin(gmr.GetTmpWin() + extraWin) // 更新累積的 win
	}
}
```
### 反饋

- [x]  1. bug: 每一局 Free spin 需要創建一個新的 extend0002 實例，原因是共用 extend0002 會導致覆蓋問題，結果只會在 api 看到最後一次 FG spin 的 ext 結果

```json=
// 修改前 FG 錯誤數據，
"round": 0,
"ext": {
  "c1wins": 0,
  "c1count": 2
}

"round": 1,
"ext": {
  "c1wins": 0,
  "c1count": 2
}

... 其他略

"round": 9,
"ext": {
  "c1wins": 0,
  "c1count": 2
}
```
### 結果 2

開啟 api 後的[測試結果](https://hackmd.io/@chiSean/ry6oySTZWl)

```json=
// 修改後 FG 正確數據
"round": 0,
"ext": {
  "c1wins": 0,
  "c1count": 0
}

"round": 1,
"ext": {
  "c1wins": 0,
  "c1count": 2
}

... 其他略

"round": 9,
"ext": {
  "c1wins": 0,
  "c1count": 0
}

```
### 調整

在 `getFreeResult` 函數每一次 FG spin 時創建一個新的 `extend0002` 實例
```go=
// game_2_demoline.go
package game

import (
	"problab/internal/spec/enum"
	"problab/internal/spec/res"
	"problab/internal/spec/settings"
)

// ============================================================
// ** 註冊 **
// ============================================================

// 會自動執行
func init() {
	gameRegister[*extend0002](
		enum.DemoLine,
		buildGame0002,
	)
}

// ============================================================
// ** 遊戲介面 **
// ============================================================

type game0002 struct {
	fixed *fixed0002
	hits  []int16

	types []enum.SymbolType // 符號類別
	exts  *extend0002
}

func buildGame0002(gh *GameHandler) gameLogic {

	// 創建 fixed0002 實例
	g0002 := &game0002{
		fixed: new(fixed0002),                                                  // 額外需要的設定
		types: gh.gameSetting.GameModeSettingList[0].SymbolSetting.SymbolTypes, // 先初始化一個空 slice
	}

	// 讀設定檔
	settings.DecodeFixed(gh.gameSetting, g0002.fixed)
	g0002.exts = buildExtend0002() // 創建 extend0002 實例

	screenSize := gh.gameSetting.GameModeSettingList[0].ScreenSetting.ScreenSize // 盤面大小
	g0002.hits = make([]int16, 0, screenSize)                                    //

	return g0002
}

// ============================================================
// ** 此遊戲 Fixed 設定宣告 **
// ============================================================

// fixed
type fixed0002 struct {
	FreeGameRounds  int   `yaml:"FreeGameRounds"`  // BG 觸發 FG
	RetriggerRounds int   `yaml:"RetriggerRounds"` // FG 觸發加局
	Multipiler      int   `yaml:"Multipilers"`     // 乘數
	C1Pay           []int `yaml:"C1Pay"`           // C1 賠率
}

// ============================================================
// ** 此遊戲需要的額外結構宣告: extend拓展結果格式宣告 **
// ============================================================
type extend0002 struct {
	C1Wins  int `json:"c1wins"`
	C1Count int `json:"c1count"`
}

func buildExtend0002() *extend0002 {
	return &extend0002{
		C1Wins:  0,
		C1Count: 0,
	}
}

func (ext *extend0002) reset() {
	ext.C1Wins = 0
	ext.C1Count = 0
}

// ============================================================
// ** 遊戲主邏輯入口 **
// ============================================================

// getResult 主要介面函數 回傳遊戲結果 *res.SpinResult

// 一把 spin 的入口。
func (g *game0002) getResult(betMode int, betMult int, gh *GameHandler) *res.SpinResult {
	// 先 gh.StartNewSpin 重置共用 SpinResult
	sr := gh.StartNewSpin(betMode, betMult)

	//
	base := g.getBaseResult(betMult, gh) // 跑 base mode
	sr.AppendModeResult(base)

	// 觸發 FG
	if base.Trigger != 0 {
		free := g.getFreeResult(betMult, gh) // 跑 free mode
		sr.AppendModeResult(free)
	}
	sr.End()
	return sr
}

// ============================================================
// ** 遊戲中各模式內部邏輯實作 **
// ============================================================

func (g *game0002) getBaseResult(betMult int, gh *GameHandler) *res.GameModeResult {
	mode := gh.GameModeHandlerList[0] // 對應 yaml game mpde 0
	sg := mode.ScreenGenerator
	sc := mode.ScreenCalculator
	gmr := mode.GameModeResult // base game 結果

	g.exts.reset()

	// 1. 生成盤面
	screen := sg.GenScreen()

	// 2. 得分符號算分
	_ = sc.CalcScreen(betMult, screen, gmr)

	// 3. C1 符號算分
	g.countC1(screen, betMult, gmr, g.exts)

	// 4. Act完成
	gmr.FinishAct("GenAndCalcScreen", screen, g.exts)

	// 5. 判斷觸發
	if g.exts.C1Count > 2 {
		gmr.Trigger = 1
	}
	// 6. Round提交
	gmr.FinishRound()

	return mode.YieldResult()
}

func (g *game0002) getFreeResult(betMult int, gh *GameHandler) *res.GameModeResult {
	mode := gh.GameModeHandlerList[1] // 對應 yaml game mpde 1
	sg := mode.ScreenGenerator
	sc := mode.ScreenCalculator
	gmr := mode.GameModeResult

	nowLimitRounds := g.fixed.FreeGameRounds // 初始 FG 局數

	i := 0 // 當前 FG 次數
	for i < nowLimitRounds {

		// 每一局 Free spin 創建一個新的 extend0002 實例，原因是共用 extend0002 會導致覆蓋問題，結果是只會看到最後一個結果
		ext := buildExtend0002()

		detailStart := len(gmr.GetDetails()) // 本次 Act 新增的 CalcScreen detail，避免改到前一 Act 的紀錄。

		// 1. 生成盤面
		screen := sg.GenScreen()

		// 2. 算分
		_ = sc.CalcScreen(betMult, screen, gmr)

		// 3. 判斷有沒有 W1 如果有 分數 x3
		g.applyW1Multiplier(screen, gmr, detailStart)
		// 4. C1 符號算分
		g.countC1(screen, betMult, gmr, ext)

		// 5. 判斷 FG 加局
		if ext.C1Count > 2 {
			nowLimitRounds += g.fixed.RetriggerRounds
		}

		// 6. Act完成
		gmr.FinishAct("GenAndCalcScreen", screen, ext)
		gmr.FinishRound()

		// 更新
		i++
	}

	return mode.YieldResult()
}

// ============================================================
// ** 遊戲內部輔助函數實作 **
// ============================================================
// 1. 任意位置 3+ 個 C1 依 scatter 表計分
func (g *game0002) countC1(screen []int16, betMult int, gmr *res.GameModeResult, ext *extend0002) {
	if len(g.types) == 0 || len(g.fixed.C1Pay) == 0 {
		return
	}

	// 2.計算 C1 符號數量
	for _, sym := range screen {
		if sym >= 0 && int(sym) < len(g.types) && g.types[sym] == enum.SymbolTypeScatter {
			ext.C1Count++
		}
	}

	// 3.早退機制
	if ext.C1Count < 3 {
		return
	}

	// 4.上邊界處理
	if ext.C1Count >= len(g.fixed.C1Pay) {
		ext.C1Count = len(g.fixed.C1Pay)
	}

	// 5.更新 C1 累積獎金
	ext.C1Wins = betMult * g.fixed.C1Pay[ext.C1Count-1]
	gmr.UpdateTmpWin(gmr.GetTmpWin() + ext.C1Wins)
}

// 2. 判斷 W1 是否出現在中獎線上的函數，如果有獎金 x3
func (g *game0002) applyW1Multiplier(screen []int16, gmr *res.GameModeResult, detailStart int) {
	details := gmr.GetDetails()
	if detailStart >= len(details) || len(g.types) == 0 {
		return
	}

	mult := g.fixed.Multipiler // 乘數
	if mult <= 1 {
		return
	}

	extraWin := 0 // 維護一個乘數部份的 win，用於更新

	for i := detailStart; i < len(details); i++ {

		// 以下是判斷 W1 是否出現在路線上的邏輯
		start := details[i].HitsFlatStart
		end := start + details[i].HitsFlatLen
		if end > len(gmr.HitsFlat) {
			continue
		}
		hits := gmr.HitsFlat[start:end]

		hasW1 := false
		for _, pos := range hits {
			if screen[pos] >= 0 && int(screen[pos]) < len(g.types) && g.types[screen[pos]] == enum.SymbolTypeWild {
				hasW1 = true
				break
			}
		}

		if !hasW1 {
			continue
		}

		// 更新數值
		win := details[i].Win        // 基礎贏分
		details[i].Win = win * mult  // 更新
		extraWin += win * (mult - 1) // x3 多出的部分，也就是 x2
	}

	if extraWin > 0 {
		gmr.UpdateTmpWin(gmr.GetTmpWin() + extraWin) // 更新累積的 win
	}
}

```
































