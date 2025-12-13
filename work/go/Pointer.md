
函數在傳遞 pointer 當作 inout 的時候會直接獲取該記憶體位置的值(不會產生 copy value)，同時也會直接對函數外的變數值做改變(side effect)。

```go=
var age = 32

// agePointer := &age
agePointer *int
agePointer = &age

```

dereferance: 如果要獲取這個記憶體位置的值，在pointer value 前面加上 `*` 字元

Pointer null value


在 go 中不能對 pointer 進行運算，但是可以在函數中傳遞 pointer 在裡面做運算，然後這當然也會改變外面的數值，也可以看到這裡不需要 return 任何東西就可以改變外面的值了(修改而不回傳)。

<div style="text-align:center">
  <img src="https://hackmd.io/_uploads/B1xYSgXfgZe.png" style="width:60%;">
    <p>圖 1 函數運算</p>
</div>


## 應用場景

* slot game 中有兩種算分模式要在某個函數中進行，可以將整個 struct 的 pointer 當作參數傳遞給那個函數。
* 如果返回一個固定的 rusult struct 只需要指定他就行了

