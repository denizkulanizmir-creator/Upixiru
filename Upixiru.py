import sys

class UpixiruFatalError(Exception):
    pass

class UpixiruInterpreter:
    def __init__(self):
        self.variables = {"variablename": "Hi"}

    def execute_print(self, cmd: str, line_no: int):
        prefix = "{//'']]]]]]]]\""
        if not cmd.startswith(prefix) or not cmd.endswith("}"):
            raise UpixiruFatalError(f"[Line {line_no}] UPX-PRINT-TORTURE: Invalid print brackets!")

        body = cmd[len(prefix):-1]
        if '"theletter(' not in body or ")-is-is" not in body or "?ALL/but not theletter(" not in body or ")/is-is" not in body:
            raise UpixiruFatalError(f"[Line {line_no}] UPX-PRINT-TORTURE: Missing print keywords!")

        text, rest = body.split('"theletter(', 1)
        group1_raw, rest = rest.split(")-is-is", 1)
        case1, rest = rest.split("?ALL/but not theletter(", 1)
        group2_raw, case2 = rest.split(")/is-is", 1)

        group1 = [c.strip().lower() for c in group1_raw.split(",") if c.strip()]
        group2 = [c.strip().lower() for c in group2_raw.split(",") if c.strip()]

        for ch in group1 + group2:
            if ch not in text.lower():
                raise UpixiruFatalError(f"[Line {line_no}] UPX-LOGIC-PANIC: Letter '{ch}' not in '{text}'!")

        if set(group1) & set(group2):
            raise UpixiruFatalError(f"[Line {line_no}] UPX-PARADOX: Letter in both groups!")

        result = []
        for ch in text:
            low = ch.lower()
            if low in group1:
                result.append(ch.upper() if case1 == "WITHBIGLETTERS" else ch.lower())
            elif low in group2:
                result.append(ch.upper() if case2 == "WITHBIGLETTERS" else ch.lower())
            else:
                raise UpixiruFatalError(f"[Line {line_no}] UPX-UNDECLARED-LETTER: Letter '{ch}' missing!")
        print("".join(result))

    def run(self, code: str):
        lines = [line.strip() for line in code.strip().splitlines() if line.strip()]
        sep = "}''elsee,do:\"\"\"\"\""

        for line_no, line in enumerate(lines, start=1):
            if line.startswith("{//'']]++"):
                if sep not in line:
                    raise UpixiruFatalError(f"[Line {line_no}] UPX-NO-MERCY: Standalone IF is forbidden!")

                left, else_cmd = line.split(sep, 1)
                var_part, rest = left[len("{//'']]++"):].split("++?\"", 1)
                expected_val, if_cmd = rest.split("\",do:\"\"\"\"\"", 1)

                if self.variables.get(var_part) == expected_val:
                    self.execute_print(if_cmd, line_no)
                else:
                    self.execute_print(else_cmd, line_no)
            elif line.startswith("{//'']]]]]]]]"):
                self.execute_print(line, line_no)
            else:
                raise UpixiruFatalError(f"[Line {line_no}] UPX-UNKNOWN-CURSE: Unrecognized command!")

if __name__ == "__main__":
    filename = sys.argv.pop(1)
    with open(filename, "r", encoding="utf-8") as f:
        UpixiruInterpreter().run(f.read())
