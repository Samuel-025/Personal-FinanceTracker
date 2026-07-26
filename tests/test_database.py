import pytest
from database import normalize_date

def test_normalize_date_valid():
    assert normalize_date("25-12-2025") == "25-12-2025"
    assert normalize_date("2025-12-25") == "25-12-2025"
    assert normalize_date("12/25/2025") == "25-12-2025"
    assert normalize_date("01-01-2026") == "01-01-2026"

def test_normalize_date_invalid():
    assert normalize_date("invalid-date") is None
    assert normalize_date("2025/13/45") is None
    assert normalize_date("") is None
    assert normalize_date(12345) is None
