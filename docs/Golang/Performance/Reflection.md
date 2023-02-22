Reflection is a powerful feature of Go that allows a program to introspect and modify its own structure and behavior at runtime.

You can use reflection to determine the type of a value, access its fields, and call its methods.

```go
package main  
  
import (  
  "fmt"  
  "reflect"  
)  
  
func main() {  
  x := 100  
  v := reflect.ValueOf(x)  
  t := v.Type()  
  fmt.Println("Type:", t) // "Type: int"  
}
```

When using reflection, it involves introspection and manipulation of values at runtime, rather than at compile time.

The Go runtime must perform additional work to determine the type and structure of the reflected value, which can add overhead and slow down the program.

Reflection can also make code more difficult to read and understand, which can impact productivity.

Reference: https://medium.com/@func25/go-performance-boosters-the-top-5-tips-and-tricks-you-need-to-know-e5cf6e5bc683
