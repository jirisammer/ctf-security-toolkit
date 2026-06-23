import pytest

from ctf_toolkit.core.settings import (
    DEFAULT_SETTINGS,
    get_setting,
    load_settings,
    reset_settings,
    save_settings,
    update_setting,
)


def test_load_settings_returns_defaults_when_file_missing(tmp_path):
    settings_file = tmp_path / "missing_settings.json"

    settings = load_settings(settings_file)

    assert settings == DEFAULT_SETTINGS


def test_save_and_load_settings(tmp_path):
    settings_file = tmp_path / "settings.json"

    settings = DEFAULT_SETTINGS.copy()
    settings["history_default_limit"] = 10

    save_settings(settings, settings_file)

    loaded_settings = load_settings(settings_file)

    assert loaded_settings["history_default_limit"] == 10


def test_get_setting(tmp_path):
    settings_file = tmp_path / "settings.json"

    settings = DEFAULT_SETTINGS.copy()
    settings["reports_directory"] = "my_reports"

    save_settings(settings, settings_file)

    result = get_setting("reports_directory", settings_file)

    assert result == "my_reports"


def test_update_integer_setting(tmp_path):
    settings_file = tmp_path / "settings.json"

    update_setting("history_default_limit", "30", settings_file)

    settings = load_settings(settings_file)

    assert settings["history_default_limit"] == 30


def test_update_string_setting(tmp_path):
    settings_file = tmp_path / "settings.json"

    update_setting("reports_directory", "custom_reports", settings_file)

    settings = load_settings(settings_file)

    assert settings["reports_directory"] == "custom_reports"


def test_reset_settings(tmp_path):
    settings_file = tmp_path / "settings.json"

    update_setting("history_default_limit", "99", settings_file)
    reset_settings(settings_file)

    settings = load_settings(settings_file)

    assert settings == DEFAULT_SETTINGS


def test_unknown_setting_raises_error(tmp_path):
    settings_file = tmp_path / "settings.json"

    with pytest.raises(ValueError):
        update_setting("unknown_setting", "123", settings_file)


def test_integer_setting_must_be_positive(tmp_path):
    settings_file = tmp_path / "settings.json"

    with pytest.raises(ValueError):
        update_setting("history_default_limit", "0", settings_file)


def test_integer_setting_must_be_integer(tmp_path):
    settings_file = tmp_path / "settings.json"

    with pytest.raises(ValueError):
        update_setting("history_default_limit", "abc", settings_file)


def test_string_setting_cannot_be_empty(tmp_path):
    settings_file = tmp_path / "settings.json"

    with pytest.raises(ValueError):
        update_setting("reports_directory", "", settings_file)