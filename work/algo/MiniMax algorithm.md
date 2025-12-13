# 

MA(MiniMax algorithm) 的目標是最大化電腦的獲勝機率，最小化人類的獲勝機率。基於 Deepth First Search

## 1. 原理

MA 基於深度優先搜索與 Game Tree 的演算法。追求 loss 機率的最小的決策過程。MA 演算法假設所有遊戲參與者所做的決策都會基於理性的最佳決策(在每一回合都會選擇當前的最佳策略，白話說不放水)。

在實際應用中，MA 會用遞迴的方式對下一個回合的遊戲做決策，在樹中每一個終端節點(leaf nodes) 都會跟一個值做綁定。

結論是，首先 MA 會建立一個 Game Tree ，然後基於深度優先搜索，最後 end node 產生一個狀態(以井字遊戲而言就是 win、neutral、loss)每個狀態會對應一個值(比如說 win =1、neutral = 0、loss = -1) 

接下來，演算法會分成 mini layer 和 max layer。每一層分別對應遊戲在輪流的過程。

mini layer 會根據下一層節點的適應值選最小的當自己的適應值

max layer 會根據下一層節點的適應值選最大的當自己的適應值


<div style="text-align:center">
  <div style="display:flex; justify-content:center; gap:0;">
    <img src="https://hackmd.io/_uploads/HyT4ESnyZe.png"
         alt="" style="width:25%; height:auto; margin:0;">
    <img src="https://hackmd.io/_uploads/ry7v4BhJ-e.png"
         alt="" style="width:25%; height:auto; margin:0;">
    <img src="https://hackmd.io/_uploads/Byg1rShk-l.png"
         alt="" style="width:25%; height:auto; margin:0;">
    <img src="https://hackmd.io/_uploads/S1HbSBn1Zg.png"
         alt="" style="width:25%; height:auto; margin:0;">
  </div>
  <p style="margin-top:6px;">圖 1 mini layer、max layer</p>
</div>


 

<div style="text-align:center">
  <div style="display:flex; justify-content:center; gap:0;">
    <img src="https://hackmd.io/_uploads/H1p6vr2J-e.png"
         alt="" style="width:50%; height:auto; margin:0;">
    <img src="https://hackmd.io/_uploads/B1jzOB21-l.png"
         alt="" style="width:50%; height:auto; margin:0;">
  </div>
  <p style="margin-top:6px;">圖 1 mini layer、max layer</p>
</div>

## 2. 具體案例

通常 MA 演算法是用來建立電腦的決策模型，所以第一層會是根節點也就是 maximize layer ，電腦會自己嘗試最大化自己的勝率。

<div style="text-align:center">
  <img src="https://hackmd.io/_uploads/B1ozc421Zg.png" style="width:80%;">
    <p>圖 每個 end node 的適應值</p>
</div>

因為訓練的對象是電腦，所以根節點為先手(同時也是 maximize layer) maximize layer 的意義就是在於說會根據下一層的數值選最大的。


<div style="text-align:center">
  <img src="https://hackmd.io/_uploads/r1W3cH31Zl.png" style="width:80%;">
    <p>圖 每個 end node 的適應值</p>
</div>

因為是深度優先搜索所以由上至下，從左到右。去更新每個節點的適應值。


<div style="text-align:center">
  <div style="display:flex; justify-content:center; gap:0;">
    <img src="https://hackmd.io/_uploads/r1LBkUn1bx.png"
         alt="" style="width:33%; height:auto; margin:0;">
    <img src="https://hackmd.io/_uploads/SkbVII2yWg.png"
         alt="" style="width:33%; height:auto; margin:0;">
    <img src="https://hackmd.io/_uploads/Bk3vUU3J-g.png"
         alt="" style="width:33%; height:auto; margin:0;">
  </div>
  <p style="margin-top:6px;">圖 決策過程</p>
</div>



## 案例分析

首先要建立 Game Tree 這東西就是某個盤面的起始點，後面衍伸所有的可能組合的樹狀圖

<div style="text-align:center">
  <div style="display:flex; justify-content:center; gap:0;">
    <img src="https://hackmd.io/_uploads/HJC05Lnkbg.png"
         alt="" style="width:50%; height:auto; margin:0;">
      
  <img src="https://hackmd.io/_uploads/HyNtjL2k-l.png" style="width:65%;">
      
</div>  
    <p>圖 1 Game Tree(左) 轉換成 end node(右)</p>
</div>


利用 MA 演算法計算後得出以下結論，可以看到根節點(+1)說明了下一步的最佳決策是 +1 也就是中間那個決策。

<div style="text-align:center">
  <img src="https://hackmd.io/_uploads/r1qj2Lhkbe.png" style="width:80%;">
    <p>圖 每個 end node 的適應值</p>
</div>

## alpha-beta pruning 

這就是 MiniMax algorithm 的改良版，

### 為什麼會需要提升? 
因為利用 MA 求解的 Game Tree 可能非常巨大(光是井字遊戲就有 9! 種可能了) 所以當巨大的 Game Tree 會造成 DFS 跑的特別久。，所以借助 alpha-beta pruning 的方法提升效能(也就是運行的速度)

當 game tree 趨近於無限大的時候有些節點可能無法被獵具出來。

基於降低時間複雜度的原因，原始的 MA 的時間複雜度會是 $O(\text{最大分支數}^\text{層數})$ 經過使用了 alpha-beta pruning 時間複雜度降低為 $O(\sqrt{\text{最大分支數}^\text{層數}})$


### 計算方式
現在的目標是要判斷要不要修剪某個分支，現在在每個節點中添加兩個參數( $\alpha$ 跟 $\beta$ )，$\alpha$ 參數用來儲存在 maximize layer 最高適應值，$\beta$ 用來儲存  miniimize 最小值。
* **$\alpha$ 的意義:** 對「Max 那一方」來說，目前沿著這條路徑，已經找到的「最好（最高）的分數」。
* Max layer 至少可以保證拿到這麼高的分數。
* **$\alpha$ 初始值:** 一開始設為 負無限大。
* **$\beta$ 的意義:** 對「Min 那一方」來說，目前沿著這條路徑，已經找到的「最好（最低）的分數」。
* **$\beta$ 初始值:** 一開始設為 正無限大。


如果 $\alpha \ge \beta$ 就表示後面的分支再看也不可能改變雙方已知的最好結果，所以可以「剪掉」那部分，不用繼續算，這就是 α–β 剪枝的核心。




## 參考文獻

* [AI - Ch4 極大極小搜尋法與剪枝 Minimax Algorithm and Alpha-beta Pruning](https://www.mropengate.com/2015/04/ai-ch4-minimax-alpha-beta-pruning.html)
* [Alpha-Beta Pruning](https://ithelp.ithome.com.tw/m/articles/10355817)

