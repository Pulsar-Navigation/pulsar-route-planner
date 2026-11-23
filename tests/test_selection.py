from datetime import UTC, datetime

import pytest

ROTTERDAM = (51.95, 4.14)
TIME = datetime(2026, 12, 1, 12, 0, tzinfo=UTC)


@pytest.mark.skip(reason="select_four_pulsars is not implemented yet")
def test_select_four_pulsars_returns_four() -> None:
    from planner.selection import select_four_pulsars

    lat, lon = ROTTERDAM
    result = select_four_pulsars(lat, lon, TIME)

    assert len(result.pulsars) == 4
