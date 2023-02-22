The `govet` tool is a static analysis tool without running code that can help you find potential issues in your Go code.

`govet` checks your code for all sorts of problems that could cause bugs or lead to poor performance. It's like a code quality police, constantly checking to make sure you're not doing anything stupid.

To use `govet`, you can run the `go tool vet` command and pass the names of the Go source files you want to check as arguments:

```
go tool vet main.go
```

Reference: https://medium.com/@func25/go-performance-boosters-the-top-5-tips-and-tricks-you-need-to-know-e5cf6e5bc683