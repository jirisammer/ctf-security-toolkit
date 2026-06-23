import json
from copy import deepcopy
from pathlib import Path
from typing import Any


SETTINGS_FILE = Path("settings.json")


DEFAULT_SETTINGS: dict[str, Any] = {
    "history_default_limit": 20,
    "report_default_limit": 50,
    "reports_directory": "reports",
    "http_timeout_seconds": 10,
    "http_response_preview_limit": 1000,
}


def _get_settings_path(settings_file: str | Path | None = None) -> Path:
    if settings_file is None:
        return SETTINGS_FILE

    return Path(settings_file)


def _validate_setting_key(key: str) -> None:
    if not isinstance(key, str):
        raise TypeError("Setting key must be a string.")

    if key not in DEFAULT_SETTINGS:
        raise ValueError(f"Unknown setting: {key}")


def _validate_setting_value(key: str, value: Any) -> Any:
    _validate_setting_key(key)

    default_value = DEFAULT_SETTINGS[key]

    if isinstance(default_value, int):
        if not isinstance(value, int):
            raise TypeError(f"Setting '{key}' must be an integer.")

        if value <= 0:
            raise ValueError(f"Setting '{key}' must be greater than zero.")

        return value

    if isinstance(default_value, str):
        if not isinstance(value, str):
            raise TypeError(f"Setting '{key}' must be a string.")

        cleaned_value = value.strip()

        if cleaned_value == "":
            raise ValueError(f"Setting '{key}' cannot be empty.")

        return cleaned_value

    return value


def load_settings(settings_file: str | Path | None = None) -> dict[str, Any]:
    """
    Loads settings from settings.json.

    If the file does not exist, default settings are returned.
    """
    path = _get_settings_path(settings_file)

    if not path.exists():
        return deepcopy(DEFAULT_SETTINGS)

    try:
        data = json.loads(path.read_text(encoding="utf-8"))

    except json.JSONDecodeError:
        raise ValueError("Settings file contains invalid JSON.")

    if not isinstance(data, dict):
        raise ValueError("Settings file must contain a JSON object.")

    settings = deepcopy(DEFAULT_SETTINGS)

    for key, value in data.items():
        if key in DEFAULT_SETTINGS:
            settings[key] = _validate_setting_value(key, value)

    return settings


def save_settings(
    settings: dict[str, Any],
    settings_file: str | Path | None = None,
) -> None:
    """
    Saves settings to settings.json.
    """
    if not isinstance(settings, dict):
        raise TypeError("Settings must be a dictionary.")

    validated_settings = {}

    for key in DEFAULT_SETTINGS:
        value = settings.get(key, DEFAULT_SETTINGS[key])
        validated_settings[key] = _validate_setting_value(key, value)

    path = _get_settings_path(settings_file)
    path.write_text(
        json.dumps(validated_settings, indent=4, ensure_ascii=False),
        encoding="utf-8",
    )


def get_setting(
    key: str,
    settings_file: str | Path | None = None,
) -> Any:
    """
    Returns one setting value.
    """
    _validate_setting_key(key)

    settings = load_settings(settings_file=settings_file)

    return settings[key]


def update_setting(
    key: str,
    value: str,
    settings_file: str | Path | None = None,
) -> dict[str, Any]:
    """
    Updates one setting.

    Value is received as string from CLI and converted based on default type.
    """
    _validate_setting_key(key)

    if not isinstance(value, str):
        raise TypeError("Setting value must be a string.")

    default_value = DEFAULT_SETTINGS[key]

    if isinstance(default_value, int):
        try:
            parsed_value = int(value)

        except ValueError:
            raise ValueError(f"Setting '{key}' must be a valid integer.")

    elif isinstance(default_value, str):
        parsed_value = value.strip()

    else:
        parsed_value = value

    parsed_value = _validate_setting_value(key, parsed_value)

    settings = load_settings(settings_file=settings_file)
    settings[key] = parsed_value

    save_settings(settings, settings_file=settings_file)

    return settings


def reset_settings(settings_file: str | Path | None = None) -> dict[str, Any]:
    """
    Resets settings to default values.
    """
    settings = deepcopy(DEFAULT_SETTINGS)
    save_settings(settings, settings_file=settings_file)

    return settings