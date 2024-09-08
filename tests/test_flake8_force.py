from dataclasses import dataclass
import os
import re
import subprocess


@dataclass
class Result:
    row: int
    col: int
    code: str
    text: str


def _flake8(test_input, *, cython=False, force=False):
    args = ["flake8", "--isolated"]
    if cython:
        args += ["--ignore", "E999"]
    if force:
        args += ["--force-check"]
    args += [
        os.path.join(os.path.dirname(__file__), 'test_inputs', test_input)]
    proc = subprocess.run(
        args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        encoding='utf-8')
    assert (
        (proc.returncode == 0 and len(proc.stdout) == 0) or
        proc.returncode != 0 and len(proc.stdout) != 0)
    results = []
    for line in proc.stdout.splitlines():
        m = re.fullmatch(r"(.+?):(\d+):(\d+): (.+?) (.+?)", line)
        assert m is not None, f'unexpected output: {proc.stdout}'
        results.append(Result(
            int(m.group(2)), int(m.group(3)), m.group(4), m.group(5)))
    return results


def test_valid():
    assert _flake8("valid.py") == _flake8("valid.py", force=True) == []


def test_invalid_unused():
    assert (
        _flake8("invalid_unused.py") ==
        _flake8("invalid_unused.py", force=True) == [
            Result(2, 1, "F401", "'os' imported but unused"),
        ]
    )


def test_invalid_token():
    results = _flake8("invalid_token.py")
    assert len(results) == 1
    assert results[0].row == 1
    assert results[0].code == "E999"
    assert "SyntaxError" in results[0].text

    results_force = _flake8("invalid_token.py", force=True)
    assert len(results_force) == 2
    if results_force[0] == results[0]:
        # Python 3.11 or earlier
        token_error = results_force[1]
        assert token_error.row == 2
    else:
        # Python 3.12+
        assert results_force[1] == results[0]  # SyntaxError
        token_error = results_force[0]
        assert token_error.row == 1
    assert token_error.code == "E902"
    assert "TokenError" in token_error.text


def test_invalid_indent():
    results = _flake8("invalid_indent.py")
    assert len(results) == 1
    assert results[0].row == 4
    assert results[0].code == "E999"
    assert "IndentationError" in results[0].text

    results_force = _flake8("invalid_indent.py", force=True)
    assert len(results_force) == 2
    assert results_force[0] == results[0]
    assert results_force[1].row == 4
    assert results_force[1].code == "E113"
    assert "unexpected indentation" in results_force[1].text


def test_valid_cython():
    assert (
        _flake8("valid_cython.pyx", cython=True) ==
        _flake8("valid_cython.pyx", cython=True, force=True) == [])


def test_invalid_cython():
    assert _flake8("invalid_cython.pyx", cython=True) == []
    assert _flake8("invalid_cython.pyx", cython=True, force=True) == [
        Result(6, 1, "E302", "expected 2 blank lines, found 0"),
    ]
