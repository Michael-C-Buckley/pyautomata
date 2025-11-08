{
  perSystem = {
    self',
    pkgs,
    ...
  }: let
    env = {
      LD_LIBRARY_PATH = with pkgs; lib.makeLibraryPath [stdenv.cc.cc];
      RUST_SRC_PATH = "${pkgs.rustPlatform.rustLibSrc}";
    };
    shellLines = ''
      export LOCALE_ARCHIVE="${pkgs.glibcLocales}/lib/locale/locale-archive"
      export LC_ALL="C.UTF-8"
      export UV_LINK_MODE=copy
      export UV_PROJECT_ENVIRONMENT="$VIRTUAL_ENV"
    '';
  in {
    devShells = {
      default = pkgs.mkShell {
        inherit env;
        buildInputs = with pkgs; [
          # Python
          python313
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
        shellHook =
          shellLines
          + ''
            lefthook install
            git fetch
            git status --short --branch
          '';
      };
    };
  };
}
