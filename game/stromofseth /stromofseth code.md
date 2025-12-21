package game

import (
"log"
"problab/internal/core"
"problab/internal/result"
"problab/internal/sampler"
"problab/internal/settings"
"problab/pkg/spec/enum"
)

// ============================================================
// ** 註冊 **
// ============================================================

func init() {
gameRegister[*extend1801](
enum.StormOfSeth,
buildGame1801,
)
}

// ============================================================
// ** 遊戲介面 **
// ============================================================

type game1801 struct {
fixed *fixed1801 // 額外設定
ext *extend1801 // 對外暴露資訊

    // 輔助參數
    accWin      int // 累積贏分
    maxWinLimit int // 最高贏分上限

}

func buildGame1801(g \*GameHandler) gameLogic {

    gs := g.gameSetting

    // 創建 fixed1801 實例
    f := &fixed1801{
    	fillScreenIdx:        make([]int, gs.GameModeSettingList[0].ScreenSetting.Columns),      //
    	nowfillReelStripsIdx: make([]int, gs.GameModeSettingList[0].ScreenSetting.Columns),      //
    	betmodes:             make([]betModes1801, len(g.BetUnit)),                              // 下注模式
    	screen:               make([]int16, gs.GameModeSettingList[0].ScreenSetting.ScreenSize), // 盤面
    	symbolTypes:          gs.GameModeSettingList[0].SymbolSetting.SymbolTypes,               // 符號類型清單
    	multipilersIndex:     make([]int, 501),                                                  // 乘數索引清單
    	ScatterPay:           make([]int, gs.GameModeSettingList[0].ScreenSetting.ScreenSize),   // scatter 賠率清單
    }

    // 讀設定檔
    if err := settings.DecodeFixed(gs, f); err != nil {
    	log.Fatalf("game %s decode fixed failed : %s", gs.GameNameStr, err.Error())
    }

    // 初始化乘數索引清單
    for idx := range f.multipilersIndex {
    	f.multipilersIndex[idx] = -1
    }
    // 添加索引值
    for idx, mu := range f.Multipilers {
    	f.multipilersIndex[mu] = idx
    }

    // 設定檔 weight 轉存為 Lut
    for d := 0; d < len(g.BetUnit); d++ {
    	f.betmodes[d] = betModes1801{
    		betMode:          d,
    		baseReelLut:      sampler.BuildLookUpTable(f.BetModes[d].BaseReelChooseWeight), // 將權重轉換為 Lut
    		freeReelLut:      sampler.BuildLookUpTable(f.BetModes[d].FreeReelChooseWeight),
    		baseMultiProbLut: sampler.BuildLookUpTable(f.BetModes[d].BaseMultiProb),
    		baseMultiLvUp:    f.BetModes[d].BaseMultiLvUp,
    		freeMultiProbLut: sampler.BuildLookUpTable(f.BetModes[d].FreeMultiProb),
    		freeMultiLvUp:    f.BetModes[d].FreeMultiLvUp,
    	}
    }

    // 組裝
    g1801 := &game1801{
    	fixed:       f,
    	accWin:      0,                                                                                       // 累積贏分
    	maxWinLimit: 0,                                                                                       // 最高贏分上限
    	ext:         buildExtend1801(g.IsSim, g.gameSetting.GameModeSettingList[0].ScreenSetting.ScreenSize), // exts pool
    }

    return g1801

}

// 重置 game1801
func (g \*game1801) newspin() {
g.accWin = 0 // 重置累積贏分

}

// ============================================================
// ** 此遊戲需要的額外結構宣告: Fixed 設定宣告 **
// ============================================================

type fixed1801 struct {
fillScreenIdx []int // 每一軸要補盤的位置
nowfillReelStripsIdx []int // 補盤軸當下 idx
betmodes []betModes1801 // 儲存需要 Lut 處理後不同下注模式對應的權重/機率參數
screen []int16 // 盤面緩存，包含乘倍圖標資訊的盤面

    // 圖標類型快取
    symbolTypes []enum.SymbolType

    // 乘數索引清單
    multipilersIndex []int

    // 以下讀表
    FreeGameRounds  int           `yaml:"FreeGameRounds"`  // 基礎 Free spin 次數
    RetriggerRounds int           `yaml:"RetriggerRounds"` // 加局次數
    FreeMaxRounds   int           `yaml:"FreeMaxRounds"`   // FG 最大 spin 次數
    Multipilers     []int         `yaml:"Multipilers"`     // 乘數
    BetModes        []BetMode1801 `yaml:"BetModes"`        // 不同下注模式對應的權重/機率參數
    MultipilerLimit int           `yaml:"MultipilerLimit"` // 乘數清單
    ScatterPay      []int         `yaml:"ScatterPay"`      // Scatter 賠率清單

}

// 讀設定檔
type BetMode1801 struct {
// 後面的 `yaml:"BetMode"` 語法是 struct tag 告訴 YAML 解碼器這個欄位對應 YAML 檔裡的 key name。
BetMode int `yaml:"BetMode"`
BaseReelChooseWeight []int `yaml:"BaseReelChooseWeight"`
FreeReelChooseWeight []int `yaml:"FreeReelChooseWeight"`
BaseMultiProb []int `yaml:"BaseMultiProb"`
BaseMultiLvUp []int `yaml:"BaseMultiLvUp"`
FreeMultiProb []int `yaml:"FreeMultiProb"`
FreeMultiLvUp []int `yaml:"FreeMultiLvUp"`
}

// Lut 處理後
type betModes1801 struct {
betMode int // 押注模式
baseReelLut sampler.LUT // 主遊戲起始輪 id LUT 表
freeReelLut sampler.LUT
baseMultiProbLut sampler.LUT
baseMultiLvUp []int
freeMultiProbLut sampler.LUT
freeMultiLvUp []int
}

// base 升級乘數值
func (b *betModes1801) baseMultLvUp(core *core.Core, nowIdx int) (bool, int) {
prob := b.baseMultiLvUp[nowIdx]
if core.IntN(1000) < prob {
next := nowIdx + 1
return true, next
}
return false, nowIdx
}

// free 升級乘數值
func (b *betModes1801) freeMultLvUp(core *core.Core, nowIdx int) (bool, int) {
prob := b.freeMultiLvUp[nowIdx]
if core.IntN(1000) < prob {
next := nowIdx + 1
return true, next
}
return false, nowIdx
}

// ============================================================
// ** 此遊戲需要的額外結構宣告: extend 拓展結果格式宣告 **
// ============================================================

type extend1801 struct {

    // 乘數相關屬性
    Nowmulti      int   `json:"nowmulti,omitzero"`      // 當前盤面累積乘數
    MultiSymPos   []int `json:"multisympos,omitzero"`   // 乘數符號索引位置清單
    MultiSymMults []int `json:"multisymmults,omitzero"` // 乘數值清單
    // isLvUp        []bool // 升級狀態(todo)

    ScatterPay  int   `json:"ScatterPay,omitzero"`  // C1 獎金
    ScatterHits []int `json:"ScatterHits,omitzero"` // C1 中獎圖

    SymWin       int // 當前盤面贏分(不是累積)
    AccSymWin    int // 每 round 累積贏分(包含累積贏分)
    NowTotalMult int // (feature) FG 期間累積乘數

    isSim bool // 模擬模式

}

