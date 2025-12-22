# Crawler lab

## 功能

設計一個高效能系統，負責控制機器管理(創建 machine 、關閉 machine)。對每一台 machine 自動化控制(一台 machine 需要蒐集滿 5000 次 base spin)，數據收集，分析收集結果。

所以現在需要創建一個執行打開爬蟲系統的函數，這個函數會創建一個 機器管理的實例，他會負責調控當前機器的數量，數據收集情況。

### 面臨的挑戰

- 穩定獲取 Spin 數據
- 不掉線
- 自動化
- 高效能(蒐集 1 億局的前提下，對多開的效能以及網路 ip 位置)
- 防止被擋

## 待解決的問題

### 操作問題

- 進入遊戲需要按一下空白鍵，然後設定自動轉 1000 spins ， UnitBet 多少無所謂。
- 如果滿 1000 次 spin 再 1000 次 spin 一個 machine 跑滿 4500 次，需要開 10000 台，共 4500 萬次 spins 呼叫。

## 待解決的問題

### 操作問題

- 進入遊戲需要按一下空白鍵，然後設定自動轉 1000 spins ， UnitBet 多少無所謂。
- 如果滿 1000 次 spin 再 1000 次 spin 一個 machine 跑滿 4500 次，需要開 10000 台，共 4500 萬次 spins 呼叫。
- 數值需要校正，每次開始餘額都不同，下注金額也不同，需要對此進行統計上的校正

### 效能壓力

- machine 大量設置: 假設花 3 天進行數據收集，每一台 machine 收集 4500 筆數據需要 4 小時，三天內要跑完需要同時開 1667 台 machine 同時收集數據，對效能是一個挑戰。

- 前端渲染對效能的消耗: 有沒有可能單純跟後端 api 互動就好了省去前端渲染的效能消耗，因為前端的關係數據獲取的進度難以達標

## 系統架構

建立 make 檔案，可以利用 make file 下指令，在命令行可以定義 -> 同時開多少台 machine，一台 machine 收集多少次 spin 等。

系統第一步:建立 "控制器" 負責創建 machine 實例，調控 machine 數量同時保持在線數量 n 台，如果 machine 滿足收集的 spin 次數，能正確的關閉。並再開新的 machine 實例

爬取資料
自動化操作
獲取 socket
二進位資料

### 設定檔

```yaml=

1. 入口 url
2. 儲存到哪
3. 自動化參數

```

### Config 模組

`Config` 模組負責解析 yaml 檔，yaml 檔裡面存放根據觀察所了解的資料格式在此定義，以及遊戲參數可以用來做驗證。

```python=

class Config:
    def __init__():
        self.url # 入口網址
        self.outputStruct # 輸出結構

    def parse(self):
        # 解析 設定檔

        # 更新數值
        self.url = ...
        self.outputStruct = ... # 輸出結構
```

### 主要的執行函數

```python=
def runner():
    # 命令行
    # 這裡應該是要獲取命令行所定義的參數，比如說，要爬哪個遊戲 可以維護一個 enum 清單
    # 獲取最多要開幾台
    # 獲取每一台 Machine 最多要收集幾次 spins


    # 解析 yaml 設定檔
    # cfg = Config() # 讀取設定檔
    # # 驗證資料正確性

    # 創建 Control 實例
    # 執行 Control.cntrHandler()

```

### Control 模組

一台機器可以給一個玩家(收集數據)、同時創建多台機器給多個玩家玩(1 對 1 收集數據)、

Control 模組主要負責控制 Machine 實例的開啟與關閉，確保效能最佳化。

```py=
class Control:
    def __init__(spin):
        # 當前 Machine 數量
        # 最大 Machine 數量上限
        # 紀錄 Machine 運行情況
        # 已經收集幾台了

        # 在這邊放分析工具?

    # 創建與關閉 Machine 的控制功能
    def cntrHandler():

        # 查看當前數量
        while True:
            # 檢查當前 Machine 數量

            # 如果低於設定數量
            if 低於設定數量:
                self.open()
                # 更新 當前 Machine 數量
```

### Machine 模組

Machine 模組會開啟一個獨立的瀏覽器環境，在這個瀏覽器環境負責監聽 spin 結果

