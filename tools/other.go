package tools

import (
	"errors"
	"os"
	"path/filepath"
	"strings"
)

func Use(s any) any {
	return s
}

func Read(filename string) []string {
	file, _ := os.ReadFile(filename)
	lines := strings.Split(string(file), "\n")
	return lines
}

func FileExists(path string) (bool, error) {
	info, err := os.Stat(path)
	if err == nil {
		return !info.IsDir(), nil
	}
	if errors.Is(err, os.ErrNotExist) {
		return false, nil
	}
	return false, err
}

func AbsPath(relPath string) (string, error) {
	return filepath.Abs(relPath)
}
