# Configuration Uploader

This script helps manage rainfall configuration files describing the
scenarios on which we want to run CityCAT. It uploads configuration
files to Google Cloud Storage (GCS) and creates a batch configuration
file for scheduling CityCAT runs against the uploaded files.

Given a directory full of rainfall files, the script uploads each file
to GCS and creates an associated CityCAT configuration file for the
rainfall configuration. The CityCAT configuration files will be
identical except for their SimulationRunTime setting, which will match
the duration of its associated rainfall configuration file.  Note that
the uploaded rainfall configuration files will have different names in
GCS. They will have names in GCS with the form 'Rainfall_Data_X.txt'
where X is some number.

The resulting batch configuration file will map each rainfall
configuration file to the CityCAT configuration file with the correct
simulation run time.

## Installation

```
pip install -r requirements.txt
pip install -e .
```

## To run
You can run the script with
```
python config_uploader/main.py
  --rainfall-directory path/to/rainfall/configuation/files \
  --configuration-name unique-name-for-this-group-of-configurations \
  --batch-configuration-path path/to/resulting/batch/config/file
```
or equivalently, run the executable installed by `pip install -e .`
```
upload_citycat_config
  --rainfall-directory path/to/rainfall/configuation/files \
  --configuration-name unique-name-for-this-group-of-configurations \
  --batch-configuration-path path/to/resulting/batch/config/file
```

See
```
upload_citycat_config --help
```
for more details.

## Example

```
mkdir out
upload_citycat_config \
  --rainfall-directory data/test_config \
  --configuration-name test_config \
  --batch-configuration-path out/test_config.txt
```

Should produce

```
-c 1 -r 1
-c 1 -r 2
```