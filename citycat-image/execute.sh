#!/bin/bash
echo "Starting execute.sh"

echo "CITYCAT_CONFIG_FILE=$CITYCAT_CONFIG_FILE"
echo "RAINFALL_DATA_FILE=$RAINFALL_DATA_FILE"
echo "STUDY_AREA=$STUDY_AREA"
echo "CONFIG=$CONFIG"
echo "INPUT_MOUNT_DIRECTORY=$INPUT_MOUNT_DIRECTORY"
echo "CONFIG_MOUNT_DIRECTORY=$CONFIG_MOUNT_DIRECTORY"
echo "OUTPUT_MOUNT_DIRECTORY=$OUTPUT_MOUNT_DIRECTORY"
echo "DRY_RUN=$DRY_RUN"

# Create a directory to run everything in
mkdir run
cd run

# Get the CityCat executable and study area information from the input bucket.
cp $INPUT_MOUNT_DIRECTORY/CityCat.exe . 
chmod -755 ./CityCat.exe 
cp $INPUT_MOUNT_DIRECTORY/$STUDY_AREA/Buildings.txt . 
cp $INPUT_MOUNT_DIRECTORY/$STUDY_AREA/Domain_DEM.asc . 
cp $INPUT_MOUNT_DIRECTORY/$STUDY_AREA/GreenAreas.txt . 
# Get the config files.
cp $CONFIG_MOUNT_DIRECTORY/config_$CONFIG/Rainfall_Data_$RAINFALL_DATA_FILE.txt . 
cp $CONFIG_MOUNT_DIRECTORY/config_$CONFIG/CityCat_Config_$CITYCAT_CONFIG_FILE.txt . 

# Print the log file for debugging
filename="CityCat_Log.txt"
touch $filename
tail -f $filename &

# Run CityCat
if [ "$DRY_RUN" == "true" ]; then
echo "Dry run enabled, not running CityCat"
else
    echo "Running citycat"
    wine64 CityCat.exe -c $CITYCAT_CONFIG_FILE -r $RAINFALL_DATA_FILE
fi 

# Zip the output and move the output to the write bucket
ZIP_FILENAME=R${RAINFALL_DATA_FILE}C${CITYCAT_CONFIG_FILE}_${STUDY_AREA}.zip
CITYCAT_OUTPUT_DIRECTORY=R${RAINFALL_DATA_FILE}C${CITYCAT_CONFIG_FILE}_SurfaceMaps
if [ -d "$CITYCAT_OUTPUT_DIRECTORY" ]; then
    zip -r $ZIP_FILENAME $CITYCAT_OUTPUT_DIRECTORY
    OUTPUT_DIRECTORY=$OUTPUT_MOUNT_DIRECTORY/$STUDY_AREA
    mkdir -p $OUTPUT_DIRECTORY
    cp $ZIP_FILENAME $OUTPUT_DIRECTORY
else
echo "Directory does not exist: $CITYCAT_OUTPUT_DIRECTORY" 
fi

# Cleanup
cd ..
rm -rf run
pkill tail

echo "Finished execute.sh"

