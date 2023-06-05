import pytest
import storage_json

file_path = "json_test_file.json"


def test_constructor():
    storage = storage_json.StorageJson(file_path)
    assert storage.file_path == file_path


pytest.main()
