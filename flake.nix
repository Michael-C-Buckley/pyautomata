{
  description = "Pyautomata Nix Flake";

  outputs = {flake-parts, ...} @ inputs:
    flake-parts.lib.mkFlake {inherit inputs;} {
      systems = ["x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin"];

      imports = [
        ./nix/rustPkgs.nix
        ./nix/pythonPkgs.nix
      ];

      perSystem = {pkgs, ...}: {
        devShells.default = import ./nix/shell.nix {inherit pkgs;};
      };
    };

  inputs = {
    nixpkgs.url = "https://channels.nixos.org/nixos-unstable/nixexprs.tar.xz";
    flake-parts.url = "github:hercules-ci/flake-parts";
  };
}