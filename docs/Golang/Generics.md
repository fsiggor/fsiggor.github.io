# Generics

## Intro

**With generics, we can declare and use functions or types that are written to work with _any_ _type_ of a _set of types_ provided.**

Simply, your generic functions and types will work with any number of types that you define them for, hence making them more useful in a broader sense in your Go program or project as a whole.

```go
package main

import (
	"fmt"
)

// Concats the string values of map m.
func ConcatStr(m map[string]string) string {
	var s string
	for _, v := range m {
		s += v
	}
	return s
}

// Concats the int values of map m.
func ConcatInt(m map[string]int) int {
	var s int
	for _, v := range m {
		s += v
	}
	return s
}

// Concat generic function
func ConcatGeneric[K comparable, V Concat](m map[K]V) V {
	var s V
	for _, v := range m {
		s += v
	}
	return s
}

type Concat interface {
	string | int
}

func main() {
	// Initialize a map for the int values
	map_string_int := map[string]int{
		"first":  13,
		"second": 26,
		"third":  39,
	}

	// Initialize a map for the string values
	map_string_string := map[string]string{
		"first":  "firstval",
		"second": "secondval",
		"third":  "thirdval",
	}

	// call the two functions
	fmt.Println("Concat outputs from the functions: \n",
		ConcatInt(map_string_int), "\n",
		ConcatStr(map_string_string))

	// call the generic function with two kinds of inputs
	fmt.Println("Concat with generic function: \n",
		ConcatGeneric(map_string_int), "\n",
		ConcatGeneric(map_string_string))
}
```

Reference: https://medium.com/this-code/understanding-golang-generics-with-examples-907cfbd5023b
