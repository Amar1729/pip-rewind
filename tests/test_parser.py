from pip_rewind import parser


def test_1():
    assert "pip" == parser.line_parser("pip")


def test_2():
    assert "pip" == parser.line_parser("  pip==5.0")


def test_3():
    assert "pip" == parser.line_parser("pip<=5.0")
    assert "pip" == parser.line_parser("pip<=5.0,>=6.0")
    assert "pip" == parser.line_parser("pip<=5.0,!=4.0")
    assert "pip" == parser.line_parser("pip>=5.0")
    assert "pip" == parser.line_parser("  pip<=5.0")
    assert "pip" == parser.line_parser("  pip<=5.0,>=6.0")
    assert "pip" == parser.line_parser("  pip<=5.0,!=4.0")
    assert "pip" == parser.line_parser("  pip>=5.0")
