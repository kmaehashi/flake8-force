import os
import re
import subprocess


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
        results.append(
            (int(m.group(2)), int(m.group(3)), m.group(4), m.group(5)))
    return results


def test_valid():
    assert _flake8("valid.py") == _flake8("valid.py", force=True) == []


def test_invalid_unused():
    assert (
        _flake8("invalid_unused.py") ==
        _flake8("invalid_unused.py", force=True) == [
            (2, 1, "F401", "'os' imported but unused"),
        ]
    )


def test_invalid_token():
    results = _flake8("invalid_token.py")
    assert len(results) == 1
    assert results[0][0] == 1
    assert results[0][2] == "E999"
    assert "SyntaxError" in results[0][3]

    results_force = _flake8("invalid_token.py", force=True)
    assert len(results_force) == 2
    assert results_force[0] == results[0]
    assert results_force[1][0] == 2
    assert results_force[1][2] == "E902"
    assert "TokenError" in results_force[1][3]


def test_invalid_indent():
    results = _flake8("invalid_indent.py")
    assert len(results) == 1
    assert results[0][0] == 4
    assert results[0][2] == "E999"
    assert "IndentationError" in results[0][3]

    results_force = _flake8("invalid_indent.py", force=True)
    assert len(results_force) == 2
    assert results_force[0] == results[0]
    assert results_force[1][0] == 4
    assert results_force[1][2] == "E113"
    assert "unexpected indentation" in results_force[1][3]


def test_valid_cython():
    assert (
        _flake8("valid_cython.pyx", cython=True) ==
        _flake8("valid_cython.pyx", cython=True, force=True) == [])


def test_invalid_cython():
    assert _flake8("invalid_cython.pyx", cython=True) == []
    assert _flake8("invalid_cython.pyx", cython=True, force=True) == [
        (6, 1, "E302", "expected 2 blank lines, found 0"),
    ]