```py=
class Machine:
    def __init__(spinTime):

        self.cfg = # 設定檔模組(這款遊戲的已知參數)
        self.nowSpin = 0 # 累積成功spin 次數
        self.spinTime = spinTime # 最多 spin 的次數

        self.spinResult = result 模組 # 初始化 spin 緩存，儲存結果(預先開一個記憶體位置，儲存所有 spin 結果嗎?)
        self.collect = Collect # 初始化資料收集模組


    # 真的點擊一下遊戲介面的 spin btn 並監聽結果，解析資料並儲存資料
    def run()

        for i in range(self.spinTime):
            # 1. 利用 self.collect 模組點擊螢幕觸發 spin
            # 2. 檢查接收到的數據是否正確
            # 3. 將結果存到 self.spinResult
            # 4. 更新當前累積次數

            # 5. 他有可能因為遊戲過程輸特別多次而提早結束無法滿足 4500，所以這邊需要判斷餘額剩下多少的時候要停下來但是這裡依然是有意義的資料

            # 6. 隨機等待一段時間


    def open(self):
        # 打開 Machine
        pass

    def close(self):
        # 關閉 Machine
        # 清除瀏覽器紀錄
        # 清除緩存等等(也不一定)
        # 關閉瀏覽器
```

### Collect 模組

在開始爬蟲遊戲數據前會有如何解析獲取數據的問題，利用 yaml 檔案去定義獲取的數據結構。利用 yaml 定義資料應該如何被儲存。會是好的選擇嗎?

收集一次 spin 的結果返回給

```py=
class Collect:
    def __init__():
        # self.auto = Auto # 自動化模組，比如點擊這種的
        #
        self.queue1 # 資料格式是 queue
        self.spinResult # 一次 spin 的結果緩存
        self.queue2 #


    # 這邊我預計設計成 "拿資料" 跟 "解析" 兩件事分別獨立進行，利用 quequ 串聯工作流程
    # 解析又跟 存到資料庫獨立進行
    def spin(self):
        # 1. self.auto.click() 點擊
        # 2. 以 seth 為例，監聽 socket 的二進位 respone
        # 2.1 存入 self.queue 緩存當中
        # 3. 從 self.queue 緩存拿一筆資料解析二進位內容
        # 4. 格式檢查
        # 4.1. 存到緩存 self.queue2
        # 5. self.queue2 儲存資料到 self.spinResult 或是資料庫?




```

存放所有自動化操作的模組

```python=
class Auto:
    def __init__():
        # 位置從哪裡開始
        # 隨機值
        # 間隔多少時間執行一次
        # 幾秒後開始執行

    def click(self):
        # 起始位置
        # 從起始位置點擊一下的操作，可以加一些隨機量

    def drag(self):
        # 起始位置
        # 從起始位置進行拖曳

```

解析資料

```python
class Parse:
    def __init__(需要解析的數據,解析方法):
        self.result # 解析結果，這裡的資料結構又受到設定檔的限制
        self.map # 可以找到對應的解析函數

    def parse(self)
        return parse[解析方法](需要解析的數據)

    def method1(self):
        # 方法1
        pass
```

[問題 1]現在 "賽特 1" 盤面儲存在一個 "二進位"，需要解析後獲得當前盤面訊息，生成盤面 1 條 "二進位"，每掉落消除 1 次返回 1 條 "二進位"。

- 判斷當前是 "生成盤面" 還是 "掉落消除"
- 如果是 "生成盤面" 儲存盤面、贏分情況、贏分符號、贏分符號數量、乘數符號...
- 如果是 "掉落消除" 儲存盤面、補盤內容(掉落下來的內容)、贏分情況、贏分符號、贏分符號數量、乘數符號...

- 已知遊戲設定，放在 yaml 設定檔。比如說 "符號清單" 對應的數值。
- 他們一定會有 n 組輪帶表，有辦法知道他們是用哪一組嗎?

[問題 2]

### 數據儲存模組

資料會被儲存到

### 數據分析

採集來的數據需要怎麼使用? 目前方案是參考 prob lab 看結果，多玩家的情況下利用獲取的數據進行在解析與整理後進行統計計算。

## 腳本解讀

### olympus.py
