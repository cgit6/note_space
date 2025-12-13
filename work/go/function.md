# function

## func 定義

...


## 2. 進階 func

### 函數作為值傳遞

func 在 go 中是一個 first class function ，所以可以當作 value 來傳遞。

當作 input 進行傳遞，需要注意的是需要寫清楚他的 type，但也可以在文件上方定義 type ... 寫清楚後直接調用 type name


當作 output 進行傳遞時，舉個例子可以做一個邏輯判斷，如果是這樣 返回 func1 如果是那樣返回 func2。

接下來是匿名函數，可以在函數中直接放一個沒有定義名稱的函數

最後，函數還可以利用 closure 製作工廠函數。

### 遞迴

寫一個自己呼叫自己的函數，簡單的計算 5! 


### 動態輸入值

將 a,b,c,d 存到一個
```go=
sum(a,b,c,d)

fun sum(list ...int){
    for i,num := range list {
        ...
    }
}
```





































