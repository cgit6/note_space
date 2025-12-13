## 概述
* `buildGame1801` 函數負責創建 `game1801` struct 以及延伸的子結構 `fixed1801` struct 、`exts` struct。
* `getResult` 函數負責執行一次 spin 的遊戲主要邏輯，子函數 `getBaseResult` 、`getFreeResult` 負責遊戲內部邏輯。
* 重點說明 yaml 設定與遊戲邏輯
* 補充討論

## 設定檔

重點內容 `GameModeSettingList`、`Fixed` 兩個。

* `GameModeSettingList` 子結構有兩個 `GameModeSetting` 分別用於 BaseGame 設定、FreeGame 設定。`GameModeSetting` 裡面有 `ReelStripsGroup` 可定義多組輪帶。
* `Fixed` 定義該遊戲特殊設定 `BetMode` 0/1 對應不同買入設定，分別是 "普通" 與 "直接買 FG"

```yaml=
# [文件網址] None
# [玩法說明] None


# 遊戲名稱 : 1801 | StormOfSeth | 戰神賽特
GameName: StormOfSeth

# 押注基本單位，兩種下注模式
BetUnit : [20,2000]

# 最大贏分(對應BetUnit)
MaxWinLimit : 200000

# 遊戲模式設定列表，一個遊戲模式相當於一個狀態，遊戲將在各狀態間轉換
GameModeSettingList:
    - # GameModeSetting[0]: BaseGame 設定
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
                    symbols : [4,4,9,9,9]
                    weights : [1,1,1,1,1]
                  - # Reel[1]
                    symbols : [4,4,8,8,8]
                    weights : [1,1,1,1,1]
                  - # Reel[2]
                    symbols : [6,2,2,7,7]
                    weights : [1,1,1,1,1]
                  - # Reel[3]
                    symbols : [6,6,7,7,7]
                    weights : [1,1,1,1,1]
                  - # Reel[4] 
                    symbols : [6,6,6,6,2]
                    weights : [1,1,1,1,1]
                  - # Reel[5] 
                    symbols : [6,6,6,6,2]
                    weights : [1,1,1,1,1]
              - # ReelStrip[1] 
                weight : 0
                reels : 
                  - # Reel[0]
                      symbols : [7,6,7,6,7]
                      weights : [1,0,0,0,0]
                  - # Reel[1]
                      symbols : [9,4,9,4,9]
                      weights : [1,0,0,0,0]
                  - # Reel[2]
                      symbols : [8,8,6,6,6]
                      weights : [1,0,0,0,0]
                  - # Reel[3]
                      symbols : [7,7,7,5,5]
                      weights : [1,0,0,0,0]
                  - # Reel[4]
                      symbols : [6,6,6,9,9]
                      weights : [1,0,0,0,0]
                  - # Reel[5]
                      symbols : [6,6,6,9,9]
                      weights : [1,0,0,0,0]
              - # ReelStrip[2]
                weight : 0
                reels : 
                  - # Reel[0]
                      symbols : [6,7,6,7,7,2,7,6,7]
                      weights : [0,1,1,1,1,1,0,0,0]                 
                  - # Reel[1]
                      symbols : [6,7,6,7,7,2,7,6,7]
                      weights : [0,1,1,1,1,1,0,0,0]                    
                  - # Reel[2]
                      symbols : [6,7,6,7,7,2,7,6,7]
                      weights : [0,1,1,1,1,1,0,0,0]                
                  - # Reel[3]
                      symbols : [6,7,6,7,7,2,7,6,7]
                      weights : [0,1,1,1,1,1,0,0,0]            
                  - # Reel[4]
                      symbols : [6,7,6,7,7,6,7,6,7]
                      weights : [1,1,1,1,1,1,1,1,1]   
                  - # Reel[5]
                      symbols : [6,7,6,7,7,6,7,6,7]
                      weights : [1,1,1,1,1,1,1,1,1]  
              - # ReelStrip[3]
                weight : 0
                reels : 
                  - # Reel[0]
                      symbols : [6,7,6,7,7,6,7,6,7]
                      weights : [1,1,1,1,1,1,1,1,1]                 
                  - # Reel[1]
                      symbols : [6,7,6,7,7,2,7,6,7]
                      weights : [0,1,1,1,1,1,0,0,0]                    
                  - # Reel[2]
                      symbols : [6,7,6,7,7,2,7,6,7]
                      weights : [0,1,1,1,1,1,0,0,0]                
                  - # Reel[3]
                      symbols : [6,7,6,7,7,2,7,6,7]
                      weights : [0,1,1,1,1,1,0,0,0]            
                  - # Reel[4]
                    symbols : [6,7,6,7,7,6,7,6,7]
                    weights : [1,1,1,1,1,1,1,1,1]   
                  - # Reel[5]
                    symbols : [6,7,6,7,7,2,7,6,7]
                    weights : [0,1,1,1,1,1,0,0,0] 
              - # ReelStrip[4]
                weight : 0
                reels : 
                  - # Reel[0]
                    symbols : [6,7,6,7,7,2,7,6,7]
                    weights : [0,1,1,1,1,1,0,0,0]                 
                  - # Reel[1]
                    symbols : [6,7,6,7,7,6,7,6,7]
                    weights : [1,1,1,1,1,1,1,1,1]                    
                  - # Reel[2]
                    symbols : [6,7,6,7,7,2,7,6,7]
                    weights : [0,1,1,1,1,1,0,0,0]                
                  - # Reel[3]
                    symbols : [6,7,6,7,7,2,7,6,7]
                    weights : [0,1,1,1,1,1,0,0,0]            
                  - # Reel[4]
                    symbols : [6,7,6,7,7,2,7,6,7]
                    weights : [0,1,1,1,1,1,0,0,0]  
                  - # Reel[5]
                    symbols : [6,7,6,7,7,6,7,6,7]
                    weights : [1,1,1,1,1,1,1,1,1]

              - # ReelStrip[5]
                weight : 0
                reels : 
                  - # Reel[0]
                    symbols : [6,7,6,7,7,2,7,6,7]
                    weights : [0,1,1,1,1,1,0,0,0]                 
                  - # Reel[1]
                    symbols : [6,7,6,7,7,6,7,6,7]
                    weights : [1,1,1,1,1,1,1,1,1]                    
                  - # Reel[2]
                    symbols : [6,7,6,7,7,2,7,6,7]
                    weights : [0,1,1,1,1,1,0,0,0]                
                  - # Reel[3]
                    symbols : [6,7,6,7,7,2,7,6,7]
                    weights : [0,1,1,1,1,1,0,0,0]            
                  - # Reel[4]
                    symbols : [6,7,6,7,7,2,7,6,7]
                    weights : [0,1,1,1,1,1,0,0,0]  
                  - # Reel[5]
                    symbols : [6,7,6,7,7,6,7,6,7]
                    weights : [1,1,1,1,1,1,1,1,1]
      # 圖標設定
      SymbolSetting:
          symbolUsed : [Z1,S1,C1,H1,H2,H3,H4,L1,L2,L3,L4,L5]
          payTable : 
              - [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
              - [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
              - [0, 0, 0, 60, 100, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000]
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
                    symbols : [4,4,9,9,9]
                    weights : [1,1,1,1,1]
                  - # Reel[1]
                    symbols : [4,4,8,8,8]
                    weights : [1,1,1,1,1]
                  - # Reel[2]
                    symbols : [6,2,2,7,7]
                    weights : [1,1,1,1,1]
                  - # Reel[3]
                    symbols : [6,6,7,7,7]
                    weights : [1,1,1,1,1]
                  - # Reel[4] 
                    symbols : [6,6,6,6,2]
                    weights : [1,1,1,1,1]
                  - # Reel[5] 
                    symbols : [6,6,6,6,2]
                    weights : [1,1,1,1,1]
              - # ReelStrip[1] 
                weight : 0
                reels : 
                  - # Reel[0]
                      symbols : [7,6,7,6,7]
                      weights : [1,0,0,0,0]
                  - # Reel[1]
                      symbols : [9,4,9,4,9]
                      weights : [1,0,0,0,0]
                  - # Reel[2]
                      symbols : [8,8,6,6,6]
                      weights : [1,0,0,0,0]
                  - # Reel[3]
                      symbols : [7,7,7,5,5]
                      weights : [1,0,0,0,0]
                  - # Reel[4]
                      symbols : [6,6,6,9,9]
                      weights : [1,0,0,0,0]
                  - # Reel[5]
                      symbols : [6,6,6,9,9]
                      weights : [1,0,0,0,0]
      # 圖標設定
      SymbolSetting:
          symbolUsed : [Z1,S1,C1,H1,H2,H3,H4,L1,L2,L3,L4,L5]
          payTable : 
              - [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
              - [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
              - [0, 0, 0, 60, 100, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000]
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
  BetModes:
    - # Mode:0 Normal
      BetMode: 0
      BaseStartReelChooseWeight: [1,1,0,0,0]
      FreeStartReelChooseWeight: [1,1]
      BaseMultiProb: [100,100,100,100,100,80,80,60,60,50,50,30,30,20,15,10,5]
      BaseMultiLvUp: [100,100,100,100,100,80,80,60,60,50,50,30,30,20,15,15,0]
      FreeMultiProb: [50,50,50,50,50,110,110,90,90,80,80,50,50,40,25,15,10]
      FreeMultiLvUp: [120,120,120,120,120,60,60,60,50,50,50,30,30,20,15,15,0]
    - # Mode:1 BuyFeaureFree
      BetMode: 1
      BaseStartReelChooseWeight: [0,0,1,1,1]
      FreeStartReelChooseWeight: [1,1]
      BaseMultiProb: [100,100,100,100,100,80,80,60,60,50,50,30,30,20,15,10,5]
      BaseMultiLvUp: [100,100,100,100,100,80,80,60,60,50,50,30,30,20,15,15,0]
      FreeMultiProb: [50,50,50,50,50,110,110,90,90,80,80,50,50,40,25,15,10]
      FreeMultiLvUp: [120,120,120,120,120,60,60,60,50,50,50,30,30,20,15,15,0]
```

