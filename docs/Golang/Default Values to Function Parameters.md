# Default Values to Function Parameters

### Functional options pattern

1. Create a struct to hold our arguments:
```go
type GreetingOptions struct {  
  Name string  
  Age  int  
}
```

2. Now let’s define the function:
```go
func Greet(options GreetingOptions) string {
  return "My name is " + options.Name + " and I am " + strconv.Itoa(options.Age) + " years old."
}
```

3. Define functional options for the fields in the struct:
```go
type GreetingOption func(*GreetingOptions)  
  
func WithName(name string) GreetingOption {  
  return func(o *GreetingOptions) {  
    o.Name = name  
  }  
}  
  
func WithAge(age int) GreetingOption {  
  return func(o *GreetingOptions) {  
    o.Age = age  
  }  
}
```

4. Create a wrapper:
```go
func GreetWithDefaultOptions(options ...GreetingOption) string {  
  opts := GreetingOptions{  
    Name: "Aiden",  
    Age:  30,  
  }  
  for _, o := range options {  
    o(&opts)  
  }  
  return Greet(opts)  
}
```

5. Use:
```go
greeting := GreetWithDefaultOptions(WithName("Alice"), WithAge(20))  
// Out: "My name is Alice and I am 20 years old."
```

Reference: https://medium.com/@func25/golang-secret-how-to-add-default-values-to-function-parameters-60bd1e9625dc