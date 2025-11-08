{pkgs ? import <nixpkgs> {}}:
pkgs.mkShell {
  buildInputs = with pkgs; [
    # Python
    python313
    python313Packages.pip
    uv
    ruff
    gcc
    pkg-config

    # Rust toolchain
    cargo
    rustc
    rustfmt
    clippy
    rust-analyzer

    # Pre-commit
    lefthook
    typos
    bandit
  ];
  env = {
    LD_LIBRARY_PATH = with pkgs;
      lib.makeLibraryPath [
        stdenv.cc.cc
      ];
    # Rust environment variables
    RUST_SRC_PATH = "${pkgs.rustPlatform.rustLibSrc}";
  };

  shellHook = ''
    lefthook install
    export LOCALE_ARCHIVE="${pkgs.glibcLocales}/lib/locale/locale-archive"
    export LC_ALL="C.UTF-8"
    export UV_LINK_MODE=copy
    export UV_PROJECT_ENVIRONMENT="$VIRTUAL_ENV"
    git fetch
    git status --short --branch
  '';
}
