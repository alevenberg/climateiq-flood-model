import io
import pathlib
import textwrap
from unittest import mock

from google.cloud import storage
import jinja2
import pytest

from config_uploader import main


def test_parse_rainfall_config():
    """Ensures we can parse rainfall config files."""
    mock_path = mock.Mock(spec=pathlib.Path)
    mock_path.open.return_value = io.StringIO(
        textwrap.dedent(
            """\
            * * *
            * * * rainfall ***
            * * *
            3
            * * *
            0	0.0
            300	0.1
            600	0.2
            """
        )
    )
    rainfall = main._parse_rainfall_config(mock_path)
    assert rainfall == [
        main._RainEvent(0, 0.0),
        main._RainEvent(300, 0.1),
        main._RainEvent(600, 0.2),
    ]


def test_parse_rainfall_config_invalid_entries_header():
    """Ensures we raise an error if the entries header is wrong."""
    mock_path = mock.Mock(spec=pathlib.Path)
    mock_path.open.return_value = io.StringIO(
        textwrap.dedent(
            """\
            * * *
            * * * rainfall ***
            * * *
            not a number
            * * *
            0	0.0
            300	0.1
            600	0.2
            """
        )
    )
    with pytest.raises(ValueError) as excinfo:
        main._parse_rainfall_config(mock_path)

    assert "Invalid number of entries header: not a number" in str(excinfo.value)


def test_parse_rainfall_config_bad_num_entries():
    """Ensures we raise an error if the entries header is wrong."""
    mock_path = mock.Mock(spec=pathlib.Path)
    mock_path.open.return_value = io.StringIO(
        textwrap.dedent(
            """\
            * * *
            * * * rainfall ***
            * * *
            5
            * * *
            0	0.0
            300	0.1
            600	0.2
            """
        )
    )
    with pytest.raises(ValueError) as excinfo:
        main._parse_rainfall_config(mock_path)

    assert "5 does not match actual number of rainfall entries 3" in str(excinfo.value)


def test_parse_rainfall_config_bad_entry():
    """Ensures we raise an error for bad rainfall entries."""
    mock_path = mock.Mock(spec=pathlib.Path)
    mock_path.open.return_value = io.StringIO(
        textwrap.dedent(
            """\
            * * *
            * * * rainfall ***
            * * *
            3
            * * *
            0	0.0
            300	0.1
            600
            """
        )
    )
    with pytest.raises(ValueError) as excinfo:
        main._parse_rainfall_config(mock_path)

    assert "rainfall configuration entry: 600" in str(excinfo.value)


def test_parse_rainfall_config_bad_time_interval():
    """Ensures we raise an error if entries are not all 5 minutes apart."""
    mock_path = mock.Mock(spec=pathlib.Path)
    mock_path.open.return_value = io.StringIO(
        textwrap.dedent(
            """\
            * * *
            * * * rainfall ***
            * * *
            4
            * * *
            0     0.0
            300   0.1
            600   0.2
            5000  0.3
            """
        )
    )
    with pytest.raises(ValueError) as excinfo:
        main._parse_rainfall_config(mock_path)

    assert "entries separated by non-five minute interval" in str(excinfo.value)


def test_write_batch_config():
    """Ensures we produce correct batch config files."""
    config_file = io.StringIO()
    main._write_batch_config(
        config_file,
        [
            main._ConfigMapping(1, 1),
            main._ConfigMapping(1, 2),
            main._ConfigMapping(2, 3),
        ],
    )
    assert config_file.getvalue() == "-c 1 -r 1\n-c 1 -r 2\n-c 2 -r 3\n"


def test_group_configs_by_duration():
    """Ensures we group rainfall configs with the same duration together."""
    # Create a mock dir with three config files.
    mock_dir = mock.Mock(spec=pathlib.Path)
    mock_rain_path_1 = mock.Mock(spec=pathlib.Path)
    mock_rain_path_2 = mock.Mock(spec=pathlib.Path)
    mock_rain_path_3 = mock.Mock(spec=pathlib.Path)

    # These two are both 600 seconds long.
    mock_rain_path_1.open.return_value = io.StringIO("3\n0 0.0\n300 0.1\n600 0.2\n")
    mock_rain_path_2.open.return_value = io.StringIO("3\n0 0.0\n300 0.1\n600 0.2\n")
    # This one is 300 seconds long.
    mock_rain_path_3.open.return_value = io.StringIO("2\n0 0.0\n300 0.1\n")

    mock_dir.rglob.return_value = [
        mock_rain_path_1,
        mock_rain_path_2,
        mock_rain_path_3,
    ]

    configs_by_duration = main._group_configs_by_duration(mock_dir)
    assert configs_by_duration == {
        600: [mock_rain_path_1, mock_rain_path_2],
        300: [mock_rain_path_3],
    }


def test_upload_city_cat_configs():
    jinja_env = jinja2.Environment(
        loader=jinja2.PackageLoader("config_uploader"),
        autoescape=jinja2.select_autoescape(),
    )
    template = jinja_env.get_template("CityCat_Config.txt.jinja")

    mock_bucket = mock.Mock(spec=storage.Bucket)
    mock_configs_by_duration = {
        300: [pathlib.Path("path1"), pathlib.Path("path2")],
        600: [pathlib.Path("path3")],
    }

    uploaded_configs = main._upload_city_cat_configs(
        mock_bucket, "config_name", mock_configs_by_duration, template
    )

    mock_bucket.assert_has_calls(
        [
            # Upload CityCAT configuration file for a 300 duration storm.
            mock.call.blob("config_name/CityCat_Config_1.txt"),
            mock.call.blob().upload_from_string(
                template.render(simulation_run_time=300)
            ),
            # Upload the two 300 duration rainfall configs.
            mock.call.blob("config_name/Rainfall_Data_1.txt"),
            mock.call.blob().upload_from_filename(pathlib.Path("path1")),
            mock.call.blob("config_name/Rainfall_Data_2.txt"),
            mock.call.blob().upload_from_filename(pathlib.Path("path2")),
            # Upload CityCAT configuration file for a 600 duration storm.
            mock.call.blob("config_name/CityCat_Config_2.txt"),
            mock.call.blob().upload_from_string(
                template.render(simulation_run_time=600)
            ),
            # Upload the one 600 duration rainfall configs.
            mock.call.blob("config_name/Rainfall_Data_3.txt"),
            mock.call.blob().upload_from_filename(pathlib.Path("path3")),
        ]
    )

    assert uploaded_configs == [
        main._ConfigMapping(city_cat_config=1, rainfall_config=1),
        main._ConfigMapping(city_cat_config=1, rainfall_config=2),
        main._ConfigMapping(city_cat_config=2, rainfall_config=3),
    ]
