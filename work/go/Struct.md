 

對資料進行分組的操作，將不同的資料屬性共同形成一個 value。

## 1. 定義 Struct

開頭大寫代表可以在 Package 外調用。先定義一個 struct 出來，再創建 instance，最後調用 method。

```go=
type User struct {
    attr1 int 
    name  string
    ... // 其他 attr
}

// 創建 method
// reciver 是 value 或是 pointer 的差異?
func (u *User) GetName () {
    fmt.PrintLn(u.name)
}
func main (){
    // 創建 instance
    u User = User{
        attr1 int
        ... // 其他 attr
    }
    
    // 調用     
    fmt.Println(u.attr1)
}
```

## 2. Struct & Pointer

如果在函數中引入 Struct 的 pointer 當作參數，在函數內調用不需要在 de-referance ，這是 golang 的語法糖。

```go=
func name (u *User){
    fmt.Println(u.Name) // 不需要 de-referance
} 
```

## 3. 定義 Struct method

在 `func` 跟 func name 之間定義 receiver。

`mutation method` 可以寫一個函數來更新狀 instance 的狀態，但是需要注意的是 receiver 是 pointer 或 value 的差異，因為函數 input value 是會自動 copy 的。


## 4. 工廠函數(Constructor Function)

用於處理"創建某個 struct 的 instance" 這個任務的 Func 。

可以想到的是，創建這個 instance 是要用直接傳值的方式還是 pointer? 有什麼差別?

如果是用 return value 的方式那會 copy 一份給外部；如果是 return pointer 的時候返回的是創建的那個 struct 就不會產生 copy。當需要大量創建 instance 的時候，如果 return pointer 的時候就不會產生大量的 copy。


## 5. 匯出 package 的 struct 

當要匯入不同的 package 的 struct 的時候要先，import 其他 package 進來。

要注意的是匯出的 struct 名稱需要是大寫開頭，同時也要注意，裡面的屬性名稱也要是大寫開頭，這兩個東西是獨立看的(代表可以匯出 struct 而不匯出 屬性)

有些 建構函數如果分別存放在不同的 package 中會直接叫 New()，而不是 New...()。

## 6. Struct Embedding

struct 不是物件導向因此沒有繼承，而是用 embedding 實做嵌入。假設由一個父結構 User 子結構 Admin 那 User 要怎麼嵌入子結構?

### 範例
首先，在建立 嵌入式的 struct:

```go=
type User struct {
    Firstname string
    lastname string
    birthTime time.Time
}

type Admin struct {
    email string
    password string
    user User       // 嵌入
}
```

接下來，創建 instance 

```go=
return &admin{
    email: "..."
    password: "..."
    User: User{
        firstName: "..."
        lastName: "..."
    }
```


### 匿名嵌入

```go=
type User struct {
    Firstname string
    lastname string
    birthTime time.Time
}

type Admin struct {
    email string
    password string
    User       // 匿名嵌入 struct
}
```

接下來，創建 instance 

```go=
return &admin{
    email: "..."
    password: "..."
    User: User{
        firstName: "..."
        lastName: "..."
    }
```

## 7. 結論

 struct 對資料進行分組，可以寫一個建構函數用來專門處理創建 instance 的任務。並且在建構函數中添加驗證邏輯。
 
 struct 定義在不同的 package 中互相調用，大小寫就很重要了。關乎於能不能在外部調用。
 
一般來說，定義 method 需要注意的是 receiver 需要指向 struct 的 pointer 不然他會在執行這個函數的時候複製一份 struct(不會動到一開始創建的那個 instance) 但這份 copy value 也只會存在於這個 function 中。

最後提到 embedding struct，如果嵌入 struct 要創建 instance 要怎麼做?

## 8. 使用 type 的時機

type keyword 的功能，
``` go= 
type str string // 自定義資料型態
// 對 str 添加自定義 method

type 
```
