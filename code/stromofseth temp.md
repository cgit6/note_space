```yaml=

# [文件網址] None
# [玩法說明] None


# 遊戲名稱 : 1801 | StormOfSeth | 戰神賽特
GameName: StormOfSeth

# 押注基本單位
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
                    symbols : [1, 8, 7, 9, 6, 9, 9, 7, 4, 5, 9, 8, 5, 4, 9, 9, 5, 8, 9, 7, 3, 8, 4, 8, 3, 7, 4, 9, 4, 8, 8, 3, 8, 4, 9, 9, 8, 7, 3, 9, 3, 9, 7, 9, 4, 9, 4, 7, 6, 9, 9, 6, 4, 5, 3, 6, 4, 5, 7, 7, 8, 3, 5, 6, 5, 8, 7, 5, 4, 5, 8, 7, 9, 1, 7, 6, 5, 4, 6, 8, 8, 7, 9, 7, 4, 9, 7, 6, 8, 8, 9, 5, 9, 7, 3, 7, 9, 7, 9, 5, 9, 8, 7, 1, 4, 4, 3, 8, 7, 7, 1, 8, 2, 5, 9, 5, 8, 9, 5, 6, 3, 7, 7, 8, 9, 9, 7, 4, 4, 8, 5, 6, 9, 9, 8, 6, 8]
                    weights : [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
                  - # Reel[1]
                    symbols : [6, 8, 4, 8, 9, 5, 9, 7, 9, 6, 3, 8, 6, 9, 8, 5, 9, 6, 7, 9, 9, 9, 4, 9, 8, 9, 7, 8, 8, 5, 9, 5, 8, 8, 3, 7, 9, 4, 6, 8, 2, 8, 3, 6, 9, 6, 4, 7, 7, 4, 4, 6, 9, 3, 8, 9, 5, 7, 1, 7, 3, 6, 7, 7, 8, 9, 8, 9, 8, 9, 6, 8, 7, 7, 5, 3, 9, 6, 4, 7, 7, 7, 7, 4, 7, 3, 5, 7, 9, 9, 8, 5, 8, 3, 3, 7, 8, 7, 9, 6, 6, 9, 5, 4, 8, 7, 6, 8, 5, 5, 7, 8, 6, 9, 7, 8, 8, 8, 5, 8, 3, 7, 7, 8, 4, 9, 7, 5, 6, 5, 5, 8, 6, 3, 6, 6, 7, 1, 9, 9, 7, 9, 8, 8, 6, 9, 9, 5, 8, 8, 2, 7, 3, 7, 1]
                    weights : [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
                  - # Reel[2]
                    symbols : [7, 7, 6, 5, 7, 4, 9, 6, 9, 4, 7, 5, 8, 4, 8, 7, 9, 4, 7, 8, 7, 4, 5, 9, 6, 9, 9, 8, 4, 8, 9, 9, 4, 3, 7, 9, 7, 5, 9, 4, 7, 9, 7, 3, 9, 5, 7, 5, 3, 3, 3, 5, 4, 7, 8, 8, 4, 7, 3, 9, 5, 4, 4, 5, 9, 4, 9, 8, 8, 5, 8, 4]
                    weights : [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
                  - # Reel[3]
                    symbols : [7, 2, 6, 6, 5, 6, 9, 8, 4, 6, 8, 9, 8, 3, 7, 6, 5, 1, 8, 1, 6, 4, 7, 6, 2, 7, 3, 7, 7, 9, 5, 5, 8, 3, 6, 7, 5, 9, 6, 8, 7, 4, 5, 8, 7, 8, 6, 7, 7, 4, 9, 5, 7, 9, 7, 9, 3, 9, 7, 8, 7, 4, 3, 4, 6, 5, 7, 9, 3, 4, 6, 9, 9, 6, 3, 9, 3, 9, 3, 6, 4, 9, 9, 9, 8, 3, 4, 9, 7, 7, 3, 9, 9, 7, 4, 4, 9, 7, 8, 7, 8, 8, 6, 9, 9, 9, 8, 4, 2, 5, 9, 9, 8, 4, 7, 7, 5, 8, 7, 9, 8, 4, 7, 8, 6, 4, 8, 7, 7, 7, 8, 8, 7, 7, 8, 9, 3, 8, 3, 9, 5, 7, 3, 9, 6, 3, 8, 7, 4, 4, 9, 9, 6, 7, 6, 7, 1, 3, 9, 1, 3, 7, 7, 9, 2, 9, 9, 7, 6, 4, 9, 8, 3, 1, 8, 9, 2, 9, 5, 7, 5, 7, 5, 4, 5, 9, 8, 6, 7, 7, 7, 8, 5, 4, 8, 7, 6, 6, 8]
                    weights : [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
                  - # Reel[4]
                    symbols : [8, 4, 9, 3, 5, 8, 6, 5, 8, 8, 5, 7, 8, 8, 5, 9, 2, 7, 5, 6, 5, 8, 7, 4, 3, 9, 9, 3, 9, 8, 3, 4, 6, 4, 4, 8, 9, 8, 5, 6, 6, 9, 3, 8, 8, 3, 6, 8, 9, 8]
                    weights : [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
                  - # Reel[5]
                    symbols : [6,6,6,6,6]
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
      BaseReelChooseWeight: [1,1,1,1,1]
      FreeReelChooseWeight: [1,1]
      BaseMultiProb: [100,100,100,100,100,80,80,60,60,50,50,30,30,20,15,10,5]
      BaseMultiLvUp: [100,100,100,100,100,80,80,60,60,50,50,30,30,20,15,15,0]
      FreeMultiProb: [50,50,50,50,50,110,110,90,90,80,80,50,50,40,25,15,10]
      FreeMultiLvUp: [120,120,120,120,120,60,60,60,50,50,50,30,30,20,15,15,0]
    - # Mode:1 BuyFeaureFree
      BetMode: 1
      BaseReelChooseWeight: [1,1,1,1,1]
      FreeReelChooseWeight: [1,1]
      BaseMultiProb: [100,100,100,100,100,80,80,60,60,50,50,30,30,20,15,10,5]
      BaseMultiLvUp: [100,100,100,100,100,80,80,60,60,50,50,30,30,20,15,15,0]
      FreeMultiProb: [50,50,50,50,50,110,110,90,90,80,80,50,50,40,25,15,10]
      FreeMultiLvUp: [120,120,120,120,120,60,60,60,50,50,50,30,30,20,15,15,0]


```