## 遊戲介面

[code](https://hackmd.io/SpfFhYq_Q2qyyPP5tFPPQA#game_1801_stromofsethgo)

### 註冊


### 創建 game1801 struct
`buildGame1801()` 主要目標是創建 `game1801` struct，該結構包含 `fixed1801` struct 、`exts` struct。以及 accWin、maxWinLimit、extendId 屬性值。
```go=
type game1801 struct {
	fixed       *fixed1801
	accWin      int
	maxWinLimit int
	extendId    int
	exts        []*extend1801
}

```
1. 建立`fixed1801` 實例，負責接收設定檔的 Fixed 設定值。
2. 讀設定檔，做型別轉換。將 any 依據 fixed 定義的型別轉成 特定型別。做4. `f.betmodes` 依照不同下注模式，對設定檔的 權重/機率 做 Lut 處理，方便快速抽樣。
3. 建立 `game1801` 實例，特別注意 `extendId` 和 `exts` 建立 exts pool 初始長度 200。
4. 創建 `ext` 實例存入 `game1801` 實例。

``` go=
func buildGame1801(g *GameHandler) gameLogic {

	gs := g.gameSetting // 指向 GameHandler 設定

	// 創建 fixed1801 實例
	f := &fixed1801{
		// 配置補盤位置
		fillScreenIdx: make([]int, gs.GameModeSettingList[0].ScreenSetting.Columns),
		// 補盤軸索引用的緩存
		nowfillReelStripsIdx: make([]int, gs.GameModeSettingList[0].ScreenSetting.Columns),
		// 提供不同下注模式的 Lut 配置(如果需要轉成 Lut 的話)
		betmodes: make([]betModes1801, len(g.BetUnit)),
		// 盤面緩存
		screen: make([]int16, g.gameSetting.GameModeSettingList[0].ScreenSetting.ScreenSize),
		// 符號類型，用於判斷符號時可以直接調用
		symbolTypes: g.gameSetting.GameModeSettingList[0].SymbolSetting.SymbolTypes,
		// 乘數索引清單
		multipilersIndex: make([]int, 501),
	}

	// 讀設定檔
	// 把 gs.Fixed 由 map[string]any 轉成特定型別 T。
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

	// fmt.Println(f.multipilersIndex)
	// 設定檔 weight 轉存為 Lut
	// 依照 不同下注模式把設定檔裡的權重或是機率轉成 Lut 方便快速抽樣
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
		accWin:      0,                        // 累積贏分
		maxWinLimit: 0,                        // 最大贏分上限
		extendId:    0,                        // exts 索引值
		exts:        make([]*extend1801, 200), // exts pool
	}

	// 獲取盤面大小
	size := g.gameSetting.GameModeSettingList[0].ScreenSetting.ScreenSize

	// 根據盤面大小創建長度為 200 的 exts pool
	// 這邊就會跳到下面的 額外結構
	for i := 0; i < 200; i++ {
		g1801.exts[i] = buildExtend1801(size)
	}

	return g1801
}
```

```go=
// 重置 game1801
func (g *game1801) newspin() {
	g.accWin = 0 // 重置累積贏分

	for i := 0; i < g.extendId; i++ {
		g.exts[i].reset()
	}
	g.extendId = 0
}

func (g *game1801) next() *extend1801 {
	g.extendId++
	// 當局連鎖過長時動態擴充 extend pool，避免索引溢位
	if g.extendId >= len(g.exts) {
		g.exts = append(g.exts, buildExtend1801(len(g.fixed.screen)))
	}
	return g.exts[g.extendId]
}

```

## 此遊戲需要的額外結構宣告

### fixed 設定宣告

這部分分成 `fixed1801` struct、子結構 `BetMode1801` / `betModes1801` 、 隨機選取元素的函數


 `Fixed` struct 負責儲存 yaml 設定檔的 Fixed、包含乘倍圖標資訊的盤面、補盤相關參數、符號類型
```go=
type fixed1801 struct {
	fillScreenIdx        []int // 每一軸要補盤的位置
	nowfillReelStripsIdx []int // 補盤軸當下idx
	betmodes             []betModes1801
	screen               []int16 // 包含乘倍圖標資訊的盤面

	// 圖標類型快取
	symbolTypes []enum.SymbolType

	// 以下讀表
	FreeGameRounds  int           `yaml:"FreeGameRounds"`
	RetriggerRounds int           `yaml:"RetriggerRounds"`
	FreeMaxRounds   int           `yaml:"FreeMaxRounds"`
	Multipilers     []int         `yaml:"Multipilers"`
	BetModes        []BetMode1801 `yaml:"BetModes"`
	MultipilerLimit int           `yaml:"MultipilerLimit"`
}
```

`Fixed` 子結構 `BetMode1801` / `betModes1801` 分別儲存 "讀入設定檔後的原始權重" 以及 "Lut 處理後的索引"。
根據數值的意義 `baseMultiLvUpLut` 與 `freeMultiLvUpLut` 不需要經過 Lut 轉換，故保留原始資料。

```go=
// 讀設定檔
type BetMode1801 struct {
	// 後面的 `yaml:"BetMode"` 語法是 struct tag 告訴 YAML 解碼器這個欄位對應 YAML 檔裡的 key name。
	BetMode              int   `yaml:"BetMode"`
	BaseReelChooseWeight []int `yaml:"BaseReelChooseWeight"`
	FreeReelChooseWeight []int `yaml:"FreeReelChooseWeight"`
	BaseMultiProb        []int `yaml:"BaseMultiProb"`
	BaseMultiLvUp        []int `yaml:"BaseMultiLvUp"`
	FreeMultiProb        []int `yaml:"FreeMultiProb"`
	FreeMultiLvUp        []int `yaml:"FreeMultiLvUp"`
}

// Lut 處理後
type betModes1801 struct {
	betMode          int         // 押注模式
	baseReelLut      sampler.LUT // 主遊戲起始輪id LUT表
	freeReelLut      sampler.LUT
	baseMultiProbLut sampler.LUT
	baseMultiLvUpLut []int
	freeMultiProbLut sampler.LUT
	freeMultiLvUpLut []int
}
```
隨機選取陣列中的元素
1. `getBaseMult` / `getFreeMult` 選擇 BG/FG spin 乘數符號對應的乘數值
2. `baseMultLvUp` / `freeMultLvUp` 選擇 BG/FG 乘數符號在掉落後的升級概率

```go=
func (b *betModes1801) getBaseMult(core *core.Core) int {
	return b.baseMultiProbLut[core.IntN(len(b.baseMultiProbLut))]
}

// 丟一個 0–999 的隨機數判斷是否升級；成功就回傳 (true, nowIdx+1)，失敗回 (false, nowIdx)。
func (b *betModes1801) baseMultLvUp(core *core.Core, nowIdx int) (bool, int) {
	prob := b.baseMultiLvUpLut[nowIdx]
	if core.IntN(1000) < prob {
		next := nowIdx + 1
		return true, next
	}
	return false, nowIdx
}


func (b *betModes1801) getFreeMult(core *core.Core) int {
	return b.freeMultiProbLut[core.IntN(len(b.freeMultiProbLut))]
}


func (b *betModes1801) freeMultLvUp(core *core.Core, nowIdx int) (bool, int) {
	prob := b.freeMultiLvUpLut[nowIdx]
	if core.IntN(1000) < prob {
		next := nowIdx + 1
		return true, next
	}
	return false, nowIdx
}
```


### ext 拓展結果格式宣告

`extend1801` struct 儲存對外暴露的資料，包含: 當前累積乘數、乘數符號位置、乘數符號
```go=
type extend1801 struct {
	NowMulti      int   `json:"nowmulti"`      // 當前累積乘數
	MultiSymPos   []int `json:"multisympos"`   // 乘數符號位置
	MultiSymMults []int `json:"multisymmults"` // 乘數符號
}

func buildExtend1801(size int) *extend1801 {
	return &extend1801{
		NowMulti:      0,
		MultiSymPos:   make([]int, 0, size),
		MultiSymMults: make([]int, 0, size),
	}
}

func (ext *extend1801) reset() {
	ext.NowMulti = 0
	ext.MultiSymPos = ext.MultiSymPos[:0]
	ext.MultiSymMults = ext.MultiSymMults[:0]
}
```

## 遊戲主要邏輯函數

`getResult` 流程

1. 更新最高累積贏分值
2. 重置這次 SpinResult 緩存，並且把投注資訊寫入 `SpinResult` 
3. 重置 `game1801` 內部的累積贏分 與 exts、extendId
4. 執行 BG spin 返回 `*result.GameModeResult`
5. 將 BG spin 結果添加到 `spinResult`
6. 判斷是否觸發 FG
7. 結束這次spin 
8. 返回 SpinResult pointer

```go=
func (g *game1801) getResult(betMode int, betMult int, gh *GameHandler) *result.SpinResult {
	g.maxWinLimit = gh.gameSetting.MaxWinLimit * betMult // 最高累計贏分值

	// StartNewSpin 重置 SpinResult 狀態、設定本次投注資訊，返回 SpinResult 指標。
	// gh.StartNewSpin() 做了以下三件事
	// 1. ResetResult() 重置這次 SpinResult 緩存，
	// 2. 並且把投注資訊(betMode / betMult) 寫入 SpinResult
	// 3. 回傳 gh.SpinResult pointer
	sr := gh.StartNewSpin(betMode, betMult)

        // 重置 game1801 狀態 (accWin、ext、ext id)
	g.newspin()

	// 執行一局 BG spin，返回 *result.GameModeResult
	base := g.getBaseResult(betMode, betMult, gh)
	// 加入到這次 spin 的 結果清單
	sr.AppendModeResult(base)

	if base.Trigger != 0 && g.accWin < g.maxWinLimit {
		free := g.getFreeResult(betMode, betMult, gh)
		sr.AppendModeResult(free)
	}
        // 結束遊戲狀態
	sr.End()
	return sr
}
```

## 遊戲中各模式內部邏輯實作

### getBaseResult

* 掉落消除流程
* 更新累積 `g.accWin` 贏分判斷 "累積贏分" 是否大於 "最高贏分上限值"
* 選擇輪帶表 "生成盤面" 與 "補盤用輪帶表" 保持一致 
* 調用 FinishAct / FinishStep / FinishStep / FinishRound 時機


``` go=
func (g *game1801) getBaseResult(betMode int, betMult int, gh *GameHandler) *result.GameModeResult {
	fixed := g.fixed
        // 獲取 BaseGame 設定、盤面生成、算分、儲存 spin 結果、ext
	mode := gh.GameModeHandlerList[0] // GameModeHandlerList 依照設定檔建 0 就是 BaseGame 設定
	sg := mode.ScreenGenerator
	sc := mode.ScreenCalculator
	gmr := mode.GameModeResult
	ext := g.exts[g.extendId]
    
        // 重置補盤相關索引
	g.resetIdx()

	// 選擇輪帶表
	betmodeSets := fixed.betmodes[betMode].baseReelLut.Pick(gh.core)
	// 補盤用輪帶表
	fillReelStrips := &mode.GameModeSetting.GenScreenSetting.ReelStripsGroup[betmodeSets] // 指定補盤軸
	// 1. 生成該round開局盤面
	screen := sg.GenScreenByAssignedReelStrip(betmodeSets)
        // 把 screen 這個 slice 的元素複製到 fixed.screen 中
	copy(fixed.screen, screen)

	// 取得本次補珠輪帶起始位置
        // 預先處理要補盤時，每一軸要從哪裡開始補
	for i := 0; i < len(fixed.fillScreenIdx); i++ {
		fixed.fillScreenIdx[i] = gh.core.IntN(len(fillReelStrips.ReelStripsReels[i].ReelSymbols))
	}

        // 掉落消除流程
	for range 100 {
		// 2. 算分
		_ = sc.CalcScreen(betMult, screen, gmr)
                // 取回的當前暫存「中獎格子索引」紀錄這一輪算分命中的盤面位置
                // gravity 會用來把那些格子清空並做掉落
		hm := gmr.HitMapTmp()

		// 3. 取原始 win
                // 得分符號的贏分，不含乘數處理
		win := gmr.GetTmpWin() // 先記當下贏分避免提交後要重找

		// 4. 如果沒贏分退出(step結束)
		if win == 0 {
			gmr.FinishAct("GenAndCalcScreen", screen, nil)
			gmr.FinishStep()
			break
		}

		// 5. 有贏分: 算乘倍
		mult := g.getBaseMulti(fixed.screen, betMode, gh.core, ext)
		if mult > 0 {
			win *= mult
		}

		// 判斷 "累積贏分" 是否大於 "最高贏分上限值"
		// **注意等號，如果沒有等號，剛好達到滿倍時會再走一輪0分**
		if (g.accWin + win) >= g.maxWinLimit {
			gmr.UpdateTmpWin(g.maxWinLimit - g.accWin) // 更新分數
			gmr.FinishAct("MaxWin", screen, ext)       // 落地
			gmr.FinishStep()                           // 落地
			break
		}

		g.accWin += win // 更新累積贏分
		gmr.UpdateTmpWin(win)

		// 6. 提交得分的 Act 結果
		gmr.FinishAct("GenAndCalcScreen", screen, ext)
		// ext = g.next()

		// 7. 判斷是否要提升乘倍等級
		for idx, pos := range ext.MultiSymPos {
			mu := ext.MultiSymMults[idx] // 目前乘倍
			for i := 0; i < len(fixed.Multipilers); i++ {
				if (i < (len(fixed.Multipilers) - 1)) && mu == fixed.Multipilers[i] {
					up, nextIdx := fixed.betmodes[betMode].baseMultLvUp(gh.core, i)
					if up {
						fixed.screen[pos] = int16(100 + fixed.Multipilers[nextIdx]) // 把乘倍標記放到盤面上
					}
					break
				}
			}
		}

		// 8. 消除掉落，同步更新 fixed.screen、screen
		fixed.screen = g.gravity(fixed.screen, hm, sg.Cols, sg.Rows, g.fixed.fillScreenIdx)
		screen = g.gravity(screen, hm, sg.Cols, sg.Rows, g.fixed.fillScreenIdx)
		gmr.FinishAct("Gravity", screen, nil) // 消除掉落盤面

		// 9. 提交step結果(step結束)
		gmr.FinishStep()
		ext = g.next()

		// 10. 補滿盤面 
		// screen 是計分用的原始盤面；fixed.screen 另外帶有乘倍標記
		// fillScreen 用補盤輪帶把 screen 補滿後，再把補好的新符號同步回 fixed.screen 里那些先前被消除成 0 的位置。
		screen = g.fillScreen(screen, fillReelStrips, g.fixed.fillScreenIdx, g.fixed.nowfillReelStripsIdx, sg.Cols)
		for pos, sym := range fixed.screen {
			if sym == 0 {
				fixed.screen[pos] = screen[pos]
			}
		}
	}
	gmr.Trigger = g.trigger(screen)
	gmr.FinishRound()

	return mode.YieldResult()
}
```

### getFreeResult

講 BG 沒有的重點機制
* 狀態值: `nowTotalMult` 累積乘數 / `nowLimitRounds` FG spin 次數
* 第 5 步 多了判斷 `nowTotalMult` 是否大於 "累加總倍數上限值"
```go=
func (g *game1801) getFreeResult(betMode int, betMult int, gh *GameHandler) *result.GameModeResult {
	mode := gh.GameModeHandlerList[1]
	sg := mode.ScreenGenerator
	sc := mode.ScreenCalculator
	gmr := mode.GameModeResult
	nowLimitRounds := g.fixed.FreeGameRounds
	fixed := g.fixed
	nowTotalMult := 0
	ext := g.next()

	for i := 0; i < nowLimitRounds; i++ {
		g.resetIdx()
		// 押注設定
		betmodeSets := fixed.betmodes[betMode].baseReelLut.Pick(gh.core)
		fillReelStrips := &mode.GameModeSetting.GenScreenSetting.ReelStripsGroup[betmodeSets] // 指定補盤軸
		// 1. 生成該round開局盤面
		screen := sg.GenScreenByAssignedReelStrip(betmodeSets)
		copy(fixed.screen, screen)

		for range 100 {
			// 2. 算分
			_ = sc.CalcScreen(betMult, screen, gmr)
			hm := gmr.HitMapTmp()

			// 3. 取原始 win
			win := gmr.GetTmpWin() // 先記當下贏分避免提交後要重找

			// 4. 如果沒贏分退出(step結束)
			if win == 0 {
				gmr.FinishStep()
				gmr.FinishAct("GenAndCalcScreen", screen, nil)
				break
			}

			// 5. 計算乘倍
			mult := g.getFreeMulti(fixed.screen, betMode, gh.core, ext)

			// 更新贏分相關參數
			if mult > 0 {
				nowTotalMult += mult // 更新累積乘數

				// 判斷 nowTotalMult 是否大於 "累加總倍數上限值"
				if nowTotalMult >= g.fixed.MultipilerLimit {
					nowTotalMult = g.fixed.MultipilerLimit
				}

				win *= nowTotalMult // 更新贏分

			}

			// 判斷 "累積贏分" 是否大於 "最高贏分上限值"
			// **注意等號，如果沒有等號，剛好達到滿倍時會再走一輪0分**
			if (g.accWin + win) >= g.maxWinLimit {
				gmr.UpdateTmpWin(g.maxWinLimit - g.accWin) // 最高
				break
			}

			g.accWin += win
			gmr.UpdateTmpWin(win)

			// 6. 提交得分的 Act 結果
			gmr.FinishAct("GenAndCalcScreen", screen, ext)

			// 7. 判斷是否要提升乘倍等級
			for idx, pos := range ext.MultiSymPos {
				mu := ext.MultiSymMults[idx] // 目前乘倍
				for i := 0; i < len(fixed.Multipilers); i++ {
					if (i < (len(fixed.Multipilers) - 1)) && mu == fixed.Multipilers[i] {
						up, nextIdx := fixed.betmodes[betMode].freeMultLvUp(gh.core, i)
						if up {
							fixed.screen[pos] = int16(100 + fixed.Multipilers[nextIdx]) // 把乘倍標記放到盤面上
						}
						break
					}
				}
			}
			// 8. 消除掉落
			fixed.screen = g.gravity(fixed.screen, hm, sg.Cols, sg.Rows, g.fixed.fillScreenIdx)
			screen = g.gravity(screen, hm, sg.Cols, sg.Rows, g.fixed.fillScreenIdx)
			gmr.FinishAct("Gravity", screen, nil) // 消除掉落盤面

			// 9. 提交step結果(step結束)
			gmr.FinishStep()
			ext = g.next()

			// 10. 補滿盤面
			screen = g.fillScreen(screen, fillReelStrips, g.fixed.fillScreenIdx, g.fixed.nowfillReelStripsIdx, sg.Cols)
			for pos, sym := range fixed.screen {
				if sym == 0 {
					fixed.screen[pos] = screen[pos]
				}
			}
		}

		gmr.FinishRound()
	}

	return mode.YieldResult()
}
```

## 內部輔助函數

`trigger` 函數，計算 Scatter 數量，如果大於 4 顆，則更新


`gravity`


`fillScreen`


`resetIdx`


### `getBaseMulti()` 函數


`getBaseMulti` 檢視盤面，如果有看到乘數符號，則做以下兩種處理


需要特別注意它的盤面適用 `g.fixed.screen[pos]` 不是用 `screen`(為什麼?)



`getFreeMulti`


這份遊戲邏輯的難點在於

## 反饋

根據早上討論做了以下一系列調整
<!-- * 加強理解輔助函數 `gravity`、`fillScreen`、`getBaseMulti`、`getFreeMulti`
* `screen` 與 `fixed.screen` 的差異 -->
- [x] 遊戲邏輯 `getBaseResult` 、`getFreeResult` "判斷是否要提升乘倍等級" 邏輯優化，以下是目前邏輯:

    ```go=
        // 7. 判斷是否要提升乘倍等級

        // 遍歷目前盤面乘數符號的位置
        for idx, pos := range ext.MultiSymPos {
            // 
            mu := ext.MultiSymMults[idx] // 目前乘倍
            for i := 0; i < len(fixed.Multipilers); i++ {
                if (i < (len(fixed.Multipilers) - 1)) && mu == fixed.Multipilers[i] {
                    up, nextIdx := fixed.betmodes[betMode].freeMultLvUp(gh.core, i)

                    if up {
                        fixed.screen[pos] = int16(100 + fixed.Multipilers[nextIdx]) // 把乘倍標記放到盤面上
                    }
                    break
                }
            }
        }
    ```

    [方案] 在 `fixed` 維護一個 `multipilersIndex []int` 用於查找 `ext.MultiSymMults[idx]` 執行以下步驟
    1. 維護一個 `[]int` 長度為 501 的位置索引值，[-1,-1,0,1,2,...,16]
    
    ```go=
	// 初始化乘數索引清單
	for idx := range f.multipilersIndex {
		f.multipilersIndex[idx] = -1
	}

	// 添加索引值
	for idx, mu := range f.Multipilers {
		f.multipilersIndex[mu] = idx
	}
    ```
    結果
    ```
    [-1 -1 0 1 2 3 4 -1 5 -1 6 -1 7 -1 -1 8 -1 -1 -1 -1 9 -1 -1 -1 -1 10 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 11 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 12 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 13 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 14 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 15 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 16]
    ```
    
    2. 在 `fixed` 建立 `MultipilersIndexLookUp` 方法 查找函數 -> 給 乘數值 返回 索引位置
    
    ``` go=
    // 傳入乘數值，返回該乘數值在乘數清單的索引位置
    func (f *fixed1801) MultipilersIndexLookUp (m int) int {
        return f.MultipilersIndex[m]
    }
    ```


    3. 在 `getBaseResult`、`getFreeResult` 的 "判斷是否要提升乘倍等級" 部分調用
    ```go=
		for idx, pos := range ext.MultiSymPos {
			fmt.Println("idx", idx)
			mu := ext.MultiSymMults[idx] // 目前乘倍

			fmt.Println("mu: ", mu)
			idx := fixed.MultipilersIndexLookUp(mu)
			if (idx < (len(fixed.Multipilers) - 1)) && mu == fixed.Multipilers[idx] {
				// 用機率決定要不要升到下一級，回傳 nextIdx
				up, nextIdx := fixed.betmodes[betMode].baseMultLvUp(gh.core, idx)
				if up {
					fixed.screen[pos] = int16(100 + fixed.Multipilers[nextIdx]) // 把乘倍標記放到盤面上
				}
				break
			}
		}
    ```
    
- [ ] [疑問待確認] `getBaseMulti` 與 `getFreeMulti` 函數返回的是 "乘數值" 還是 "Lut 索引值"? 
    以下 `getBaseMulti` 為例，原始函數如下:
    ```go=
        func (g *game1801) getBaseMulti(screen []int16, betMode int, core *core.Core, ext *extend1801) int {
        multiGetter := g.fixed.betmodes[betMode]
        for pos, sym := range screen {
            g.fixed.screen[pos] = sym
            if sym == 1 {
                mult := multiGetter.getBaseMult(core)
                g.fixed.screen[pos] = int16(100 + mult) // 把乘倍標記放到盤面上

                ext.MultiSymPos = append(ext.MultiSymPos, pos)
                ext.MultiSymMults = append(ext.MultiSymMults, mult)
                ext.NowMulti += mult
            }
            if sym > 100 {
                mult := int(sym) - 100
                ext.MultiSymPos = append(ext.MultiSymPos, pos)
                ext.MultiSymMults = append(ext.MultiSymMults, mult)
                ext.NowMulti += mult
            }
        }
        return ext.NowMulti
    }
    ```

    我判斷是 Lut 所以我做了以下更新，因為有動到遊戲邏輯以外的函數，為了謹慎跟你確認一下。

    ```go=
    func (g *game1801) getBaseMulti(screen []int16, betMode int, core *core.Core, ext *extend1801) int {
        // 取出對應下注模式
        multiGetter := g.fixed.betmodes[betMode]
        for pos, sym := range screen {
            g.fixed.screen[pos] = sym
            if sym == 1 {
                // 隨機選擇乘數符號索引值
                multIdx := multiGetter.baseMultiProbLut.Pick(core)
                // 多加一行獲取乘數值
                mult := g.fixed.Multipilers[multIdx]
                g.fixed.screen[pos] = int16(100 + mult) // 把乘倍標記放到盤面上

                ext.MultiSymPos = append(ext.MultiSymPos, pos)
                ext.MultiSymMults = append(ext.MultiSymMults, mult)
                ext.NowMulti += mult
            }
            if sym > 100 {
                mult := int(sym) - 100
                ext.MultiSymPos = append(ext.MultiSymPos, pos)
                ext.MultiSymMults = append(ext.MultiSymMults, mult)
                ext.NowMulti += mult
            }
        }
        return ext.NowMulti
    }
    
    ```
    
- [x] `betModes1801` 屬性名稱命名問題， `baseMultiLvUpLut`、`freeMultiLvUpLut` 更新為 `baseMultiLvUp`、`freeMultiLvUp`。 
- [x] `getBaseMult`、`getFreeMult` 可以拿掉獲取方式可以改成 `b.baseMultiProbLut.Pick(core)` 這邊選擇直接在 `getBaseMulti`、`getFreeMulti` 函數中調用。
- [x] 設定檔命名問題 目前 `BaseReelStartChooseWeight`、`FreeReelStartChooseWeight` 皆提供給盤面生成與 掉落消除，命名更新為 `BaseReelChooseWeight`、`FreeReelChooseWeight`。
- [x] 不需要作兩次 `gravity()` 這種"重"計算。
    只要把 `screen` 用 `fix.screen` 反填回去就好(對於>100的符號統一改成乘倍圖標）
    ```go=
		fixed.screen = g.gravity(fixed.screen, hm, sg.Cols, sg.Rows, g.fixed.fillScreenIdx)
		// screen = g.gravity(screen, hm, sg.Cols, sg.Rows, g.fixed.fillScreenIdx)
		for i, s := range fixed.screen {
			if s > 100 {
				screen[i] = 1
			} else {
				screen[i] = s
			}
		}
		gmr.FinishAct("Gravity", screen, nil) // 消除掉落盤面
    ```
    
    
## 數值驗證

- [ ] `getBaseMulti` 中 `multIdx` 對應的 `mult` 值正確

fixed.screen 顯示某個位置是乘數值 但 screen 顯示它不是

- [ ] 先確認第一次 step 中步驟 8 消除掉落後 