# Partly from https://leimao.github.io/blog/Docker-Wine/
# Partly from https://github.com/OpenCLIM/citycat-dafni/blob/master/Dockerfile

FROM ubuntu:20.04

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
        software-properties-common \
        ca-certificates \
        language-pack-en \
        language-pack-zh-han* \
        locales \
        locales-all \
        wget 

RUN apt-get install -y --no-install-recommends \
    vim \ 
    zip

# Install Wine
RUN dpkg --add-architecture i386 && \
    mkdir -pm755 /etc/apt/keyrings && \
    wget -O /etc/apt/keyrings/winehq-archive.key https://dl.winehq.org/wine-builds/winehq.key && \
    wget -nc -P /etc/apt/sources.list.d/ https://dl.winehq.org/wine-builds/ubuntu/dists/$(lsb_release -sc)/winehq-$(lsb_release -sc).sources && \
    apt-get update -y && \
    apt-get install -y --install-recommends winehq-stable

# Set env variable defaults
ENV INPUT_MOUNT_DIRECTORY=/mnt/disks/share/citycat-input-test
ENV CONFIG_MOUNT_DIRECTORY=/mnt/disks/share/citycat-config-test
ENV OUTPUT_MOUNT_DIRECTORY=/mnt/disks/share/citycat-output-test
ENV STUDY_AREA=1
ENV CONFIG=1
ENV CITYCAT_CONFIG_FILE=1
ENV RAINFALL_DATA_FILE=11
ENV DRY_RUN=false

# Copy entrypoint script and run
WORKDIR /root
COPY --chmod=0755 execute.sh .

ENTRYPOINT ["bash", "/root/execute.sh"]
