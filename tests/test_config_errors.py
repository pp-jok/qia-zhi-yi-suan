from destiny_personality.config_errors import ConfigError


def test_config_error_exposes_machine_readable_context() -> None:
    error = ConfigError(
        code="CONFIG_VALUE_ERROR",
        message="expected tropical",
        file="astrology_methodology_v1.yaml",
        field="core.zodiac",
    )

    assert error.code == "CONFIG_VALUE_ERROR"
    assert error.file == "astrology_methodology_v1.yaml"
    assert error.field == "core.zodiac"
    assert str(error) == (
        "CONFIG_VALUE_ERROR | astrology_methodology_v1.yaml | "
        "core.zodiac: expected tropical"
    )
