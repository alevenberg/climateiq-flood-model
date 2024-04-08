# Batch job 

This is a script around the Cloud Batch API that will let us scale our runs for the CityCat flood model.

## Compiling the Example

This project uses `vcpkg` to install its dependencies. Clone `vcpkg` in your
`$HOME`:

```shell
git clone -C $HOME https://github.com/microsoft/vcpkg.git
```

Install the typical development tools, on Ubuntu you would use:

```shell
apt update && apt install -y build-essential cmake git ninja-build pkg-config g++ curl tar zip unzip
```

In this directory compile the dependencies and the code, this can take as long
as an hour, depending on the performance of your workstation:

```shell
cd climateiq-flood-model/batch
cmake -S . -B .build -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_TOOLCHAIN_FILE=$HOME/vcpkg/scripts/buildsystems/vcpkg.cmake
cmake --build .build
```

## Run the sample

Run the example, replace the `[PROJECT ID]` placeholder with the id of your
project:

```shell
.build/src/main [PROJECT ID] us-central1 test-container-run hello-world-container.json
```