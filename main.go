package main

import (
	"fmt"
	"gosyh/context"
	"gosyh/language"
	"gosyh/tools"
	"strings"
)

func main() {
	fmt.Println("Hello, Go Sisyph!")
	fmt.Println("From bare metal to linear algebra.")
	lang := language.Language{}
	tools.Use(lang)
	file := tools.Read("./tests/test.gosyh")
	result := lang.Preprocessor(file, "./tests/test.gosyh")
	fmt.Println(strings.Join(result, "\n"))
	fmt.Println(context.Labels)
	fmt.Println(context.Included)
}
