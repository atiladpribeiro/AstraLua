#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Monta um pacote Linux com dependências locais sem acessar dados pessoais."""

import argparse
import hashlib
import os
from pathlib import Path
import re
import shutil
import subprocess
import tarfile


# A libc e os drivers devem ser fornecidos pelo sistema do jogador.
SYSTEM_LIBS = re.compile(
    r"^(?:ld-linux.*|lib(?:c|m|pthread|dl|rt|resolv|util|anl)\.so(?:\..*)?"
    r"|lib(?:GL|GLX|GLdispatch|OpenGL|EGL|GLESv[12]|gbm|drm.*|nvidia.*|udev)\.so.*)$"
)


def dependencies(binary):
    result = subprocess.run(["ldd", str(binary)], text=True, capture_output=True, check=True)
    if "not found" in result.stdout:
        raise RuntimeError("Há bibliotecas ausentes:\n" + result.stdout)
    paths = []
    for line in result.stdout.splitlines():
        match = re.search(r"=> (/\S+)", line)
        if match:
            paths.append(Path(match.group(1)))
    return paths


def package(source, destination):
    source = source.resolve()
    destination = destination.resolve()
    binary = source / "bin/astralua"
    if not binary.is_file():
        raise RuntimeError("Compile primeiro o executável bin/astralua.")
    if destination.exists():
        raise RuntimeError("A pasta de destino já existe; nada foi sobrescrito.")
    if source == destination or source.is_relative_to(destination):
        raise RuntimeError("Destino inválido para o pacote.")

    destination.mkdir(parents=True)
    (destination / "bin").mkdir()
    (destination / "lib").mkdir()
    shutil.copy2(binary, destination / "bin/astralua")
    # Lista explícita: nunca copiar mundos, configurações pessoais ou caches.
    for name in ("builtin", "client/shaders", "clientmods", "fonts", "locale",
                 "textures/base/pack", "doc/pt_BR"):
        src = source / name
        if src.is_dir():
            shutil.copytree(src, destination / name,
                            ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"))
    for name in ("README.md", "LICENSE.txt", "COPYING.LESSER", "LICENSE-MIT"):
        shutil.copy2(source / name, destination / name)
    (destination / "games").mkdir(exist_ok=True)
    (destination / "LEIA-ME.txt").write_text(
        "AstraLua\n\nAbra bin/astralua.\n"
        "Os dados são salvos em ~/Luanti, inclusive minetest.conf, mods e worlds.\n"
        "Se já houver dados nessa pasta, faça uma cópia de segurança antes de\n"
        "usar uma nova versão. Não execute versões diferentes simultaneamente.\n"
        "Para testes separados, defina ASTRALUA_USER_PATH com outra pasta.\n"
        "Jogos podem ser instalados pelo menu Conteúdo.\n",
        encoding="utf-8",
    )

    copied = set()
    pending = dependencies(binary)
    while pending:
        library = pending.pop()
        if library.name in copied or SYSTEM_LIBS.match(library.name):
            continue
        target = destination / "lib" / library.name
        shutil.copy2(library.resolve(), target)
        copied.add(library.name)
        pending.extend(dependencies(library))
        subprocess.run(["patchelf", "--set-rpath", "$ORIGIN", str(target)], check=True)
    subprocess.run(["patchelf", "--set-rpath", "$ORIGIN/../lib",
                    str(destination / "bin/astralua")], check=True)

    (destination / "AppRun").write_text(
        '#!/bin/sh\n'
        '# SPDX-License-Identifier: MIT\n'
        'app_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd) || exit 1\n'
        'exec "$app_dir/bin/astralua" "$@"\n', encoding="utf-8")
    (destination / "AppRun").chmod(0o755)
    shutil.copy2(source / "misc/org.astralua.AstraLua.desktop", destination / "AstraLua.desktop")
    shutil.copy2(source / "misc/astralua.svg", destination / "astralua.svg")

    checksum_lines = []
    for file in sorted(destination.rglob("*")):
        if file.is_file():
            digest = hashlib.sha256(file.read_bytes()).hexdigest()
            checksum_lines.append(f"{digest}  {file.relative_to(destination)}")
    (destination / "SHA256SUMS").write_text("\n".join(checksum_lines) + "\n")
    return destination


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=Path.cwd())
    parser.add_argument("--destination", type=Path, required=True)
    args = parser.parse_args()
    destination = package(args.source, args.destination)
    archive = destination.with_name(destination.name + ".tar.gz")
    if archive.exists():
        raise RuntimeError("O arquivo de distribuição já existe.")
    with tarfile.open(archive, "x:gz") as output:
        output.add(destination, arcname="AstraLua")
    print(f"Pacote criado: {archive}")


if __name__ == "__main__":
    main()