// 創建 extend1801 實例
func buildExtend1801(isSim bool, size int) \*extend1801 {
return &extend1801{
Nowmulti: 0,
MultiSymPos: make([]int, 0, size),
MultiSymMults: make([]int, 0, size),
// isLvUp: make([]bool, 0, size),
isSim: isSim,

    	ScatterPay:  0,
    	ScatterHits: make([]int, 0, size),
    }

}

// 實作介面
func (e \*extend1801) Reset() {
e.MultiSymPos = e.MultiSymPos[:0] // 每 round 乘數位置清單
e.MultiSymMults = e.MultiSymMults[:0] // 每 round 乘數值清單
e.Nowmulti = 0 // 每 round 累積乘數
e.AccSymWin = 0 // 每 round 累積純 "贏分符號"
e.ScatterPay = 0
e.ScatterHits = e.ScatterHits[:0]

}

// 實作介面
func (e \*extend1801) Snapshot() any {
if e.isSim {
return nil
}
r := &extend1801{
Nowmulti: e.Nowmulti,
MultiSymPos: append([]int(nil), e.MultiSymPos...),
MultiSymMults: append([]int(nil), e.MultiSymMults...),
isSim: e.isSim,
}
return r
}

// ============================================================
// ** 遊戲主邏輯入口 **
// ============================================================

// getResult 主要介面函數 回傳遊戲結果 *res.SpinResult
func (g *game1801) getResult(betMode int, betMult int, gh *GameHandler) *result.SpinResult {
g.maxWinLimit = gh.gameSetting.MaxWinLimit \* betMult // 最高累計贏分值
sr := gh.StartNewSpin(betMode, betMult)
// 重置 game1801
g.newspin()

    base := g.getBaseResult(betMode, betMult, gh)
    sr.AppendModeResult(base)

    if base.Trigger != 0 && g.accWin < g.maxWinLimit {
    	free := g.getFreeResult(betMode, betMult, gh)
    	sr.AppendModeResult(free)
    }

    sr.End()
    return sr

}

// ============================================================
// ** 遊戲中各模式內部邏輯實作 **
// ============================================================

func (g *game1801) getBaseResult(betMode int, betMult int, gh *GameHandler) \*result.GameModeResult {

    fix := g.fixed
    mode := gh.GameModeHandlerList[0]
    sg := mode.ScreenGenerator
    sc := mode.ScreenCalculator
    gmr := mode.GameModeResult
    ext := g.ext
    ext.Reset()  // 重置 ext
    g.resetIdx() // 重置補盤相關參數

    // 隨機選擇 betMode 下，某一組輪帶表的索引值
    reelStripPick := fix.betmodes[betMode].baseReelLut.Pick(gh.core)
    fillReelStrips := &mode.GameModeSetting.GenScreenSetting.ReelStripsGroup[reelStripPick] // 指定補盤軸

    // 1. 生成該round開局盤面
    screen := sg.GenScreenByAssignedReelStrip(reelStripPick)
    copy(fix.screen, screen)
    // 提交 畫面勳要盤面訊息，不需要 乘數值
    gmr.AddAct(result.FinishAct, "InitBaseGenScreen", screen, nil)

    // 取得本次補珠輪帶起始位置
    for i := 0; i < len(fix.fillScreenIdx); i++ {
    	fix.fillScreenIdx[i] = gh.core.IntN(len(fillReelStrips.ReelStripsReels[i].ReelSymbols))
    }

    for range 100 {
    	// 2. 算當前盤面 "得分符號" 贏分
    	// 這邊算完分之後會直接改 TmpAct 狀態
    	_ = sc.CalcScreen(betMult, screen, gmr)

    	// 獲取當前盤面得分符號的索引值
    	hm := gmr.HitMapTmp()

    	// 3. 取原始 win
    	ext.SymWin = gmr.GetTmpWin() // 先記當下贏分避免提交後要重找
    	gmr.UpdateTmpWin(0)          // 暫時不記入 gmr.TmpAct

    	// 4. 判斷是否結束消除掉落
    	// 兩種可能: "初始盤面"、"消除掉落至盤面" 沒有贏分組合
    	if ext.SymWin == 0 {
    		gmr.Trigger = g.trigger(screen)                                              // 計算 C1 數量，判斷要不要觸發 FG
    		ext.ScatterPay = fix.ScatterPay[gmr.Trigger] * betMult * gh.BetUnit[betMode] // 計算 C1 贏分
    		ext.AccSymWin += ext.ScatterPay                                              // 更新累積贏分

    		// 4.1 初始盤面沒有贏分組合
    		if ext.AccSymWin == 0 {
    			gmr.AddAct(result.FinishStep, "NoWinBaseScreen", screen, nil)
    			break
    		}

    		// 4.2 消除掉落至盤面沒有贏分組合
    		g.accWin = min(ext.AccSymWin*ext.Nowmulti, g.maxWinLimit)
    		gmr.UpdateTmpWin(g.accWin)
    		msg := "RoundWin"
    		if g.accWin == g.maxWinLimit {
    			msg = "MaxWin"
    		}
    		gmr.AddAct(result.FinishStep, msg, screen, ext)
    		break
    	}

    	// 更新累積贏分
    	ext.AccSymWin += ext.SymWin

    	// 5. 有贏分，更新乘數狀態 MultiSymPos、MultiSymMults、AccMulti
    	g.getBaseMulti(fix.screen, betMode, gh.core, ext)

    	// 6. 記錄下當下累積贏分&乘倍圖標資訊
    	gmr.AddAct(result.FinishAct, "StepWin", screen, ext)

    	// 7. 判斷是否要提升乘倍等級
    	for idx, pos := range ext.MultiSymPos {
    		mu := ext.MultiSymMults[idx]  // 目前乘倍
    		i := fix.multipilersIndex[mu] // 乘數索引

    		// 如果 乘數值索引 不是最後一個(最後一個沒得升)
    		if i < (len(fix.Multipilers) - 1) {
    			// 用機率決定要不要升到下一級，回傳 nextIdx
    			up, nextIdx := fix.betmodes[betMode].baseMultLvUp(gh.core, i)
    			if up {
    				fix.screen[pos] = int16(100 + fix.Multipilers[nextIdx]) // 把乘倍標記放到盤面上
    			}
    		}
    	}
    	// 8. 消除掉落
    	fix.screen = g.gravity(fix.screen, hm, sg.Cols, sg.Rows, fix.fillScreenIdx)

    	// screen 同步消除掉落
    	for i, s := range fix.screen {
    		// 大於 100 代表是乘數值
    		if s > 100 {
    			screen[i] = 1
    		} else {
    			screen[i] = s
    		}
    	}

    	// 9. 提交 step 結果(step結束)(包含消除掉落盤面以及是否乘倍圖標升級資訊)
    	gmr.AddAct(result.FinishStep, "Gravity", screen, ext) // 消除掉落盤面

    	// 10. 補滿盤面
    	screen = g.fillScreen(screen, fillReelStrips, fix.fillScreenIdx, fix.nowfillReelStripsIdx, sg.Cols)

    	// 補 fix.screen 盤面
    	for pos, sym := range fix.screen {
    		if sym == 0 {
    			fix.screen[pos] = screen[pos]
    		}
    	}

    	// 提交 act 因為盤面改變了
    	gmr.AddAct(result.FinishAct, "FillScreen", screen, nil)

    }

    // 結束這 round
    gmr.FinishRound()
    return mode.YieldResult()

}

