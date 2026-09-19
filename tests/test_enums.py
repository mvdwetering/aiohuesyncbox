from aiohuesyncbox.models import ExecutionMode
from aiohuesyncbox.models.enums import OpenStrEnum


def test_unknown_enum_value_logs_and_returns_unknown_api_value(caplog):
    with caplog.at_level("WARNING", logger="aiohuesyncbox.models.enums"):
        mode = ExecutionMode("futureMode")

    assert mode is ExecutionMode.UNKNOWN_API_VALUE
    assert "Unknown ExecutionMode value received: 'futureMode'" in caplog.text


def test_all_open_string_enums_define_unknown_api_value():
    missing_unknown = [
        enum.__name__
        for enum in OpenStrEnum.__subclasses__()
        if "UNKNOWN_API_VALUE" not in enum.__members__
    ]

    assert not missing_unknown, (
        "OpenStrEnum subclasses must define UNKNOWN_API_VALUE: "
        + ", ".join(missing_unknown)
    )
