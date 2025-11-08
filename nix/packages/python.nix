{self, ...}: {
  perSystem = {
    self',
    pkgs,
    config,
    ...
  }: let
    pyprojectToml = builtins.fromTOML (builtins.readFile "${self}/pyproject.toml");
    rustLib = self'.packages.pyautomata-rust;
  in {
    packages.pyautomata = pkgs.python313Packages.buildPythonPackage {
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

    packages.default = config.packages.pyautomata;
  };
}
