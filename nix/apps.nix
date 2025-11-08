{
  perSystem = {self', pkgs, ...}: {
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
