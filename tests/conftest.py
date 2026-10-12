import pytest

from task_manager.demo import sample_data
from task_manager.storage import save_data


@pytest.fixture(autouse=True)
def isolated_storage(tmp_path, monkeypatch):
    monkeypatch.setenv("TASK_MANAGER_DATA_DIR", str(tmp_path))


@pytest.fixture
def sample_tasks():
    data = sample_data()
    save_data(data)
    return data["tasks"]
