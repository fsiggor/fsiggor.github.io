
### Normal Enum:

```go
type Color int  
  
const (  
  _                       // Skip a number zero or define a default value
  Red   Color = iota + 1  // 1  
  Blue                    // 2  
  Green                   // 3  
)
```

### Flags Enum:

```go
type DamageType int  
  
const (  
  Poison   DamageType = 1 << iota // 1  
  Bleeding                        // 2  
  Flame                           // 4  
)

// Has returns a boolean indicating whether the specific flag is present in the set  
func Has(set, flag int) bool {  
  return set&flag == flag  
}  
  
// Remove creates a new set of flags with the specific flag removed and returns it  
func Remove(set, flag int) int {  
  return set &^ flag  
}  
  
// Add returns a new set of flags with the specific flag added  
func Add(set, flag int) int {  
  return set | flag    
}

func main() {  
  damages := Poison | Flame  
  fmt.Println(damages.Has(Flame))    // true  
  fmt.Println(damages.Has(Bleeding)) // false  
}
```

### Namespace Enum:

```go
type Color int  
  
var ColorEnum = struct {  
    Red   Color  
    Blue  Color  
    Green Color  
  }{  
    Red:   0,  
    Blue:  1,  
    Green: 2,  
}  
  
func main() {  
  fmt.Println(ColorEnum.Red)  
}
```

Reference: https://levelup.gitconnected.com/go-enums-the-right-way-to-implement-and-iterate-9b1e233c8d9a