from justify import main
from unittest.mock import patch
import pytest
import sys

def test_main_valid_from_file(capsys):
    expected = """This  is  a   sample
text      but      a
complicated  problem
to be solved, so  we
are adding more text
to   see   that   it
actually      works.
"""
    testargs = ["justify.py", "20", "file", "file"]

    with patch.object(sys, 'argv', testargs):
        with pytest.raises(SystemExit) as e:
            main()
        actual, _ = capsys.readouterr()

        assert e.value.code == 0
        assert expected == "{}".format(actual)

def test_main_valid_from_stdin(capsys):
    expected = """hi   it
is vlad
"""
    testargs = ["justify.py", "7", "stdin", "hi it is vlad"]

    with patch.object(sys, 'argv', testargs):
        with pytest.raises(SystemExit) as e:
            main()
        actual, _ = capsys.readouterr()

        assert e.value.code == 0
        assert expected == "{}".format(actual)

def test_main_valid_newlines(capsys):
    expected = """hi   it
is vlad
"""
    testargs = ["justify.py", "7", "stdin", "hi\nit\nis\nvlad"]

    with patch.object(sys, 'argv', testargs):
        with pytest.raises(SystemExit) as e:
            main()
        actual, _ = capsys.readouterr()

        assert e.value.code == 0
        assert expected == "{}".format(actual)

def test_main_invalid_insufficient_args():
    testargs = ["justify.py"]

    with patch.object(sys, 'argv', testargs):
        with pytest.raises(SystemExit) as e:
            main()

        assert e.value.code == 1

def test_main_invalid_negative_width():
    testargs = ["justify.py", "-1", "stdin", "text"]

    with patch.object(sys, 'argv', testargs):
        with pytest.raises(SystemExit) as e:
            main()

        assert e.value.code == 2

def test_main_invalid_nontext_width():
    testargs = ["justify.py", "blabla", "stdin", "text"]

    with patch.object(sys, 'argv', testargs):
        with pytest.raises(SystemExit) as e:
            main()

        assert e.value.code == 2

def test_main_invalid_input_param():
    testargs = ["justify.py", "5", "somestuff", "text"]

    with patch.object(sys, 'argv', testargs):
        with pytest.raises(SystemExit) as e:
            main()

        assert e.value.code == 3

def test_main_invalid_input_nonexistentpath():
    testargs = ["justify.py", "5", "file", "text"]

    with patch.object(sys, 'argv', testargs):
        with pytest.raises(SystemExit) as e:
            main()

        assert e.value.code == 4

def test_main_invalid_empty_input():
    testargs = ["justify.py", "5", "stdin", ""]

    with patch.object(sys, 'argv', testargs):
        with pytest.raises(SystemExit) as e:
            main()

        assert e.value.code == 5

def test_main_invalid_unadjustfiable_input():
    testargs = ["justify.py", "5", "stdin", "toolongforme"]

    with patch.object(sys, 'argv', testargs):
        with pytest.raises(SystemExit) as e:
            main()

        assert e.value.code == 6