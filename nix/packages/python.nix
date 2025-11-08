{self, ...}: {
  perSystem = {
    self',
    pkgs,
    config,
    ...
  }: let
    pyprojectToml = builtins.fromTOML (builtins.readFile "${self}/pyproject.toml");
    rustLib = self'.packages.pyautomata-rust;
    
    # Python environment with all dependencies
    pythonEnv = pkgs.python313.withPackages (p:
      with p; [
        matplotlib
        numpy
        ipython
        jupyter
        config.packages.pyautomata
      ]);
  in {
    packages = {
      default = config.packages.pyautomata;
      
      # App package for Docker - this is what you'll build
      pyautomata-app = pkgs.stdenv.mkDerivation {
        name = "pyautomata-app";
        version = pyprojectToml.project.version;
        
        dontUnpack = true;
        dontBuild = true;
        
        installPhase = ''
          mkdir -p $out/bin
          cat > $out/bin/app <<'EOF'
          #!${pkgs.bash}/bin/bash
          export LOCALE_ARCHIVE="${pkgs.glibcLocales}/lib/locale/locale-archive"
          export LC_ALL="C.UTF-8"
          export UV_LINK_MODE=copy
          export LD_LIBRARY_PATH="${pkgs.lib.makeLibraryPath [pkgs.stdenv.cc.cc]}"
          export RUST_SRC_PATH="${pkgs.rustPlatform.rustLibSrc}"
          exec ${pythonEnv}/bin/jupyter notebook "$@"
          EOF
          chmod +x $out/bin/app
        '';
      };
      
      pyautomata = pkgs.python313Packages.buildPythonPackage {
        pname = pyprojectToml.project.name;
        version = pyprojectToml.project.version;

        # Use a minimal source with only what's needed
        src = pkgs.runCommand "pyautomata-src" {} ''
          mkdir -p $out/pyautomata
          cp ${self}/pyproject.toml $out/pyproject.toml

          # Copy Python package contents excluding rust
          for item in ${self}/pyautomata/*; do
            if [ "$(basename "$item")" != "rust" ]; then
              cp -r "$item" $out/pyautomata/
            fi
          done
        '';

        format = "pyproject";

        propagatedBuildInputs = with pkgs.python313Packages; [
          matplotlib
          numpy
          setuptools
        ];

        # Skip runtime dependency version checks - nixpkgs versions are close enough
        pythonRelaxDeps = true;

        # Create a rust subdirectory and symlink the Rust library
        postInstall = ''
          mkdir -p $out/lib/python3.13/site-packages/pyautomata/rust/target/release
          ln -s ${rustLib}/lib/libpyautomata_rust.so $out/lib/python3.13/site-packages/pyautomata/rust/target/release/libpyautomata_rust.so || \
          ln -s ${rustLib}/lib/libpyautomata_rust.dylib $out/lib/python3.13/site-packages/pyautomata/rust/target/release/libpyautomata_rust.dylib || \
          ln -s ${rustLib}/lib/pyautomata_rust.dll $out/lib/python3.13/site-packages/pyautomata/rust/target/release/pyautomata_rust.dll
        '';

        # Tests require the Rust library
        doCheck = false;

        meta = with pkgs.lib; {
          description = pyprojectToml.project.description;
          license = licenses.mit;
          maintainers = ["Michael Buckley"];
        };
      };
    };
  };
}