func (g *game1801) getFreeResult(betMode int, betMult int, gh *GameHandler) \*result.GameModeResult {
mode := gh.GameModeHandlerList[1]
sg := mode.ScreenGenerator
sc := mode.ScreenCalculator
gmr := mode.GameModeResult
nowLimitRounds := g.fixed.FreeGameRounds
fix := g.fixed
ext := g.ext // 取 ext
ext.NowTotalMult = 0 // 整個 FG 累積乘數

    // 進行 n 局 FG spins
    for i := 0; i < nowLimitRounds; i++ {
    	ext.Reset()  // 重置每 round 累積乘數、贏分狀態
    	g.resetIdx() // 重置 "補盤"
    	reelStripPick := fix.betmodes[betMode].freeReelLut.Pick(gh.core)
    	fillReelStrips := &mode.GameModeSetting.GenScreenSetting.ReelStripsGroup[reelStripPick] // 指定補盤軸

    	// baseAccWin := g.accWin // 暫時儲存 從 base game 來的 累積贏分值

    	// 1. 生成該round開局盤面
    	screen := sg.GenScreenByAssignedReelStrip(reelStripPick)
    	copy(fix.screen, screen)
    	// 提交 畫面勳要盤面訊息，不需要 乘數值
    	gmr.AddAct(result.FinishAct, "InitFreeGenScreen", screen, nil)
    	// 消除掉落
    	for range 100 {
    		// 2. 算分
    		_ = sc.CalcScreen(betMult, screen, gmr)
    		// 獲取當前盤面得分符號的索引值
    		hm := gmr.HitMapTmp()

    		// 3. 取原始 win
    		ext.SymWin = gmr.GetTmpWin() // 先記當下贏分避免提交後要重找
    		gmr.UpdateTmpWin(0)          // 暫時不記入 gmr.TmpAct

    		// 4. 準備結束這局 (round)
    		if ext.SymWin == 0 {
    			c1Count := g.reTrigger(screen) // // 計算 C1 數量，判斷要不要觸發加局

    			if c1Count != 0 {
    				nowLimitRounds = min(nowLimitRounds+5, 100)
    				ext.ScatterPay = fix.ScatterPay[c1Count] * betMult * gh.BetUnit[betMode] // 計算 C1 贏分
    				ext.AccSymWin += ext.ScatterPay
    			}

    			if ext.AccSymWin == 0 {
    				gmr.AddAct(result.FinishStep, "NoWinFreeScreen", screen, nil)
    				break
    			}

    			// 更新 FG 特色累積乘數值
    			if ext.Nowmulti > 0 {
    				ext.NowTotalMult += ext.Nowmulti            // 更新 FG 特色: 累積乘數
    				ext.NowTotalMult = min(51000, ext.Nowmulti) // 最高 51000
    			}

    			// 4.2 消除掉落至盤面沒有贏分組合
    			g.accWin = min(ext.AccSymWin*(ext.Nowmulti+ext.NowTotalMult), g.maxWinLimit)
    			gmr.UpdateTmpWin(g.accWin)
    			msg := "RoundWin"
    			if g.accWin == g.maxWinLimit {
    				msg = "MaxWin"
    			}
    			gmr.AddAct(result.FinishStep, msg, screen, ext)
    			break
    		}

    		// 更新累積贏分
    		ext.AccSymWin += ext.SymWin

    		// 5. 計算乘倍，更新乘數狀態 MultiSymPos、MultiSymMults、AccMulti
    		g.getFreeMulti(fix.screen, betMode, gh.core, ext)

    		// 6. 記錄下當下累積贏分&乘倍圖標資訊
    		gmr.AddAct(result.FinishAct, "StepWin", screen, ext)

    		// 7. 判斷是否要提升乘倍等級
    		for idx, pos := range ext.MultiSymPos {
    			mu := ext.MultiSymMults[idx]  // 目前乘倍
    			i := fix.multipilersIndex[mu] // 乘數索引

    			if i < (len(fix.Multipilers) - 1) {
    				// 用機率決定要不要升到下一級，回傳 nextIdx
    				up, nextIdx := fix.betmodes[betMode].freeMultLvUp(gh.core, i)
    				if up {
    					fix.screen[pos] = int16(100 + fix.Multipilers[nextIdx]) // 把乘倍標記放到盤面上
    				}
    			}
    		}

    		// 8. 消除掉落
    		fix.screen = g.gravity(fix.screen, hm, sg.Cols, sg.Rows, fix.fillScreenIdx)

    		for i, s := range fix.screen {
    			if s > 100 {
    				screen[i] = 1
    			} else {
    				screen[i] = s
    			}
    		}

    		// 9. 提交 step 結果 (step 結束)
    		gmr.AddAct(result.FinishStep, "Gravity", screen, nil) // 消除掉落盤面

    		// 10. 補滿盤面
    		screen = g.fillScreen(screen, fillReelStrips, g.fixed.fillScreenIdx, g.fixed.nowfillReelStripsIdx, sg.Cols)
    		for pos, sym := range fix.screen {
    			if sym == 0 {
    				fix.screen[pos] = screen[pos]
    			}
    		}

    		// 提交 act 因為盤面改變了
    		gmr.AddAct(result.FinishAct, "FillScreen", screen, ext)
    	}

    	gmr.FinishRound()
    }
    return mode.YieldResult()

}

// ============================================================
// ** 遊戲內部輔助函數實作 **
// ============================================================

// 0 代表不觸發 > 0 各自觸發
func (g \*game1801) trigger(screen []int16) int {
st := g.fixed.symbolTypes
count := 0
ext := g.ext

    for pos, sym := range screen {
    	if st[sym] == enum.SymbolTypeScatter {
    		ext.ScatterHits = append(ext.ScatterHits, pos)
    		count++
    	}
    }

    if count < 4 {
    	ext.ScatterHits = ext.ScatterHits[:0]
    	return 0
    }

    return min(count, 6)

}

func (g \*game1801) reTrigger(screen []int16) int {
st := g.fixed.symbolTypes
count := 0

    for _, sym := range screen {
    	if st[sym] == enum.SymbolTypeScatter {
    		count++
    	}
    }

    if count < 3 {
    	return 0
    }

    return min(count, 6)

}

// 重力掉落函數
func (g *game1801) gravity(screen []int16, hitmap []int16, cols int, rows int, buf []int) []int16 {
// 先把要消除的地方改 0
for \_, v := range hitmap {
screen[v] = 0
}
// 逐欄由下而上做「就地壓縮」：
// wp = write pointer（寫入位置，從底部往上移），
// rp = read pointer（讀取位置，從底部往上掃）。
for c := 0; c < cols; c++ {
wp := (rows-1)*cols + c // 最底部該欄位索引
// 將非 0 元素往下疊，保持欄內相對順序（穩定）
for r := rows - 1; r >= 0; r-- {
rp := r\*cols + c
if screen[rp] != 0 {
if rp != wp {
screen[wp] = screen[rp]
}
wp -= cols
}
}
buf[c] = wp // 記錄下第 c 軸要補的位置
// 上方殘餘位置補 0
for w := wp; w >= 0; w -= cols {
screen[w] = 0
}
}
return screen
}

