"""Tests for the shared ATM account engine (no GUI dependencies)."""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from apps.atm_core import AtmAccount


def test_initial_state():
    acct = AtmAccount()
    assert acct.verify_pin("1234")
    assert acct.balance == 2500.0
    assert acct.transactions == []


def test_verify_pin_rejects_wrong_pin():
    acct = AtmAccount(pin="9999")
    assert not acct.verify_pin("1234")
    assert acct.verify_pin("9999")


def test_deposit():
    acct = AtmAccount()
    ok, msg = acct.deposit(500)
    assert ok
    assert acct.balance == 3000.0
    assert "Deposit: +$500.00" in acct.transactions[-1]
    assert "Deposited $500.00" in msg


def test_deposit_rejects_non_positive():
    acct = AtmAccount()
    ok, _ = acct.deposit(0)
    assert not ok
    ok, _ = acct.deposit(-10)
    assert not ok
    ok, _ = acct.deposit("abc")
    assert not ok
    assert acct.balance == 2500.0


def test_withdraw():
    acct = AtmAccount()
    ok, msg = acct.withdraw(1000)
    assert ok
    assert acct.balance == 1500.0
    assert "Withdrawal: -$1,000.00" in acct.transactions[-1]


def test_withdraw_rejects_overdraft_and_invalid():
    acct = AtmAccount()
    ok, _ = acct.withdraw(9999)
    assert not ok
    ok, _ = acct.withdraw(0)
    assert not ok
    ok, _ = acct.withdraw(-5)
    assert not ok
    ok, _ = acct.withdraw("x")
    assert not ok
    assert acct.balance == 2500.0


def test_withdraw_exact_balance_allowed():
    acct = AtmAccount(balance=100)
    ok, _ = acct.withdraw(100)
    assert ok
    assert acct.balance == 0.0


def test_change_pin_format():
    acct = AtmAccount()
    ok, _ = acct.change_pin("4321")
    assert ok
    assert acct.verify_pin("4321")
    assert not acct.verify_pin("1234")


def test_change_pin_rejects_bad_format():
    acct = AtmAccount()
    for bad in ["123", "12ab", "", "12345"]:
        ok, _ = acct.change_pin(bad)
        assert not ok, bad
    assert acct.verify_pin("1234")


def test_transaction_history_accumulates():
    acct = AtmAccount()
    acct.deposit(100)
    acct.withdraw(50)
    assert len(acct.transactions) == 2


if __name__ == "__main__":
    for name, fn in sorted(list(globals().items())):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"PASS {name}")
    print("ALL ATM CORE TESTS PASSED")