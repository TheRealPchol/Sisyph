#!/usr/bin/bash

ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT" || exit 1

VERSION="1.0"
GOSYH_VERSION=$(cat ./data/version)
BUILDS_DIR=./builds/

COLOR_RED="\033[31m"
COLOR_GREEN="\033[32m"
COLOR_G="\033[96m"
COLOR_RESET="\033[0m"

info() { echo -e "$COLOR_G[INFO]$COLOR_RESET $*"; }
ok()   { echo -e "$COLOR_GREEN[OK]$COLOR_RESET $*"; }
err()  { echo -e "$COLOR_RED[ERROR]$COLOR_RESET $*"; }

build() {
    info "Start building into '$BUILDS_DIR$GOSYH_VERSION/gosyh'"
    mkdir -p "$BUILDS_DIR$GOSYH_VERSION/"
    rm -f "$BUILDS_DIR$GOSYH_VERSION"/* 2> /dev/null
    go build -o "$BUILDS_DIR$GOSYH_VERSION/gosyh" .
    ret=$?
    if [ $ret -eq 0 ]; then
        ok "Build completed successfully"
        exit 0
    else
        err "Build exited with error. Code: $ret"
        exit $ret
    fi

    info "Build was ended"
    exit 0
}

run(){
    go run .
    exit $?
}

version(){
    echo "GoSYH tools version: $VERSION"
    echo "GoSYH version: $GOSYH_VERSION"
    echo
}

case "$1" in
    build|run|version)
        "$1" "$2" "$3" "$4"
        ;;
    "")
        version
        echo "usage: $0 {run|build|version}"
        exit 1
        ;;
    *)
        version
        err "unknown command: $1"
        echo "usage: $0 {run|build|version}"
        exit 1
        ;;
esac
