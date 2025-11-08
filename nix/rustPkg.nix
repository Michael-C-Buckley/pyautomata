{pkgs ? import <nixpkgs> {}}: let
  cargoToml = builtins.fromTOML (builtins.readFile ../pyautomata/rust/Cargo.toml);
in
  pkgs.rustPlatform.buildRustPackage {
    pname = cargoToml.package.name;
    version = cargoToml.package.version;

    src = ../pyautomata/rust;

    cargoLock.lockFile = ../pyautomata/rust/Cargo.lock;

    buildPhase = "cargo build --release --lib";

    installPhase = ''
      mkdir -p $out/lib
      cp target/release/libpyautomata_rust.so $out/lib/ || \
      cp target/release/libpyautomata_rust.dylib $out/lib/ || \
      cp target/release/pyautomata_rust.dll $out/lib/
    '';

    meta = with pkgs.lib; {
      description = "Rust acceleration library for PyAutomata";
      license = licenses.mit;
    };
  }
