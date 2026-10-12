from datetime import date, datetime, timedelta, timezone

from task_manager.demo import sample_data
from task_manager.productivity import format_stats, weekly_counts


TODAY = date(2026, 10, 12)
NOW = datetime(2026, 10, 12, 12).astimezone()


def test_weekly_chart_has_real_completion_counts():
    tasks = sample_data(NOW)["tasks"]
    week = weekly_counts(tasks, TODAY)
    assert [day for day, _ in week] == [TODAY - timedelta(days=offset) for offset in range(6, -1, -1)]
    assert [count for _, count in week] == [1, 3, 2, 4, 1, 3, 4]
    output = format_stats(tasks, TODAY)
    assert "Total: 26\nCompleted: 18\nPending: 8" in output
    assert "69%" in output
    assert "18 completed in the last 7 days" in output


def test_chart_ignores_unknown_old_future_and_pending_dates():
    tasks = [{"status": status, "completed_at": timestamp} for status, timestamp in (
        ("completed", None), ("completed", "broken"), ("completed", 4),
        ("completed", (NOW - timedelta(days=7)).isoformat()),
        ("completed", (NOW + timedelta(days=1)).isoformat()),
        ("pending", NOW.isoformat()), ("completed", NOW.astimezone(timezone.utc).isoformat()),
    )]
    assert [count for _, count in weekly_counts(tasks, TODAY)] == [0, 0, 0, 0, 0, 0, 1]


def test_empty_stats_and_legacy_tasks():
    assert "0%" in format_stats([], TODAY)
    assert "0 completed in the last 7 days" in format_stats([], TODAY)
    legacy = [{"status": "completed", "created_at": "now"}]
    assert "1 older completed task(s) without a date" in format_stats(legacy, TODAY)
