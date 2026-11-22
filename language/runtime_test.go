package language

import (
	"errors"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
	"testing"

	"gosyh/context"
)

func resetLabels() {
	context.Labels = make(map[string]int)
}

func TestExecuteLinesUsesProvidedLines(t *testing.T) {
	dir := t.TempDir()
	filename := filepath.Join(dir, "program.gosyh")
	if err := os.WriteFile(filename, []byte("@from_file\npass\n"), 0o644); err != nil {
		t.Fatal(err)
	}

	resetLabels()
	l := &Language{}
	l.ExecuteLines([]string{"@from_argument", "pass // ok"}, filename)

	if _, ok := context.Labels["@from_argument"]; !ok {
		t.Errorf("label from provided lines not registered: %v", context.Labels)
	}
	if _, ok := context.Labels["@from_file"]; ok {
		t.Errorf("ExecuteLines must not re-read the file: %v", context.Labels)
	}
	if l.Filename != filename {
		t.Errorf("Filename = %q, want %q", l.Filename, filename)
	}
}

func TestExecuteFile(t *testing.T) {
	dir := t.TempDir()
	filename := filepath.Join(dir, "main.gosyh")
	if err := os.WriteFile(filename, []byte("#include ./lib.gosyh\n@main\npass\n"), 0o644); err != nil {
		t.Fatal(err)
	}
	if err := os.WriteFile(filepath.Join(dir, "lib.gosyh"), []byte("@lib_label\npass\n"), 0o644); err != nil {
		t.Fatal(err)
	}

	resetLabels()
	l := &Language{}
	l.ExecuteFile(filename)

	for _, label := range []string{"@main", "@lib_label"} {
		if _, ok := context.Labels[label]; !ok {
			t.Errorf("label %s not registered: %v", label, context.Labels)
		}
	}
}

func TestExecuteFileNotFound(t *testing.T) {
	if os.Getenv("GOSYH_TEST_NOT_FOUND") == "1" {
		l := &Language{}
		l.ExecuteFile(filepath.Join(t.TempDir(), "missing.gosyh"))
		return
	}

	cmd := exec.Command(os.Args[0], "-test.run=^TestExecuteFileNotFound$")
	cmd.Env = append(os.Environ(), "GOSYH_TEST_NOT_FOUND=1")
	out, err := cmd.CombinedOutput()

	var exitErr *exec.ExitError
	if !errors.As(err, &exitErr) {
		t.Fatalf("expected non-zero exit, got err=%v, output=%s", err, out)
	}
	if exitErr.ExitCode() != 5 {
		t.Fatalf("exit code = %d, want 5; output=%s", exitErr.ExitCode(), out)
	}
	if !strings.Contains(string(out), "FileNotFoundError") {
		t.Fatalf("expected FileNotFoundError in output, got: %s", out)
	}
}