func (g *game1801) fillScreen(screen []int16, reels *settings.ReelStrips, fillScreenIdx []int, nowfillReelStripsIdx []int, cols int) []int16 {
for c, r := range fillScreenIdx {
idx := nowfillReelStripsIdx[c]
reel := reels.ReelStripsReels[c]
for w := r; w >= 0; w -= cols {
if idx < 0 {
idx = reel.ReelLength - 1
}
screen[w] = int16(reel.ReelSymbols[idx])
idx--
}
nowfillReelStripsIdx[c] = idx
}
return screen
}

// 重置 game1801 參數
func (g \*game1801) resetIdx() {
for i := 0; i < len(g.fixed.fillScreenIdx); i++ {
g.fixed.fillScreenIdx[i] = 0
g.fixed.nowfillReelStripsIdx[i] = 0
}
}

// 對當前盤面中的乘數值做更新，三種可能:
// 1. 符號值 不等於 1 也不大於 100 保持原樣就好
// 2. 符號值 等於 1 代表他是新的乘數符號，給他一個大於 100 的
// 3. 符號值 大於 100
func (g *game1801) getBaseMulti(screen []int16, betMode int, core *core.Core, ext \*extend1801) {
multiGetter := g.fixed.betmodes[betMode]
for pos, sym := range screen {
// 如果它是新的乘數值
if sym == 1 {
multIdx := multiGetter.baseMultiProbLut.Pick(core) // 隨機選擇一個乘數值
mult := g.fixed.Multipilers[multIdx]

    		g.fixed.screen[pos] = int16(100 + mult) // 把乘倍標記放到盤面上

    		ext.MultiSymPos = append(ext.MultiSymPos, pos)
    		ext.MultiSymMults = append(ext.MultiSymMults, mult)
    		ext.Nowmulti += mult
    	}

    	// 如果它是舊的乘數值
    	if sym > 100 {
    		mult := int(sym) - 100
    		ext.Nowmulti += mult
    	}
    }

}

func (g *game1801) getFreeMulti(screen []int16, betMode int, core *core.Core, ext \*extend1801) {
multiGetter := g.fixed.betmodes[betMode]
for pos, sym := range screen {
if sym == 1 {
multIdx := multiGetter.freeMultiProbLut.Pick(core)
mult := g.fixed.Multipilers[multIdx]

    		g.fixed.screen[pos] = int16(100 + mult) // 把乘倍標記放到盤面上

    		ext.MultiSymPos = append(ext.MultiSymPos, pos)
    		ext.MultiSymMults = append(ext.MultiSymMults, mult)
    		ext.Nowmulti += mult
    	}
    	if sym > 100 {
    		mult := int(sym) - 100
    		ext.Nowmulti += mult
    	}
    }

}

# [文件網址] None

# [玩法說明] None

# 遊戲名稱 : 1801 | StormOfSeth | 戰神賽特

GameName: StormOfSeth

# 押注基本單位

BetUnit : [20,2000]

# 最大贏分(對應 BetUnit)

MaxWinLimit : 200000

# 遊戲模式設定列表，一個遊戲模式相當於一個狀態，遊戲將在各狀態間轉換

GameModeSettingList: - # GameModeSetting[0]: BaseGame 設定 # 盤面設定
ScreenSetting:
columns: 6
rows: 5
damp: 1 # 生成盤面設定
GenScreenSetting:
GenReelType: GenReelByReelIdx
ReelStripsGroup:  
 - # ReelStrip[0]
