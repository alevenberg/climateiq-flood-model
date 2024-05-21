import argparse
import collections
import dataclasses
import itertools
import pathlib
from typing import List, Mapping, Sequence

import jinja2
from google.cloud import storage

_CITY_CAT_CONFIG_BUCKET = "climateiq-flood-simulation-config"


@dataclasses.dataclass(slots=True)
class _RainEvent:
    """The amount of rainfall occurring at a given time step."""

    timestep: int
    rainfall: float

    def __str__(self):
        return f"{self.timestep} {self.rainfall}"


@dataclasses.dataclass(slots=True)
class _ConfigMapping:
    """A CityCAT & rainfall config ID pair."""

    city_cat_config: int
    rainfall_config: int


def main() -> None:
    args = _parse_args()

    gcs_client = storage.Client()
    bucket = gcs_client.bucket(args.configuration_bucket)

    configs_by_duration = _group_configs_by_duration(
        pathlib.Path(args.rainfall_directory)
    )

    jinja_env = jinja2.Environment(
        loader=jinja2.PackageLoader("config_uploader"),
        autoescape=jinja2.select_autoescape(),
    )
    template = jinja_env.get_template("CityCat_Config.txt.jinja")

    uploaded_configs = _upload_city_cat_configs(
        bucket, args.configuration_name, configs_by_duration, template
    )
    with open(args.batch_configuration_path, "wt") as batch_config:
        _write_batch_config(batch_config, uploaded_configs)


def _group_configs_by_duration(
    dir_name: pathlib.Path,
) -> Mapping[int, Sequence[pathlib.Path]]:
    """Groups each rain config in a given directory by their duration."""
    configs_by_duration = collections.defaultdict(list)
    for config_path in dir_name.rglob("Rainfall_Data_*.txt"):
        config = _parse_rainfall_config(config_path)
        duration = max(event.timestep for event in config)
        configs_by_duration[duration].append(config_path)
    return configs_by_duration


def _upload_city_cat_configs(
    bucket, config_name, configs_by_duration, template
) -> Sequence[_ConfigMapping]:
    """Uploads rain and creates accompanying CityCAT configs to GCS."""
    configs: List[_ConfigMapping] = []
    rainfall_config_i = 1
    for city_cat_config_i, (duration, rainfall_configs) in enumerate(
        configs_by_duration.items(), start=1
    ):
        config_file = template.render(simulation_run_time=duration)
        bucket.blob(
            f"{config_name}/CityCat_Config_{city_cat_config_i}.txt"
        ).upload_from_string(config_file)

        for path in rainfall_configs:
            bucket.blob(
                f"{config_name}/Rainfall_Data_{rainfall_config_i}.txt"
            ).upload_from_filename(path)
            configs.append(_ConfigMapping(city_cat_config_i, rainfall_config_i))
            rainfall_config_i += 1

    return configs


def _parse_rainfall_config(path: pathlib.Path) -> Sequence[_RainEvent]:
    """Parses a CityCAT rain config file."""
    with path.open("rt") as fd:
        lines = iter(fd)

        while True:
            line = next(lines)
            if line.startswith("*"):
                continue
            try:
                num_entries = int(line)
            except ValueError:
                raise ValueError(
                    f"Unable to parse file {path}. "
                    f"Invalid number of entries header: {line}"
                )
            break

        entries = []
        for line in lines:
            if line.startswith("*"):
                continue
            try:
                timestep_part, rainfall_part = line.split()
                timestep = int(timestep_part)
                rainfall = float(rainfall_part)
            except ValueError:
                raise ValueError(
                    f"Unable to parse file {path}. "
                    f"Invalid rainfall configuration entry: {line}"
                )
            entries.append(_RainEvent(timestep, rainfall))

    if num_entries != len(entries):
        raise ValueError(
            f"Number of rainfall entries found in header: {num_entries} does not "
            f"match actual number of rainfall entries {len(entries)}"
        )
    for prev_entry, next_entry in itertools.pairwise(entries):
        if next_entry.timestep - prev_entry.timestep != 300:
            raise ValueError(
                "Rainfall entries separated by non-five minute interval: "
                f"{prev_entry}, {next_entry}. Timesteps must consistently be five "
                "minutes apart to support model training."
            )

    return entries


def _write_batch_config(batch_config_file, uploaded_configs) -> None:
    """Writes a batch config file given a mapping of uploaded rain & CityCAT configs."""
    for entry in uploaded_configs:
        batch_config_file.writelines(
            f"-c {entry.city_cat_config} -r {entry.rainfall_config}\n"
        )


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Uploads configuration files to Google Cloud Storage (GCS) and creates a "
            "batch configuration file for scheduling CityCAT runs against the uploaded "
            "files. "
            "Given a directory full of rainfall files, uploads each file to GCS and "
            "creates an associated CityCAT configuration file for the rainfall "
            "configuration. "
            "The resulting batch configuration file will map each rainfall "
            "configuration file to the CityCAT configuration file with the correct "
            "simulation run time."
        )
    )
    parser.add_argument(
        "--rainfall-directory",
        help=(
            "Path to a directory containing rainfall configuration files. The "
            "directory will be recursively searched for all rainfall configuration "
            "text files inside it and its subdirectories. The rainfall configuration "
            "files are expected to be named like Rainfall_Data_X.txt where 'X' can be "
            "anything."
        ),
        required=True,
    )
    parser.add_argument(
        "--configuration-name",
        help=(
            "Top-level name to associate with the configurations. The files will be "
            "uploaded to Google Cloud Storage inside a directory with this name."
        ),
        required=True,
    )
    parser.add_argument(
        "--batch-configuration-path",
        help=("Local file path to write the resulting batch configuration file to."),
        required=True,
    )
    parser.add_argument(
        "--configuration-bucket",
        help=(
            "Name of the Google Cloud Storage bucket to upload configuration files to."
        ),
        default="climateiq-flood-simulation-config",
    )

    return parser.parse_args()


if __name__ == "__main__":
    main()
