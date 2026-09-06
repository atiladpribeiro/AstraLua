#!/usr/bin/env bash
set -Eeuo pipefail
IFS=$'\n\t'

ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
BUILD_DIR="${ROOT_DIR}/build-linux"
JOBS="${JOBS:-$(nproc 2>/dev/null || echo 2)}"

log() { printf '\n[AstraLua] %s\n' "$*"; }
fail() { printf '\n[AstraLua] ERRO: %s\n' "$*" >&2; exit 1; }

command -v cmake >/dev/null 2>&1 || fail "CMake não encontrado. Instale cmake, g++ e as dependências do Luanti."
command -v c++ >/dev/null 2>&1 || fail "Compilador C++ não encontrado. Instale g++."

log "Limpando apenas a configuração desta compilação"
rm -rf -- "${BUILD_DIR}"
mkdir -p -- "${BUILD_DIR}"

log "Configurando AstraLua 5.17.0"
GENERATOR_ARGS=()
if command -v ninja >/dev/null 2>&1; then GENERATOR_ARGS=(-G Ninja); fi
cmake -S "${ROOT_DIR}" -B "${BUILD_DIR}" "${GENERATOR_ARGS[@]}" \
  -DCMAKE_BUILD_TYPE=Release \
  -DBUILD_CLIENT=ON \
  -DBUILD_SERVER=OFF \
  -DBUILD_UNITTESTS=ON \
  -DBUILD_BENCHMARKS=OFF \
  -DBUILD_DOCUMENTATION=OFF \
  -DRUN_IN_PLACE=TRUE \
  -DENABLE_LTO=OFF

log "Compilando com ${JOBS} núcleos"
cmake --build "${BUILD_DIR}" --parallel "${JOBS}"

BIN="${ROOT_DIR}/bin/astralua"
[[ -x "${BIN}" ]] || BIN="${ROOT_DIR}/bin/antilua"
[[ -x "${BIN}" ]] || BIN="${ROOT_DIR}/bin/luanti"
[[ -x "${BIN}" ]] || fail "A compilação terminou sem gerar um executável em bin/."

if [[ -x "${BUILD_DIR}/src/unittest/unittest" ]]; then
  log "Executando testes unitários"
  "${BUILD_DIR}/src/unittest/unittest"
fi

log "Compilação concluída com sucesso"
printf 'Executável: %s\n' "${BIN}"
printf 'Para iniciar: %q\n' "${BIN}"
