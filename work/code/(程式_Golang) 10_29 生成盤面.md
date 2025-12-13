

```go=

var REELSTRIPS = [][]int{
	{0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 2, 3, 4, 5, 6, 7, 8, 9, 10},
	{0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 2, 3, 4, 5, 6, 7, 8, 9, 10},
	{0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 2, 3, 4, 5, 6, 7, 8, 9, 10},
	{0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 2, 3, 4, 5, 6, 7, 8, 9, 10},
	{0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 2, 3, 4, 5, 6, 7, 8, 9, 10},
}

type ScreenGenerator struct {
	ScreenSize int // ScreenSize : 盤面大小（一個盤面上的圖標總數）
	Rows       int
	Cols       int
	ReelStrips [][]int  // 一組輪帶表，可以產生一個盤面
	ReelLens   []int    // 每個 reel 的長度（做取 mod 用），恆為 5 個
	Symbols    []string // 數字代號 -> 符號名稱的對照表（索引 = 代號）
	ScreenBuf  []uint8  // 盤面結果的緩衝(一次宣告，熱路徑中0分配)
	rng        *rand.Rand
}

// 
func NewScreenGenerator() *ScreenGenerator {
	c := &ScreenGenerator{}
	c.Rows = 3
	c.Cols = 5
	c.ScreenSize = c.Rows * c.Cols
	c.ReelStrips = REELSTRIPS
	c.ReelLens = make([]int, c.Cols)

	c.Symbols = []string{"None", "Scatter", "Wild", "H1", "H2", "H3", "H4", "L1", "L2", "L3", "L4", "L5"}
	c.ScreenBuf = make([]uint8, c.ScreenSize)
	// ReelLens 賦值
	for i, r := range c.ReelStrips {
		c.ReelLens[i] = len(r)
	}
	c.rng = rand.New(rand.NewSource(time.Now().UnixNano()))

	return c
}

// GenScreen 產生盤面結果
func (c *ScreenGenerator) GenScreen() []uint8 {
    // 
	for i := 0; i < len(c.ReelLens); i++ {
		idx := c.rng.Intn(c.ReelLens[i])
		for j := 0; j < c.Rows; j++ {
			c.ScreenBuf[i*c.Rows+j] = uint8(c.ReelStrips[i][(idx+j)%c.ReelLens[i]])
		}
	}
	return c.ScreenBuf
}

// 呼叫方式 
// sg := NewScreenGenerator() // 創建 NewScreenGenerator instance
// screen := sg.GenScreen() // 調用方法


```