package tools

import (
	"errors"

	"github.com/expr-lang/expr"
)

func Math_execute(code string) (float64, error) {
	program, err := expr.Compile(code, expr.AsFloat64())
	if err != nil {
		return 0.0, errors.New(err.Error())
	}

	output, err := expr.Run(program, nil)
	if err != nil {
		return 0.0, errors.New(err.Error())
	}

	result := output.(float64)
	return result, nil
}
