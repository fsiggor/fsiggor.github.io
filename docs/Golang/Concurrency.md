# Concurrency

## Introduction

It is the ability to execute multiple tasks or processes simultaneously, that allows efficient use of system resources and improves application performance.

	Note that concurrency and parallelism are two different terms. Concurrency it’s meant to do `multiple tasks` at the `same time`. It is a term used for writing programs. Parallelism it’s meant to do `multiple tasks` with `multiple resources` at `the same time` . It is hardware related term, used when building CPUs and cores.

## Goroutines and channels

Goroutines and channels are mainly used for achieving concurrency in Golang:

- **Goroutines:**  can be thought of as functions that run independently in the background, allowing the program to perform multiple tasks simultaneously.
- **Channels:** are an essential part of concurrency in Go, allowing Goroutines to communicate with each other and share data.

```go
package main  
  
import (  
 "fmt"  
 "strings"  
)  
  
func analyzeSentiment(data string, resultChan chan string) {  
 // Perform sentiment analysis on the input data  
 // Here, we simply check if the input contains the word "happy"  
 if strings.Contains(strings.ToLower(data), "happy") {  
  resultChan <- "positive"  
 } else {  
  resultChan <- "negative"  
 }  
}  
  
func main() {  
 // Define the input data  
 input := []string{  
  "I am so happy today!",  
  "I hate this weather.",  
  "Happy birthday!!",  
 }  
  
 // Create a channel for the sentiment analysis results  
 resultChan := make(chan string)  
  
 // Launch a goroutine to analyze the sentiment of each input string  
 for _, data := range input {  
  go analyzeSentiment(data, resultChan)  
 }  
  
 // Wait for the results to be processed and print them  
 for i := 0; i < len(input); i++ {  
  fmt.Println(<-resultChan)  
 }  
}
```

## Waitgroups

Waitgroups provide a way to synchronize the execution of Goroutines and ensure that all Goroutines have been completed before terminating.

```go
package main  
  
import (  
 "fmt"  
 "strings"  
 "sync"  
)  
  
var wg sync.WaitGroup // Initialize waitgroup  
  
func analyzeSentiment(data string, resultChan chan string) {  
 // Signal that the goroutine has completed its work  
 defer wg.Done()  
  
 if strings.Contains(strings.ToLower(data), "happy") {  
  resultChan <- "positive"  
 } else {  
  resultChan <- "negative"  
 }  
}  
  
func main() {  
 input := []string{  
  "I am so happy today!",  
  "I hate this weather.",  
  "Happy birthday!!",  
 }  
  
 resultChan := make(chan string)  
  
 for _, data := range input {  
  // Add one to the waitgroup for each goroutine  
  wg.Add(1)  
  go analyzeSentiment(data, resultChan)  
 }  
  
 go func() {  
  // Wait for all goroutines to complete  
  wg.Wait()  
  // Close the result channel to signal the workers to terminate  
  close(resultChan)  
 }()  
  
 // Print the results  
 for i := 0; i < len(input); i++ {  
  fmt.Println(<-resultChan)  
 }  
}
```

## Mutex

Mutex(mutual exclusion) working on a locking mechanism. When a resource is acquired by one process, add a lock, and after finishing it, unlock it.

```go
package main  
  
import (  
 "fmt"  
 "strings"  
 "sync"  
)  
  
// Create a mutex to synchronize access to the counter variable  
var mu sync.Mutex  
var wg sync.WaitGroup  
  
func analyzeSentiment(data string, resultChan chan string, counter *int) {  
  
 defer wg.Done()  
  
 if strings.Contains(strings.ToLower(data), "happy") {  
  // Acquire the lock before accessing the shared counter variable  
  mu.Lock()  
  *counter++  
  mu.Unlock()  
  resultChan <- "positive"  
 } else {  
  resultChan <- "negative"  
 }  
}  
  
func main() {  
 input := []string{  
  "I am so happy today!",  
  "I hate this weather.",  
  "Happy birthday!!",  
 }  
  
 resultChan := make(chan string)  
  
 // Create a counter variable to track the number of positive sentiments  
 counter := 0  
  
 for _, data := range input {  
  wg.Add(1)  
  go analyzeSentiment(data, resultChan, &counter)  
 }  
  
 go func() {  
  wg.Wait()  
  close(resultChan)  
 }()  
  
 // Print the results  
 for i := 0; i < len(input); i++ {  
  fmt.Println(<-resultChan)  
 }  
  
 // Print the number of positive sentiments  
 fmt.Printf("%d out of %d input strings had a positive sentiment.\n", counter, len(input))  
}
```

## Worker

A worker is a goroutine that performs a specific task or set of tasks in the background, independently of the main program or other workers.

```go
package main  
  
import (  
 "bufio"  
 "fmt"  
 "os"  
 "strings"  
 "sync"  
)  
  
var mu sync.Mutex  
var wg sync.WaitGroup  
  
func analyzeSentiment(data string, resultChan chan<- string) {  
 if strings.Contains(strings.ToLower(data), "happy"){  
  resultChan <- "positive"  
 } else {  
  resultChan <- "negative"  
 }  
}  
  
func worker(inputChan <-chan string, resultChan chan<- string, k int) {  
  
 defer wg.Done()  
  
 for data := range inputChan {  
  analyzeSentiment(data, resultChan)  
  
  // Acquire the lock to access worker  
  mu.Lock()  
  fmt.Printf("Worker %d processed line: %s\n", k, data)  
  mu.Unlock()  
 }  
  
}  
  
func main() {  
 inputChan := make(chan string, 10)  
 resultChan := make(chan string, 10)  
  
 // Launch two worker goroutines to process the sentiment analysis results  
 for i := 0; i < 2; i++ {  
  wg.Add(1)  
  go worker(inputChan, resultChan, i)  
 }  
  
 // Read lines from stdin and send them to the workers  
 scanner := bufio.NewScanner(os.Stdin)  
 for scanner.Scan() {  
  line := scanner.Text()  
  inputChan <- line  
 }  
 close(inputChan)  
  
 go func() {  
  wg.Wait()  
  close(resultChan)  
 }()  
  
 numPositive := 0  
 numNegative := 0  
 for result := range resultChan {  
  switch result {  
  case "positive":  
   numPositive++  
  case "negative":  
   numNegative++  
  }  
 }  
  
 // Print the results  
 fmt.Printf("Positive: %d\n", numPositive)  
 fmt.Printf("Negative: %d\n", numNegative)  
}
```

References:
- [A Practical Guide to Concurrency in Golang](https://blog.canopas.com/a-practical-guide-to-concurrency-in-golang-key-terms-and-examples-aa54dddb9fec)