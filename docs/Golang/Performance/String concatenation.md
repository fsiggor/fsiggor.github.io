It is generally more efficient to use the `bytes.Buffer` type to build strings rather than concatenating strings using the `+` operator.

Look at this poor performance code:
```go
s := ""  
for i := 0; i < 100000; i++ {  
  s += "x"  
}  
fmt.Println(s)
```

This code will create a new string on each iteration of the loop, which can be inefficient and may lead to poor performance.

Instead, you can use the `strings.Builder` to build the string more efficiently:

```go
var builder strings.Builder  
  
for i := 0; i < 100000; i++ {  
  builder.WriteString("x")  
}  
  
s := builder.String()  
fmt.Println(s)
```

Reference: https://medium.com/@func25/go-performance-boosters-the-top-5-tips-and-tricks-you-need-to-know-e5cf6e5bc683