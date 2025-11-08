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

    apps = {
      default = {
        type = "app";
        program = let
          pythonWithPkgs = pkgs.python313.withPackages (p:
            with p;
              [
                matplotlib
                numpy
                ipython
                jupyter
              ]
              ++ [self'.packages.pyautomata]);
        in "${pkgs.writeShellScript "run-jupyter" ''
          export LOCALE_ARCHIVE="${pkgs.glibcLocales}/lib/locale/locale-archive"
          export LC_ALL="C.UTF-8"
          export UV_LINK_MODE=copy
          export LD_LIBRARY_PATH="${pkgs.lib.makeLibraryPath [pkgs.stdenv.cc.cc]}"
          export RUST_SRC_PATH="${pkgs.rustPlatform.rustLibSrc}"
          exec ${pythonWithPkgs}/bin/jupyter notebook "$@"
        ''}";
      };
    };
  };
}