weight : 1
reels : - # Reel[0]
symbols : [9, 5, 9, 7, 7, 9, 5, 6, 9, 7, 3, 8, 7, 4, 4, 6, 6, 7, 6, 8, 8, 4, 8, 9, 4, 8, 9, 4, 5, 9, 7, 8, 7, 8, 4, 8, 7, 9, 6, 6, 7, 8, 9, 7, 8, 5, 8, 9, 5, 5, 7, 5, 6, 8, 3, 9, 7, 9, 9, 4, 3, 7, 3, 6, 3, 5, 7, 1, 3, 4, 5, 1, 5, 9, 8, 5, 4, 7, 8, 8, 5, 9, 9, 5, 8, 9, 8, 7, 5, 9, 5, 9, 4, 1, 8, 9, 7, 7, 3, 6, 9, 7, 7, 6, 2, 4, 8, 7, 9, 3, 9, 4, 5, 9, 8, 9, 8, 7, 4, 9, 6, 4, 9, 4, 7, 3, 9, 3, 4, 8, 1, 8, 9, 4, 8, 9, 7]
weights : [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1] - # Reel[1]
symbols : [5, 9, 8, 8, 4, 9, 5, 7, 5, 9, 9, 7, 3, 9, 6, 4, 1, 4, 9, 7, 5, 7, 9, 9, 8, 6, 4, 5, 5, 3, 7, 8, 8, 3, 8, 7, 8, 6, 5, 9, 7, 9, 7, 4, 7, 4, 8, 6, 7, 9, 4, 9, 7, 7, 8, 9, 8, 7, 7, 5, 8, 3, 9, 5, 5, 9, 8, 4, 9, 8, 1, 6, 7, 9, 4, 8, 5, 7, 7, 4, 9, 8, 2, 7, 1, 5, 3, 8, 8, 3, 8, 6, 9, 9, 9, 7, 6, 8, 7, 9, 9, 3, 7, 6, 4, 4, 4, 6, 8, 7, 8, 9, 9, 8, 7, 4, 4, 9, 9, 8, 3, 3, 8, 5, 5, 9, 7, 6, 9, 1, 4, 3, 4, 5, 6, 5, 9]
weights : [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1] - # Reel[2]
symbols : [7, 2, 7, 6, 7, 8, 8, 9, 4, 5, 9, 5, 8, 9, 3, 9, 7, 9, 4, 9, 6, 9, 8, 9, 6, 3, 7, 1, 4, 4, 7, 9, 1, 8, 6, 7, 7, 9, 7, 4, 9, 7, 5, 8, 5, 4, 9, 8, 5, 9, 8, 7, 3, 9, 6, 7, 7, 9, 7, 7, 7, 9, 4, 4, 3, 5, 5, 3, 4, 9, 5, 4, 8, 3, 9, 5, 7, 8, 8, 8, 7, 8, 6, 5, 4, 9, 8, 8, 9, 6, 9, 3, 9, 3, 6, 6, 7, 8, 6, 3, 4, 9, 3, 8, 4, 8, 5, 9, 5, 5, 6, 4, 8, 5, 9, 7, 1, 4, 8, 8, 9, 1, 9, 5, 8, 8, 4, 9, 7, 8, 7, 7, 9, 4, 9, 5, 7]
weights : [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1] - # Reel[3]
symbols : [6, 4, 9, 7, 6, 5, 5, 8, 7, 8, 4, 4, 6, 3, 9, 8, 4, 7, 4, 7, 9, 4, 9, 1, 4, 6, 8, 6, 9, 5, 7, 7, 8, 5, 5, 6, 8, 9, 3, 6, 3, 9, 1, 5, 9, 3, 7, 3, 4, 6, 9, 5, 3, 4, 8, 9, 2, 7, 3, 8, 9, 8, 8, 9, 5, 9, 5, 9, 9, 9, 4, 6, 5, 8, 9, 8, 9, 9, 3, 7, 9, 7, 3, 9, 7, 5, 7, 8, 8, 8, 8, 5, 6, 9, 7, 7, 7, 8, 9, 8, 9, 1, 4, 9, 8, 5, 5, 9, 9, 7, 1, 4, 7, 8, 7, 7, 4, 7, 8, 4, 4, 9, 9, 4, 7, 4, 5, 8, 9, 8, 7, 5, 7, 3, 7, 6, 8]
weights : [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1] - # Reel[4]
symbols : [1, 8, 7, 9, 6, 9, 9, 7, 4, 5, 9, 8, 5, 4, 9, 9, 5, 8, 9, 7, 3, 8, 4, 8, 3, 7, 4, 9, 4, 8, 8, 3, 8, 4, 9, 9, 8, 7, 3, 9, 3, 9, 7, 9, 4, 9, 4, 7, 6, 9, 9, 6, 4, 5, 3, 6, 4, 5, 7, 7, 8, 3, 5, 6, 5, 8, 7, 5, 4, 5, 8, 7, 9, 1, 7, 6, 5, 4, 6, 8, 8, 7, 9, 7, 4, 9, 7, 6, 8, 8, 9, 5, 9, 7, 3, 7, 9, 7, 9, 5, 9, 8, 7, 1, 4, 4, 3, 8, 7, 7, 1, 8, 2, 5, 9, 5, 8, 9, 5, 6, 3, 7, 7, 8, 9, 9, 7, 4, 4, 8, 5, 6, 9, 9, 8, 6, 8]
weights : [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1] - # Reel[5]
symbols : [1, 8, 7, 9, 6, 9, 9, 7, 4, 5, 9, 8, 5, 4, 9, 9, 5, 8, 9, 7, 3, 8, 4, 8, 3, 7, 4, 9, 4, 8, 8, 3, 8, 4, 9, 9, 8, 7, 3, 9, 3, 9, 7, 9, 4, 9, 4, 7, 6, 9, 9, 6, 4, 5, 3, 6, 4, 5, 7, 7, 8, 3, 5, 6, 5, 8, 7, 5, 4, 5, 8, 7, 9, 1, 7, 6, 5, 4, 6, 8, 8, 7, 9, 7, 4, 9, 7, 6, 8, 8, 9, 5, 9, 7, 3, 7, 9, 7, 9, 5, 9, 8, 7, 1, 4, 4, 3, 8, 7, 7, 1, 8, 2, 5, 9, 5, 8, 9, 5, 6, 3, 7, 7, 8, 9, 9, 7, 4, 4, 8, 5, 6, 9, 9, 8, 6, 8]
weights : [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1] - # ReelStrip[1]
weight : 0
reels : - # Reel[0]
symbols : [1, 8, 7, 9, 6, 9, 9, 7, 4, 5, 9, 8, 5, 4, 9, 9, 5, 8, 9, 7, 3, 8, 4, 8, 3, 7, 4, 9, 4, 8, 8, 3, 8, 4, 9, 9, 8, 7, 3, 9, 3, 9, 7, 9, 4, 9, 4, 7, 6, 9, 9, 6, 4, 5, 3, 6, 4, 5, 7, 7, 8, 3, 5, 6, 5, 8, 7, 5, 4, 5, 8, 7, 9, 1, 7, 6, 5, 4, 6, 8, 8, 7, 9, 7, 4, 9, 7, 6, 8, 8, 9, 5, 9, 7, 3, 7, 9, 7, 9, 5, 9, 8, 7, 1, 4, 4, 3, 8, 7, 7, 1, 8, 2, 5, 9, 5, 8, 9, 5, 6, 3, 7, 7, 8, 9, 9, 7, 4, 4, 8, 5, 6, 9, 9, 8, 6, 8]
weights : [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1] - # Reel[1]
symbols : [1, 8, 7, 9, 6, 9, 9, 7, 4, 5, 9, 8, 5, 4, 9, 9, 5, 8, 9, 7, 3, 8, 4, 8, 3, 7, 4, 9, 4, 8, 8, 3, 8, 4, 9, 9, 8, 7, 3, 9, 3, 9, 7, 9, 4, 9, 4, 7, 6, 9, 9, 6, 4, 5, 3, 6, 4, 5, 7, 7, 8, 3, 5, 6, 5, 8, 7, 5, 4, 5, 8, 7, 9, 1, 7, 6, 5, 4, 6, 8, 8, 7, 9, 7, 4, 9, 7, 6, 8, 8, 9, 5, 9, 7, 3, 7, 9, 7, 9, 5, 9, 8, 7, 1, 4, 4, 3, 8, 7, 7, 1, 8, 2, 5, 9, 5, 8, 9, 5, 6, 3, 7, 7, 8, 9, 9, 7, 4, 4, 8, 5, 6, 9, 9, 8, 6, 8]
weights : [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1] - # Reel[2]
symbols : [1, 8, 7, 9, 6, 9, 9, 7, 4, 5, 9, 8, 5, 4, 9, 9, 5, 8, 9, 7, 3, 8, 4, 8, 3, 7, 4, 9, 4, 8, 8, 3, 8, 4, 9, 9, 8, 7, 3, 9, 3, 9, 7, 9, 4, 9, 4, 7, 6, 9, 9, 6, 4, 5, 3, 6, 4, 5, 7, 7, 8, 3, 5, 6, 5, 8, 7, 5, 4, 5, 8, 7, 9, 1, 7, 6, 5, 4, 6, 8, 8, 7, 9, 7, 4, 9, 7, 6, 8, 8, 9, 5, 9, 7, 3, 7, 9, 7, 9, 5, 9, 8, 7, 1, 4, 4, 3, 8, 7, 7, 1, 8, 2, 5, 9, 5, 8, 9, 5, 6, 3, 7, 7, 8, 9, 9, 7, 4, 4, 8, 5, 6, 9, 9, 8, 6, 8]
weights : [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1] - # Reel[3]
symbols : [1, 8, 7, 9, 6, 9, 9, 7, 4, 5, 9, 8, 5, 4, 9, 9, 5, 8, 9, 7, 3, 8, 4, 8, 3, 7, 4, 9, 4, 8, 8, 3, 8, 4, 9, 9, 8, 7, 3, 9, 3, 9, 7, 9, 4, 9, 4, 7, 6, 9, 9, 6, 4, 5, 3, 6, 4, 5, 7, 7, 8, 3, 5, 6, 5, 8, 7, 5, 4, 5, 8, 7, 9, 1, 7, 6, 5, 4, 6, 8, 8, 7, 9, 7, 4, 9, 7, 6, 8, 8, 9, 5, 9, 7, 3, 7, 9, 7, 9, 5, 9, 8, 7, 1, 4, 4, 3, 8, 7, 7, 1, 8, 2, 5, 9, 5, 8, 9, 5, 6, 3, 7, 7, 8, 9, 9, 7, 4, 4, 8, 5, 6, 9, 9, 8, 6, 8]
weights : [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1] - # Reel[4]
symbols : [1, 8, 7, 9, 6, 9, 9, 7, 4, 5, 9, 8, 5, 4, 9, 9, 5, 8, 9, 7, 3, 8, 4, 8, 3, 7, 4, 9, 4, 8, 8, 3, 8, 4, 9, 9, 8, 7, 3, 9, 3, 9, 7, 9, 4, 9, 4, 7, 6, 9, 9, 6, 4, 5, 3, 6, 4, 5, 7, 7, 8, 3, 5, 6, 5, 8, 7, 5, 4, 5, 8, 7, 9, 1, 7, 6, 5, 4, 6, 8, 8, 7, 9, 7, 4, 9, 7, 6, 8, 8, 9, 5, 9, 7, 3, 7, 9, 7, 9, 5, 9, 8, 7, 1, 4, 4, 3, 8, 7, 7, 1, 8, 2, 5, 9, 5, 8, 9, 5, 6, 3, 7, 7, 8, 9, 9, 7, 4, 4, 8, 5, 6, 9, 9, 8, 6, 8]
weights : [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1] - # Reel[5]
symbols : [1, 8, 7, 9, 6, 9, 9, 7, 4, 5, 9, 8, 5, 4, 9, 9, 5, 8, 9, 7, 3, 8, 4, 8, 3, 7, 4, 9, 4, 8, 8, 3, 8, 4, 9, 9, 8, 7, 3, 9, 3, 9, 7, 9, 4, 9, 4, 7, 6, 9, 9, 6, 4, 5, 3, 6, 4, 5, 7, 7, 8, 3, 5, 6, 5, 8, 7, 5, 4, 5, 8, 7, 9, 1, 7, 6, 5, 4, 6, 8, 8, 7, 9, 7, 4, 9, 7, 6, 8, 8, 9, 5, 9, 7, 3, 7, 9, 7, 9, 5, 9, 8, 7, 1, 4, 4, 3, 8, 7, 7, 1, 8, 2, 5, 9, 5, 8, 9, 5, 6, 3, 7, 7, 8, 9, 9, 7, 4, 4, 8, 5, 6, 9, 9, 8, 6, 8]
weights : [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1] - # ReelStrip[2]
weight : 0
reels : - # Reel[0]
symbols : [6, 7, 6, 7, 7, 2, 7, 6, 5, 4, 3, 5, 4, 9, 9, 5]
weights : [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]  
 - # Reel[1]
