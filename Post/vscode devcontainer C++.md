---
tags:
- memo
- vscode
- c++
date: 2022-06-18, 18:49:39
update: 2022-06-18, 20:29:06
title: vscode devcontainer C++
---
## TL;DR
Vscode의 devcontainer를 이용하여 C++ 개발 환경 구축한다. `.devcontainer` 폴더만 가지고 있으면 쉽게 개발 환경이 구축된다.
## 사전 조건
- Docker : https://www.docker.com/
- Vscode : https://code.visualstudio.com/
- Remote Development : https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack

## .devcontainer 생성
파일 구조는 다음과 같다. `.devcontainer` 파일을 만든후 하위에 `devcontainer.json`, `Dockerfile`, `reinstall-cmake.sh`을 생성한다.
```
├── .devcontainer
    ├── devcontainer.json
	├── Dockerfile
    └── reinstall-cmake.sh
```
### devcontainer.json
```json
// For format details, see https://aka.ms/devcontainer.json. For config options, see the README at:
// https://github.com/microsoft/vscode-dev-containers/tree/v0.238.0/containers/cpp
{
	"name": "C++",
	"build": {
		"dockerfile": "Dockerfile",
		// Update 'VARIANT' to pick an Debian / Ubuntu OS version: debian-11, debian-10, ubuntu-22.04, ubuntu-20.04, ubuntu-18.04
		// Use Debian 11, Ubuntu 18.04 or Ubuntu 22.04 on local arm64/Apple Silicon
		"args": { "VARIANT": "ubuntu-22.04" }
	},
	"runArgs": ["--cap-add=SYS_PTRACE", "--security-opt", "seccomp=unconfined"],

	// Configure tool-specific properties.
	"customizations": {
		// Configure properties specific to VS Code.
		"vscode": {
			// Add the IDs of extensions you want installed when the container is created.
			"extensions": [
				"ms-vscode.cpptools",
				"ms-vscode.cmake-tools"
			]
		}
	},

	// Use 'forwardPorts' to make a list of ports inside the container available locally.
	// "forwardPorts": [],

	// Use 'postCreateCommand' to run commands after the container is created.
	// "postCreateCommand": "gcc -v",

	// Comment out to connect as root instead. More info: https://aka.ms/vscode-remote/containers/non-root.
	"remoteUser": "vscode"
}
```
### Dockerfile
```dockerfile
# See here for image contents: https://github.com/microsoft/vscode-dev-containers/tree/v0.238.0/containers/cpp/.devcontainer/base.Dockerfile

# [Choice] Debian / Ubuntu version (use Debian 11, Ubuntu 18.04/22.04 on local arm64/Apple Silicon): debian-11, debian-10, ubuntu-22.04, ubuntu-20.04, ubuntu-18.04
ARG VARIANT="bullseye"
FROM mcr.microsoft.com/vscode/devcontainers/cpp:0-${VARIANT}

# [Optional] Install CMake version different from what base image has already installed. 
# CMake reinstall choices: none, 3.21.5, 3.22.2, or versions from https://cmake.org/download/
ARG REINSTALL_CMAKE_VERSION_FROM_SOURCE="none"

# Optionally install the cmake for vcpkg
COPY ./reinstall-cmake.sh /tmp/
RUN if [ "${REINSTALL_CMAKE_VERSION_FROM_SOURCE}" != "none" ]; then \
        chmod +x /tmp/reinstall-cmake.sh && /tmp/reinstall-cmake.sh ${REINSTALL_CMAKE_VERSION_FROM_SOURCE}; \
    fi \
    && rm -f /tmp/reinstall-cmake.sh

# [Optional] Uncomment this section to install additional vcpkg ports.
# RUN su vscode -c "${VCPKG_ROOT}/vcpkg install <your-port-name-here>"

# [Optional] Uncomment this section to install additional packages.
# RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
#     && apt-get -y install --no-install-recommends <your-package-list-here>
```
### reinstall-cmake.sh
```shell
#!/usr/bin/env bash
#-------------------------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See https://go.microsoft.com/fwlink/?linkid=2090316 for license information.
#-------------------------------------------------------------------------------------------------------------
#
set -e

CMAKE_VERSION=${1:-"none"}

if [ "${CMAKE_VERSION}" = "none" ]; then
    echo "No CMake version specified, skipping CMake reinstallation"
    exit 0
fi

# Cleanup temporary directory and associated files when exiting the script.
cleanup() {
    EXIT_CODE=$?
    set +e
    if [[ -n "${TMP_DIR}" ]]; then
        echo "Executing cleanup of tmp files"
        rm -Rf "${TMP_DIR}"
    fi
    exit $EXIT_CODE
}
trap cleanup EXIT


echo "Installing CMake..."
apt-get -y purge --auto-remove cmake
mkdir -p /opt/cmake

architecture=$(dpkg --print-architecture)
case "${architecture}" in
    arm64)
        ARCH=aarch64 ;;
    amd64)
        ARCH=x86_64 ;;
    *)
        echo "Unsupported architecture ${architecture}."
        exit 1
        ;;
esac

CMAKE_BINARY_NAME="cmake-${CMAKE_VERSION}-linux-${ARCH}.sh"
CMAKE_CHECKSUM_NAME="cmake-${CMAKE_VERSION}-SHA-256.txt"
TMP_DIR=$(mktemp -d -t cmake-XXXXXXXXXX)

echo "${TMP_DIR}"
cd "${TMP_DIR}"

curl -sSL "https://github.com/Kitware/CMake/releases/download/v${CMAKE_VERSION}/${CMAKE_BINARY_NAME}" -O
curl -sSL "https://github.com/Kitware/CMake/releases/download/v${CMAKE_VERSION}/${CMAKE_CHECKSUM_NAME}" -O

sha256sum -c --ignore-missing "${CMAKE_CHECKSUM_NAME}"
sh "${TMP_DIR}/${CMAKE_BINARY_NAME}" --prefix=/opt/cmake --skip-license

ln -s /opt/cmake/bin/cmake /usr/local/bin/cmake
```

## VSCode에서 컨테이너로 원격 연결
![[Pasted image 20220618194716.png]]
위와 같이 창이 뜨면 `Reopen in Container`를 누른다.

혹은 명령어 팔레트에서 `Remote-Containers: Open Folder in Containers...`를 실행한다.

![[Pasted image 20220618195027.png]]
C++를 개발할 수 있는 도커 컨테이너에 접속할 수 있다.

### CMake 설정하기
1. 명령어 팔레트에서 `Cmake: Configure`를 실행한다.
2. 컴파일러를 선택한다.(GCC 또는 Clang)
	![[Pasted image 20220618195732.png]]
3. 아래와 같은 창이 뜨면 `Create`를 선택한다. 
	![[Pasted image 20220618195209.png]]
4. 프로젝트명 입력한다.
	![[Pasted image 20220618195339.png]]
5. 라이브러리(Libray), 실행파일(Executable) 중 만들 것을 선택한다.
	![[Pasted image 20220618195454.png]]
### 빌드 및 디버깅
- `[F7] (F7)` : 빌드
- `[F5] (F5)` : 디버깅 시작
- `⌃ F5 (Ctrl + F5)` : 디버깅 없이 시작