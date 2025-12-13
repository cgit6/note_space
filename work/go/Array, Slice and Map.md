
## 定義 Array

需要知道

```go=
var arr [4]int = [4]int{0,0,0,0} // 宣告元素為 int 長度為 4 的 array
```

## 定義 Slice

```go=
var arr [4]int = [4]int{0,1,2,3} // arr

arr[:3]  // slice 從開頭到索引位置 3 前
arr[1:3] // slice 從索引 1 到 索引 3
arr[1:]  // slice 從索引 1 到 最後 
```

同時也可以對 slice 建立新的 slice。

建立 slice 的時候不會進行 copy array 的操作，所以非常節省記憶體位置，效果有點像 pointer。

slice 需要注意的是他的長度有兩個一個是 len(slice 本身的長度) 另一個是 cap(他指向的 array 的長度，但也不是 array 長度，應該說是 從 slice 這個起始點開始到 這個array 結束的長度)

再來就是 slice 可以索引到超過他自身長度的值，slice 起始位置到 array 最後的值都可以索引。

## Append to dynamic slice

在 go 中 array 是一個固定長度的陣列，然而 slice 可以做一個動態的陣列，但隨之而來的就是會有擴容的問題。

如果對一個 slice 添加 item 時，如果添加的索引值超過 slice 本身則會出現錯誤。這時候可以使用 `append(slice,item)` 來處理。

那如果要對 slice 中的元素進行移除

```go=
arr := []int{1,3,4}
sl := arr[:2]

// 對 slice 進行操作
sl[1:] // 移除第一個元素
sl[:2] // 移除最後一個元素
sl [:0] // 移除所有元素
```

### marge list

需要在這裡了解新的語法是 unpack 的作法。

```go=
arr1 = []int{1,2,3}
arr2 = []int{4,5,6}
arr3 = append(arr1, arr2...)
```

## make() in slice

假設現在有個情境1，已經初始化一個空的陣列了，接下來會怎麼添加元素到該陣列中? 如果使用 append 會發生什麼事? append(arr,item) 會創建一個新的陣列，所以調用一次append 就需要創建一個新的 arr 並指向他。這是會消耗效能的。

情況2 如果今天先創建一個空陣列，並且用 arr[i]=x 的方式 assign 那當 index 值超過 陣列長度就會出現錯誤。

因此，現在有一個函數make(arr, len, cap) 用來預先初始化一個足夠長的陣列，然後再用 index 做 assign 這樣就不會出現錯誤了。

## 定義 Map

map 由 key value 組成， key 可以是 任意資料型態， value 也可以是任意資料型態。 Map 是動態的資料結構所以可以添加元素不會有任何問題。

```go=
word := map[string]string{
    "a": "apple",
    "b": "banana"
} 
```

添加/刪除 key/value pair

```go=
word := map[string]string{
    "a": "apple",
    "b": "banana"
} 

word["c"] = "cat" // 添加 pair
delete(word,"c") // 刪除 pair
```

### Map 跟 Struct 的差別

Map 可以動態的更新資料格式但是 Struct 不行。map 比較適合用於 在 一個區塊中添加類似的一筆 key value pair 但是 Struct 則是創建 instance 根據用途選擇合適的資料結構。

### make() on Map

如果今天預先知道了要創建的 map 長度有多少，利用 make() 來預處理。make(map[string]string, len) ，然後再對其 assign。

## 自定義資料結構

```go=
type floatMap map[string]float64

func (u floatMap) Output () {
    fmt.Println("m: ",m)
}
```

## looping array,slice map

利用 for loop 加上 range 語法，

```go=
for index, value := range arr {
    fmt.Println(index)
    fmt.Println(value)
}

for key, value := range map {
    fmt.Println(key)
    fmt.Println(value)
}
```
