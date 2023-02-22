# Reflection in Go

Reflection in Go allows you to examine and manipulate variables and types while your program is running. This means that you can check the type of a variable, change its value, or even call its methods.

The **reflect** package has two main types, `reflect.Type` and `reflect.Value`, which allow you to examine the type and value of a variable.

You can use the `reflect.TypeOf()` and `reflect.ValueOf()` functions to obtain the type and value of any value, respectively.

```go
package main  
  
import (  
    "fmt"  
    "reflect"  
)  
  
func main() {  
    num := 123  
    numType := reflect.TypeOf(num)  
    numValue := reflect.ValueOf(num)  
    fmt.Println("Type:", numType)  
    fmt.Println("Value:", numValue)  
}  
  
// Type: int  
// Value: 123
```

### `reflect.Value`

The `reflect.Value` type is one of the key types in the reflect package in Go. It acts as a wrapper around a value, allowing you to obtain information about it and perform operations on it.

For instance, you can use the `Kind()` method to determine the type of value that x is (in this case, an int) or use the `Int()` method to get the integer value of x. Additionally, you can change the value of x using the `Set()` method

```go
package main

func main() {  
    x := 10   
    p := &x  
    v := reflect.ValueOf(p)  // v is reflect.Value of pointer of x  
  
    fmt.Println("Kind of x:", v.Kind())  // "ptr"  
  
    v = v.Elem()  // now v is reflect.Value of x (not pointer anymore)  
  
    fmt.Println("Kind of x:", v.Kind())  // "int"  
  
    fmt.Println("Value of x:", v.Int())  // 10  
  
    v.SetInt(20)    
    fmt.Println("Value of x after change:", x)  // 20  
}
```

**Important**: note that a `reflect.Value` holds a value, not the variable itself. If the value is a pointer to a struct, the `reflect.Value` will hold the pointer, not the value that the pointer points to.

### `reflect.Type`

The `reflect.Type` in Go is like a comprehensive guide to types, providing all the necessary information about a type, such as its name and composition. It acts as a template, providing all the information you need to know about the type.

You can use it to find information about a type, like its name, or to determine the type of a variable, such as struct, slice or pointer.
```go
package main

type Car struct {  
    Model string  
    Year int  
    EngineSize float64  
}  
  
func main() {  
    var car Car  
    t := reflect.TypeOf(car)  
  
    fmt.Println("Name:", t.Name()) // "Car"  
  
    fmt.Println("Kind:", t.Kind()) // "struct"  
  
    fmt.Println("Number of fields:", t.NumField()) // 3  
  
    // iterate all fields of Car struct  
    for i := 0; i < t.NumField(); i++ {  
        field := t.Field(i)  
        fmt.Println("Field name:", field.Name)  
        fmt.Println("Field type:", field.Type)  
    }  
}  
  
// Field name: Model  
// Field type: string  
// Field name: Year  
// Field type: int  
// Field name: EngineSize  
// Field type: float64
```

### **Common Usages**

Reflection is a powerful feature in Go that can be used for various purposes, such as:

- **Custom struct tag:** This technique allows you to add custom metadata to struct fields, which can be accessed and used at runtime. [See](https://medium.com/@func25/custom-struct-tag-technique-in-go-8667bf7da457)
- **Dynamic type checking and type assertions:** You can check the type of a variable at runtime and perform type assertions to ensure that a variable is of the expected type.
- **Iterating over struct fields:** You can use reflection to iterate over the fields of a struct, even if the struct type is unknown at compile time.
- **Implementing dependency injection:** Reflection can be used to implement dependency injection frameworks, by using the `ValueOf` and `Set` methods of the reflect package to set the fields of structs at runtime.

And much more, reflection is used in many packages to create useful utilities.

Reference: https://levelup.gitconnected.com/reflection-in-go-everything-you-need-to-know-to-use-it-effectively-52c78da1f4ff