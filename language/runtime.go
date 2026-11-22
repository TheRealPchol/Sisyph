package language

import (
	"path/filepath"
	"strings"

	"gosyh/context"
	"gosyh/tools"
)

func (r *Language) ExecuteLine(line string) any {
	args_sp := strings.Split(line, " ")
	args_dot := strings.Split(args_sp[0], ".")
	tools.Use(args_dot)
	if args_sp[0] == "pass" {
		return nil
	}
	return nil
}

func stripComments(line string) string {
	return strings.Split(line, "//")[0]
}

func (r *Language) expandDefines(line string) string {
	for define, value := range r.defines {
		line = strings.ReplaceAll(line, define, value)
	}
	return line
}

func (r *Language) preprocessFile(filename string, lines []string, visited map[string]bool, lineOffset int) ([]string, map[string]int) {
	if visited[filename] {
		return nil, nil
	}
	visited[filename] = true

	absPath, _ := tools.AbsPath(filename)

	file := lines
	if file == nil {
		exists, err := tools.FileExists(filename)
		if err != nil {
			(&GoSyhException{
				"GoError",
				"Error checking file existence",
				filename,
				lineOffset,
				"",
				err,
				1,
			}).Raise()
		}
		if !exists {
			(&GoSyhException{
				"GoError",
				"File not found",
				filename,
				lineOffset,
				"",
				nil,
				1,
			}).Raise()
		}
		file = tools.Read(absPath)
	}

	result := make([]string, 0)
	included := make([]string, 0)
	labels := make(map[string]int)
	includedLabels := make(map[string]int)
	currentLine := lineOffset

	for _, fileLine := range file {
		currentLine++

		cleaned := stripComments(fileLine)

		if strings.TrimSpace(cleaned) == "" {
			continue
		}

		parts := strings.Fields(cleaned)
		if strings.HasPrefix(cleaned, "@") {
			labelName := parts[0]
			labels[labelName] = len(result)
			result = append(result, "")
			continue
		}
		if !strings.HasPrefix(cleaned, "#") {
			result = append(result, r.expandDefines(cleaned))
			continue
		}

		switch parts[0] {
		case "#define":
			if len(parts) >= 3 {
				name := parts[1]
				value := strings.Join(parts[2:], " ")
				r.defines[name] = value
			} else if len(parts) == 2 {
				r.defines[parts[1]] = ""
			}

		case "#include":
			if len(parts) < 2 {
				(&GoSyhException{
					"GoError",
					"Invalid #include directive",
					filename,
					currentLine,
					fileLine,
					nil,
					1,
				}).Raise()
			}

			incFile := strings.Trim(parts[1], "\"'")

			if !filepath.IsAbs(incFile) {
				incDir := filepath.Dir(absPath)
				incFile = filepath.Join(incDir, incFile)
			}

			var incLines []string
			var incLinesLabels map[string]int
			incLines, incLinesLabels = r.preprocessFile(incFile, nil, visited, currentLine)
			for k, v := range incLinesLabels {
				includedLabels[k] = v
			}
			included = append(included, incLines...)

		default:
			result = append(result, r.expandDefines(cleaned))
		}
	}

	for k, v := range includedLabels {
		labels[k] = len(result) + v
	}

	result = append(result, included...)

	return result, labels
}

func (r *Language) Preprocessor(lines []string, filename string) []string {
	r.defines = make(map[string]string)
	visited := make(map[string]bool)

	result, labels := r.preprocessFile(filename, lines, visited, 0)

	for k, v := range labels {
		context.Labels[k] = v
	}

	return result
}

func (l *Language) ExecuteLines(lines []string, filename string) {
	l.Filename = filename
	lines = l.Preprocessor(lines, filename)
	for _, line := range lines {
		l.ExecuteLine(line)
	}
}

func (l *Language) ExecuteFile(filename string) {
	fexists, err := tools.FileExists(filename)
	if err != nil {
		(&GoSyhException{
			"GoError",
			"Error checking file existence",
			filename,
			0,
			"",
			err,
			1,
		}).Raise()
	}
	if !fexists {
		(&GoSyhException{
			"FileNotFoundError",
			"File '" + filename + "' not found",
			filename,
			0,
			"",
			nil,
			5,
		}).Raise()
	}

	lines, err := tools.ReadFile(filename)
	if err != nil {
		(&GoSyhException{
			"ReadFileError",
			"Error in reading file '" + filename + "'",
			filename,
			0,
			"",
			err,
			6,
		}).Raise()
	}

	l.ExecuteLines(lines, filename)
}
