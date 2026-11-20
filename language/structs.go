package language

import (
	"fmt"
	"os"
)

type GoSyhException struct {
	Type       string
	Message    string
	Filename   string
	LineNumber int
	LineText   string
	SourceErr  error
	ExitCode   int
}

func (e *GoSyhException) Raise() {
	out := os.Stderr
	fmt.Fprintf(out, "\n\033[31m┌─ ERROR [%s] ───────────────────────────────\033[0m\n", e.Type)
	fmt.Fprintf(out, "\033[31m│\033[0m File:   %s (line %d)\n", e.Filename, e.LineNumber)
	fmt.Fprintln(out, "\033[31m│\033[0m")
	fmt.Fprintf(out, "\033[31m│\033[0m   %d | %s\n", e.LineNumber, e.LineText)
	fmt.Fprintln(out, "\033[31m│\033[0m")
	fmt.Fprintf(out, "\033[31m│\033[0m Details: %s\n", e.Message)
	if e.SourceErr != nil {
		fmt.Fprintf(out, "\033[31m│\033[0m Cause:   %v\n", e.SourceErr)
	}
	fmt.Fprintln(out, "\033[31m└─────────────────────────────────────────────────────\033[0m")

	code := e.ExitCode
	if code == 0 {
		code = 1
	}
	os.Exit(code)
}

type Language struct {
	Filename string
	defines  map[string]string
}