遊戲邏輯

```go=
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
 fixed       *fixed1801
 accWin      int
 maxWinLimit int
 extendId    int
 exts        []*extend1801
}

func buildGame1801(gh *GameHandler) gameLogic {

 gs := gh.gameSetting //
 f := &fixed1801{
  fillScreenIdx:        make([]int, gs.GameModeSettingList[0].ScreenSetting.Columns),
  nowfillReelStripsIdx: make([]int, gs.GameModeSettingList[0].ScreenSetting.Columns),
  betmodes:             make([]betModes1801, len(gh.BetUnit)),
  screen:               make([]int16, gh.gameSetting.GameModeSettingList[0].ScreenSetting.ScreenSize),
  symbolTypes:          gh.gameSetting.GameModeSettingList[0].SymbolSetting.SymbolTypes,
 }

 // 讀設定檔
 if err := settings.DecodeFixed(gs, f); err != nil {
  log.Fatalf("game %s decode fixed failed : %s", gs.GameNameStr, err.Error())
 }

 for d := 0; d < len(gh.BetUnit); d++ {
  f.betmodes[d] = betModes1801{
   betMode:          d,
   baseReelLut:      sampler.BuildLookUpTable(f.BetModes[d].BaseReelChooseWeight), // 將權重轉換為 Lut
   freeReelLut:      sampler.BuildLookUpTable(f.BetModes[d].FreeReelChooseWeight), // 同上
   baseMultiProbLut: sampler.BuildLookUpTable(f.BetModes[d].BaseMultiProb),
   baseMultiLvUp:    f.BetModes[d].BaseMultiLvUp,
   freeMultiProbLut: sampler.BuildLookUpTable(f.BetModes[d].FreeMultiProb),
   freeMultiLvUp:    f.BetModes[d].FreeMultiLvUp,
  }
 }

 // 組裝
 g := &game1801{
  fixed:       f,
  accWin:      0,
  maxWinLimit: 0,
  extendId:    0,
  exts:        make([]*extend1801, 200),
 }

 size := gh.gameSetting.GameModeSettingList[0].ScreenSetting.ScreenSize
 for i := 0; i < 200; i++ {
  g.exts[i] = buildExtend1801(size)
 }

 return g
}

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

// ============================================================
// ** 此遊戲需要的額外結構宣告: Fixed設定宣告 **
// ============================================================

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

// 讀設定檔，目前狀態是 Weight 不是 LUT
type BetMode1801 struct {
 BetMode              int   `yaml:"BetMode"`
 BaseReelChooseWeight []int `yaml:"BaseReelChooseWeight"`
 FreeReelChooseWeight []int `yaml:"FreeReelChooseWeight"`
 BaseMultiProb        []int `yaml:"BaseMultiProb"`
 BaseMultiLvUp        []int `yaml:"BaseMultiLvUp"`
 FreeMultiProb        []int `yaml:"FreeMultiProb"`
 FreeMultiLvUp        []int `yaml:"FreeMultiLvUp"`
}

type betModes1801 struct {
 betMode          int         // 押注模式
 baseReelLut      sampler.LUT // 主遊戲起始輪id LUT表
 freeReelLut      sampler.LUT
 baseMultiProbLut sampler.LUT
 baseMultiLvUp    []int
 freeMultiProbLut sampler.LUT
 freeMultiLvUp    []int
}

// 隨機選擇 slice 中的某一元素

func (b *betModes1801) getBaseReelIdx(core *core.Core) int {
 return b.baseReelLut[core.IntN(len(b.baseReelLut))]
}

func (b *betModes1801) getFreeReelIdx(core *core.Core) int {
 return b.freeReelLut[core.IntN(len(b.freeReelLut))]
}

func (b *betModes1801) getBaseMult(core *core.Core) int {
 return b.baseMultiProbLut[core.IntN(len(b.baseMultiProbLut))]
}

func (b *betModes1801) baseMultLvUp(core *core.Core, nowIdx int) (bool, int) {
 prob := b.baseMultiLvUp[nowIdx]
 if core.IntN(1000) < prob {
  next := nowIdx + 1
  return true, next
 }
 return false, nowIdx
}

func (b *betModes1801) getFreeMult(core *core.Core) int {
 return b.baseMultiProbLut[core.IntN(len(b.baseMultiProbLut))]
}

func (b *betModes1801) freeMultLvUp(core *core.Core, nowIdx int) (bool, int) {
 prob := b.freeMultiLvUp[nowIdx]
 if core.IntN(1000) < prob {
  next := nowIdx + 1
  return true, next
 }
 return false, nowIdx
}

// ============================================================
// ** 此遊戲需要的額外結構宣告: extend拓展結果格式宣告 **
// ============================================================

type extend1801 struct {
 NowMulti      int   `json:"nowmulti"`      // 當前乘數
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

// ============================================================
// ** 遊戲主邏輯入口 **
// ============================================================

// getResult 主要介面函數 回傳遊戲結果 *res.SpinResult
func (g *game1801) getResult(betMode int, betMult int, gh *GameHandler) *result.SpinResult {
 g.maxWinLimit = gh.gameSetting.MaxWinLimit * betMult // 最高累計贏分值

 sr := gh.StartNewSpin(betMode, betMult)
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

func (g *game1801) getBaseResult(betMode int, betMult int, gh *GameHandler) *result.GameModeResult {
 mode := gh.GameModeHandlerList[0] //
 fixed := g.fixed                  // 遊戲特色設定
 sg := mode.ScreenGenerator
 sc := mode.ScreenCalculator
 gmr := mode.GameModeResult
 ext := g.exts[g.extendId]

 g.resetIdx()

 // 選取本次輪帶
 betmodeSets := fixed.betmodes[betMode]                              // 依照 betMode 獲取 betmodes 結構
 ReelsPicker := betmodeSets.baseReelLut.Pick(gh.core)                // betmodes 結構中獲取 baseReelLut 隨機選擇一組輪帶表的索引值
 fillReelStrips := mode.ScreenGenerator.ReelStripsGroup[ReelsPicker] // 補盤用的輪帶表

 // 1. 生成該round開局盤面
 screen := sg.GenScreenByAssignedReelStrip(ReelsPicker)
 copy(fixed.screen, screen)

 // 取得本次補珠輪帶起始位置
 for i := 0; i < len(fixed.fillScreenIdx); i++ {
  fixed.fillScreenIdx[i] = gh.core.IntN(len(fillReelStrips.ReelStripsReels[i].ReelSymbols))
 }

 for range 100 {
  // 2. 算分
  _ = sc.CalcScreen(betMult, screen, gmr)
  hm := gmr.HitMapTmp()

  // 3. 取原始 win
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

  // 8. 消除掉落
  fixed.screen = g.gravity(fixed.screen, hm, sg.Cols, sg.Rows, g.fixed.fillScreenIdx)
  screen = g.gravity(screen, hm, sg.Cols, sg.Rows, g.fixed.fillScreenIdx)
  gmr.FinishAct("Gravity", screen, nil) // 消除掉落盤面

  // 9. 提交step結果(step結束)
  gmr.FinishStep()
  ext = g.next()

  // 10. 補滿盤面
  screen = g.fillScreen(screen, &fillReelStrips, g.fixed.fillScreenIdx, g.fixed.nowfillReelStripsIdx, sg.Cols)
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

  // 選取本次輪帶
  betmodeSets := fixed.betmodes[betMode]
  ReelsPicker := betmodeSets.freeReelLut.Pick(gh.core)
  fillReelStrips := mode.ScreenGenerator.ReelStripsGroup[ReelsPicker]

  // fillReelStrips := &mode.GameModeSetting.GenScreenSetting.ReelStripsGroup[fixed.betmodes[betMode].getFreeFillReelIdx(gh.core)] // 指定補盤軸
  // 1. 生成該round開局盤面
  screen := sg.GenScreenByAssignedReelStrip(ReelsPicker)
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
   screen = g.fillScreen(screen, &fillReelStrips, g.fixed.fillScreenIdx, g.fixed.nowfillReelStripsIdx, sg.Cols)
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

// ============================================================
// ** 遊戲內部輔助函數實作 **
// ============================================================

// 0 代表不觸發 > 0 各自觸發
func (g *game1801) trigger(screen []int16) int {
 st := g.fixed.symbolTypes
 count := 0
 for _, sym := range screen {
  if st[sym] == enum.SymbolTypeScatter {
   count++
  }
 }
 if count < 4 {
  return 0
 }
 return min(count, 6)
}

// 重力掉落函數
func (g *game1801) gravity(screen []int16, hitmap []int16, cols int, rows int, buf []int) []int16 {
 // 先把要消除的地方改0
 for _, v := range hitmap {
  screen[v] = 0
 }
 // 逐欄由下而上做「就地壓縮」：
 //    wp = write pointer（寫入位置，從底部往上移），
 //    rp = read pointer（讀取位置，從底部往上掃）。
 for c := 0; c < cols; c++ {
  wp := (rows-1)*cols + c // 最底部該欄位索引
  // 將非 0 元素往下疊，保持欄內相對順序（穩定）
  for r := rows - 1; r >= 0; r-- {
   rp := r*cols + c
   if screen[rp] != 0 {
    if rp != wp {
     screen[wp] = screen[rp]
    }
    wp -= cols
   }
  }
  buf[c] = wp // 記錄下第c軸要補的位置
  // 上方殘餘位置補 0
  for w := wp; w >= 0; w -= cols {
   screen[w] = 0
  }
 }
 return screen
}

// 補盤面
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

func (g *game1801) resetIdx() {
 for i := 0; i < len(g.fixed.fillScreenIdx); i++ {
  g.fixed.fillScreenIdx[i] = 0
  g.fixed.nowfillReelStripsIdx[i] = 0
 }
}

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

func (g *game1801) getFreeMulti(screen []int16, betMode int, core *core.Core, ext *extend1801) int {
 multiGetter := g.fixed.betmodes[betMode]
 for pos, sym := range screen {
  g.fixed.screen[pos] = sym
  if sym == 1 {
   mult := multiGetter.getFreeMult(core)
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
