"""Tests for the shared calculator engine (no GUI dependencies)."""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from apps.calc_engine import evaluate, sqrt


def test_basic_arithmetic():
    assert evaluate("2+3") == "5"
    assert evaluate("10-4") == "6"
    assert evaluate("6*7") == "42"
    assert evaluate("8/2") == "4"


def test_whole_float_becomes_int():
    assert evaluate("5/5") == "1"
    assert evaluate("2.5+0.5") == "3"


def test_modulo():
    assert evaluate("5%2") == "1"


def test_unicode_operators():
    assert evaluate("2×3") == "6"
    assert evaluate("6÷2") == "3"


def test_decimal_results_kept():
    assert evaluate("1/3") == "0.3333333333333333"


def test_empty_or_blank_resolves_to_none():
    assert evaluate("") is None
    assert evaluate("   ") is None
    assert evaluate(None) is None


def test_invalid_expression_resolves_to_none():
    assert evaluate("2+") is None
    assert evaluate("abc") is None
    assert evaluate("1/0") is None


def test_restricted_context_blocks_imports():
    for evil in ["__import__('os')", "open('x')", "().__class__"]:
        assert evaluate(evil) is None, evil


def test_sqrt():
    assert sqrt("9") == "3"
    assert sqrt("2+7") == "3"


def test_sqrt_negative_is_none():
    assert sqrt("-9") is None


def test_sqrt_invalid_is_none():
    assert sqrt("") is None
    assert sqrt("abc") is None
    assert sqrt("2+") is None


if __name__ == "__main__":
    for name, fn in sorted(list(globals().items())):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"PASS {name}")
    print("ALL CALC ENGINE TESTS PASSED")