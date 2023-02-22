# Debugging 

## VSCode

Example of `launch.json`:
```json
{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Launch Package",
            "type": "go",
            "request": "launch",
            "mode": "auto",
            "program": "main.go"
        } 
    ]
}
```

Reference: https://blog.logrocket.com/debugging-go-vs-code/