symbols : [6, 7, 6, 7, 7, 2, 7, 6, 5, 4, 3, 5, 4, 9, 9, 5]
weights : [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]  
 - # Reel[2]
symbols : [6, 7, 6, 7, 7, 2, 7, 6, 5, 4, 3, 5, 4, 9, 9, 5]
weights : [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  
 - # Reel[3]
symbols : [6, 7, 6, 7, 7, 2, 7, 6, 5, 4, 3, 5, 4, 9, 9, 5]
weights : [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  
 - # Reel[4]
symbols : [6, 7, 6, 7, 7, 2, 7, 6, 5, 4, 3, 5, 4, 9, 9, 5]
weights : [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  
 - # Reel[5]
symbols : [6, 7, 6, 7, 7, 2, 7, 6, 5, 4, 3, 5, 4, 9, 9, 5]
weights : [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

      # 圖標設定
      SymbolSetting:
          symbolUsed : [Z1,S1,C1,H1,H2,H3,H4,L1,L2,L3,L4,L5]
          payTable :
              - [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
              - [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
              - [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
              - [0, 0, 0, 0, 0, 0, 0, 200, 200, 500, 500, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000]
              - [0, 0, 0, 0, 0, 0, 0, 50, 50, 200, 200, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500]
              - [0, 0, 0, 0, 0, 0, 0, 40, 40, 100, 100, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300]
              - [0, 0, 0, 0, 0, 0, 0, 30, 30, 40, 40, 240, 240, 240, 240, 240, 240, 240, 240, 240, 240, 240, 240, 240, 240, 240, 240, 240, 240, 240]
              - [0, 0, 0, 0, 0, 0, 0, 20, 20, 30, 30, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200]
              - [0, 0, 0, 0, 0, 0, 0, 16, 16, 24, 24, 160, 160, 160, 160, 160, 160, 160, 160, 160, 160, 160, 160, 160, 160, 160, 160, 160, 160, 160]
              - [0, 0, 0, 0, 0, 0, 0, 10, 10, 20, 20, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100]
              - [0, 0, 0, 0, 0, 0, 0, 8, 8, 18, 18, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80]
              - [0, 0, 0, 0, 0, 0, 0, 5, 5, 15, 15, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40]

      # 中獎設定
      HitSetting:
          betType: BetTypeCollect
          lineTable:


    - # GameModeSetting[1]: FreeGame 設定
      # 盤面設定
      ScreenSetting:
          columns: 6
          rows: 5
          damp: 1
      # 生成盤面設定
      GenScreenSetting:
          GenReelType: GenReelByReelIdx
          ReelStripsGroup:
              - # ReelStrip[0]
                weight : 1
                reels :
                  - # Reel[0]
                    symbols : [1, 8, 7, 9, 6, 9, 9, 7, 4, 5, 9, 8, 5, 4, 9, 9, 5, 8, 9, 7, 3, 8, 4, 8, 3, 7, 4, 9, 4, 8, 8, 3, 8, 4, 9, 9, 8, 7, 3, 9, 3, 9, 7, 9, 4, 9, 4, 7, 6, 9, 9, 6, 4, 5, 3, 6, 4, 5, 7, 7, 8, 3, 5, 6, 5, 8, 7, 5, 4, 5, 8, 7, 9, 1, 7, 6, 5, 4, 6, 8, 8, 7, 9, 7, 4, 9, 7, 6, 8, 8, 9, 5, 9, 7, 3, 7, 9, 7, 9, 5, 9, 8, 7, 1, 4, 4, 3, 8, 7, 7, 1, 8, 2, 5, 9, 5, 8, 9, 5, 6, 3, 7, 7, 8, 9, 9, 7, 4, 4, 8, 5, 6, 9, 9, 8, 6, 8]
                    weights : [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
                  - # Reel[1]
                    symbols : [1, 8, 7, 9, 6, 9, 9, 7, 4, 5, 9, 8, 5, 4, 9, 9, 5, 8, 9, 7, 3, 8, 4, 8, 3, 7, 4, 9, 4, 8, 8, 3, 8, 4, 9, 9, 8, 7, 3, 9, 3, 9, 7, 9, 4, 9, 4, 7, 6, 9, 9, 6, 4, 5, 3, 6, 4, 5, 7, 7, 8, 3, 5, 6, 5, 8, 7, 5, 4, 5, 8, 7, 9, 1, 7, 6, 5, 4, 6, 8, 8, 7, 9, 7, 4, 9, 7, 6, 8, 8, 9, 5, 9, 7, 3, 7, 9, 7, 9, 5, 9, 8, 7, 1, 4, 4, 3, 8, 7, 7, 1, 8, 2, 5, 9, 5, 8, 9, 5, 6, 3, 7, 7, 8, 9, 9, 7, 4, 4, 8, 5, 6, 9, 9, 8, 6, 8]
                    weights : [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
                  - # Reel[2]
                    symbols : [1, 8, 7, 9, 6, 9, 9, 7, 4, 5, 9, 8, 5, 4, 9, 9, 5, 8, 9, 7, 3, 8, 4, 8, 3, 7, 4, 9, 4, 8, 8, 3, 8, 4, 9, 9, 8, 7, 3, 9, 3, 9, 7, 9, 4, 9, 4, 7, 6, 9, 9, 6, 4, 5, 3, 6, 4, 5, 7, 7, 8, 3, 5, 6, 5, 8, 7, 5, 4, 5, 8, 7, 9, 1, 7, 6, 5, 4, 6, 8, 8, 7, 9, 7, 4, 9, 7, 6, 8, 8, 9, 5, 9, 7, 3, 7, 9, 7, 9, 5, 9, 8, 7, 1, 4, 4, 3, 8, 7, 7, 1, 8, 2, 5, 9, 5, 8, 9, 5, 6, 3, 7, 7, 8, 9, 9, 7, 4, 4, 8, 5, 6, 9, 9, 8, 6, 8]
                    weights : [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
                  - # Reel[3]
                    symbols : [1, 8, 7, 9, 6, 9, 9, 7, 4, 5, 9, 8, 5, 4, 9, 9, 5, 8, 9, 7, 3, 8, 4, 8, 3, 7, 4, 9, 4, 8, 8, 3, 8, 4, 9, 9, 8, 7, 3, 9, 3, 9, 7, 9, 4, 9, 4, 7, 6, 9, 9, 6, 4, 5, 3, 6, 4, 5, 7, 7, 8, 3, 5, 6, 5, 8, 7, 5, 4, 5, 8, 7, 9, 1, 7, 6, 5, 4, 6, 8, 8, 7, 9, 7, 4, 9, 7, 6, 8, 8, 9, 5, 9, 7, 3, 7, 9, 7, 9, 5, 9, 8, 7, 1, 4, 4, 3, 8, 7, 7, 1, 8, 2, 5, 9, 5, 8, 9, 5, 6, 3, 7, 7, 8, 9, 9, 7, 4, 4, 8, 5, 6, 9, 9, 8, 6, 8]
                    weights : [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
                  - # Reel[4]
                    symbols : [1, 8, 7, 9, 6, 9, 9, 7, 4, 5, 9, 8, 5, 4, 9, 9, 5, 8, 9, 7, 3, 8, 4, 8, 3, 7, 4, 9, 4, 8, 8, 3, 8, 4, 9, 9, 8, 7, 3, 9, 3, 9, 7, 9, 4, 9, 4, 7, 6, 9, 9, 6, 4, 5, 3, 6, 4, 5, 7, 7, 8, 3, 5, 6, 5, 8, 7, 5, 4, 5, 8, 7, 9, 1, 7, 6, 5, 4, 6, 8, 8, 7, 9, 7, 4, 9, 7, 6, 8, 8, 9, 5, 9, 7, 3, 7, 9, 7, 9, 5, 9, 8, 7, 1, 4, 4, 3, 8, 7, 7, 1, 8, 2, 5, 9, 5, 8, 9, 5, 6, 3, 7, 7, 8, 9, 9, 7, 4, 4, 8, 5, 6, 9, 9, 8, 6, 8]
                    weights : [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
                  - # Reel[5]
                    symbols : [1, 8, 7, 9, 6, 9, 9, 7, 4, 5, 9, 8, 5, 4, 9, 9, 5, 8, 9, 7, 3, 8, 4, 8, 3, 7, 4, 9, 4, 8, 8, 3, 8, 4, 9, 9, 8, 7, 3, 9, 3, 9, 7, 9, 4, 9, 4, 7, 6, 9, 9, 6, 4, 5, 3, 6, 4, 5, 7, 7, 8, 3, 5, 6, 5, 8, 7, 5, 4, 5, 8, 7, 9, 1, 7, 6, 5, 4, 6, 8, 8, 7, 9, 7, 4, 9, 7, 6, 8, 8, 9, 5, 9, 7, 3, 7, 9, 7, 9, 5, 9, 8, 7, 1, 4, 4, 3, 8, 7, 7, 1, 8, 2, 5, 9, 5, 8, 9, 5, 6, 3, 7, 7, 8, 9, 9, 7, 4, 4, 8, 5, 6, 9, 9, 8, 6, 8]
                    weights : [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
              - # ReelStrip[1]
                weight : 0
                reels :
                  - # Reel[0]
                    symbols : [1, 8, 7, 9, 6, 9, 9, 7, 4, 5, 9, 8, 5, 4, 9, 9, 5, 8, 9, 7, 3, 8, 4, 8, 3, 7, 4, 9, 4, 8, 8, 3, 8, 4, 9, 9, 8, 7, 3, 9, 3, 9, 7, 9, 4, 9, 4, 7, 6, 9, 9, 6, 4, 5, 3, 6, 4, 5, 7, 7, 8, 3, 5, 6, 5, 8, 7, 5, 4, 5, 8, 7, 9, 1, 7, 6, 5, 4, 6, 8, 8, 7, 9, 7, 4, 9, 7, 6, 8, 8, 9, 5, 9, 7, 3, 7, 9, 7, 9, 5, 9, 8, 7, 1, 4, 4, 3, 8, 7, 7, 1, 8, 2, 5, 9, 5, 8, 9, 5, 6, 3, 7, 7, 8, 9, 9, 7, 4, 4, 8, 5, 6, 9, 9, 8, 6, 8]
                    weights : [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
                  - # Reel[1]
                    symbols : [1, 8, 7, 9, 6, 9, 9, 7, 4, 5, 9, 8, 5, 4, 9, 9, 5, 8, 9, 7, 3, 8, 4, 8, 3, 7, 4, 9, 4, 8, 8, 3, 8, 4, 9, 9, 8, 7, 3, 9, 3, 9, 7, 9, 4, 9, 4, 7, 6, 9, 9, 6, 4, 5, 3, 6, 4, 5, 7, 7, 8, 3, 5, 6, 5, 8, 7, 5, 4, 5, 8, 7, 9, 1, 7, 6, 5, 4, 6, 8, 8, 7, 9, 7, 4, 9, 7, 6, 8, 8, 9, 5, 9, 7, 3, 7, 9, 7, 9, 5, 9, 8, 7, 1, 4, 4, 3, 8, 7, 7, 1, 8, 2, 5, 9, 5, 8, 9, 5, 6, 3, 7, 7, 8, 9, 9, 7, 4, 4, 8, 5, 6, 9, 9, 8, 6, 8]
                    weights : [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
                  - # Reel[2]
                    symbols : [1, 8, 7, 9, 6, 9, 9, 7, 4, 5, 9, 8, 5, 4, 9, 9, 5, 8, 9, 7, 3, 8, 4, 8, 3, 7, 4, 9, 4, 8, 8, 3, 8, 4, 9, 9, 8, 7, 3, 9, 3, 9, 7, 9, 4, 9, 4, 7, 6, 9, 9, 6, 4, 5, 3, 6, 4, 5, 7, 7, 8, 3, 5, 6, 5, 8, 7, 5, 4, 5, 8, 7, 9, 1, 7, 6, 5, 4, 6, 8, 8, 7, 9, 7, 4, 9, 7, 6, 8, 8, 9, 5, 9, 7, 3, 7, 9, 7, 9, 5, 9, 8, 7, 1, 4, 4, 3, 8, 7, 7, 1, 8, 2, 5, 9, 5, 8, 9, 5, 6, 3, 7, 7, 8, 9, 9, 7, 4, 4, 8, 5, 6, 9, 9, 8, 6, 8]
                    weights : [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
                  - # Reel[3]
                    symbols : [1, 8, 7, 9, 6, 9, 9, 7, 4, 5, 9, 8, 5, 4, 9, 9, 5, 8, 9, 7, 3, 8, 4, 8, 3, 7, 4, 9, 4, 8, 8, 3, 8, 4, 9, 9, 8, 7, 3, 9, 3, 9, 7, 9, 4, 9, 4, 7, 6, 9, 9, 6, 4, 5, 3, 6, 4, 5, 7, 7, 8, 3, 5, 6, 5, 8, 7, 5, 4, 5, 8, 7, 9, 1, 7, 6, 5, 4, 6, 8, 8, 7, 9, 7, 4, 9, 7, 6, 8, 8, 9, 5, 9, 7, 3, 7, 9, 7, 9, 5, 9, 8, 7, 1, 4, 4, 3, 8, 7, 7, 1, 8, 2, 5, 9, 5, 8, 9, 5, 6, 3, 7, 7, 8, 9, 9, 7, 4, 4, 8, 5, 6, 9, 9, 8, 6, 8]
                    weights : [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
                  - # Reel[4]
                    symbols : [1, 8, 7, 9, 6, 9, 9, 7, 4, 5, 9, 8, 5, 4, 9, 9, 5, 8, 9, 7, 3, 8, 4, 8, 3, 7, 4, 9, 4, 8, 8, 3, 8, 4, 9, 9, 8, 7, 3, 9, 3, 9, 7, 9, 4, 9, 4, 7, 6, 9, 9, 6, 4, 5, 3, 6, 4, 5, 7, 7, 8, 3, 5, 6, 5, 8, 7, 5, 4, 5, 8, 7, 9, 1, 7, 6, 5, 4, 6, 8, 8, 7, 9, 7, 4, 9, 7, 6, 8, 8, 9, 5, 9, 7, 3, 7, 9, 7, 9, 5, 9, 8, 7, 1, 4, 4, 3, 8, 7, 7, 1, 8, 2, 5, 9, 5, 8, 9, 5, 6, 3, 7, 7, 8, 9, 9, 7, 4, 4, 8, 5, 6, 9, 9, 8, 6, 8]
                    weights : [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
                  - # Reel[5]
                    symbols : [1, 8, 7, 9, 6, 9, 9, 7, 4, 5, 9, 8, 5, 4, 9, 9, 5, 8, 9, 7, 3, 8, 4, 8, 3, 7, 4, 9, 4, 8, 8, 3, 8, 4, 9, 9, 8, 7, 3, 9, 3, 9, 7, 9, 4, 9, 4, 7, 6, 9, 9, 6, 4, 5, 3, 6, 4, 5, 7, 7, 8, 3, 5, 6, 5, 8, 7, 5, 4, 5, 8, 7, 9, 1, 7, 6, 5, 4, 6, 8, 8, 7, 9, 7, 4, 9, 7, 6, 8, 8, 9, 5, 9, 7, 3, 7, 9, 7, 9, 5, 9, 8, 7, 1, 4, 4, 3, 8, 7, 7, 1, 8, 2, 5, 9, 5, 8, 9, 5, 6, 3, 7, 7, 8, 9, 9, 7, 4, 4, 8, 5, 6, 9, 9, 8, 6, 8]
                    weights : [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
      # 圖標設定
      SymbolSetting:
          symbolUsed : [Z1,S1,C1,H1,H2,H3,H4,L1,L2,L3,L4,L5]
          payTable :
              - [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
              - [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
              - [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
              - [0, 0, 0, 0, 0, 0, 0, 200, 200, 500, 500, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000]
              - [0, 0, 0, 0, 0, 0, 0, 50, 50, 200, 200, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500]
              - [0, 0, 0, 0, 0, 0, 0, 40, 40, 100, 100, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300]
              - [0, 0, 0, 0, 0, 0, 0, 30, 30, 40, 40, 240, 240, 240, 240, 240, 240, 240, 240, 240, 240, 240, 240, 240, 240, 240, 240, 240, 240, 240]
              - [0, 0, 0, 0, 0, 0, 0, 20, 20, 30, 30, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200]
              - [0, 0, 0, 0, 0, 0, 0, 16, 16, 24, 24, 160, 160, 160, 160, 160, 160, 160, 160, 160, 160, 160, 160, 160, 160, 160, 160, 160, 160, 160]
              - [0, 0, 0, 0, 0, 0, 0, 10, 10, 20, 20, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100]
              - [0, 0, 0, 0, 0, 0, 0, 8, 8, 18, 18, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80]
              - [0, 0, 0, 0, 0, 0, 0, 5, 5, 15, 15, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40]

      # 中獎設定
      HitSetting:
          betType: BetTypeCollect
          lineTable:


# 額外設定

Fixed:
FreeGameRounds: 15
RetriggerRounds: 5
FreeMaxRounds: 100
Multipilers: [2,3,4,5,6,8,10,12,15,20,25,50,100,150,200,250,500]
MultipilerLimit: 51000
ScatterPay: [0, 0, 0, 60, 100, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000]
BetModes: - # Mode:0 Normal
BetMode: 0
BaseReelChooseWeight: [1,1,0]
FreeReelChooseWeight: [0,1]
BaseMultiProb: [100,100,100,100,100,80,80,60,60,50,50,30,30,20,15,10,5]
BaseMultiLvUp: [100,100,100,100,100,80,80,60,60,50,50,30,30,20,15,15,0]
FreeMultiProb: [50,50,50,50,50,110,110,90,90,80,80,50,50,40,25,15,10]
FreeMultiLvUp: [120,120,120,120,120,60,60,60,50,50,50,30,30,20,15,15,0] - # Mode:1 BuyFeaureFree
BetMode: 1
BaseReelChooseWeight: [0,0,1]
FreeReelChooseWeight: [1,0]
BaseMultiProb: [100,100,100,100,100,80,80,60,60,50,50,30,30,20,15,10,5]
BaseMultiLvUp: [100,100,100,100,100,80,80,60,60,50,50,30,30,20,15,15,0]
FreeMultiProb: [50,50,50,50,50,110,110,90,90,80,80,50,50,40,25,15,10]
FreeMultiLvUp: [120,120,120,120,120,60,60,60,50,50,50,30,30,20,15,15,0]
