{
  description = "Pyautomata Nix Flake";

  nixConfig = {
    extra-substituters = [ "https://pyautomata.cachix.org" ];
    extra-trusted-public-keys = [ "pyautomata.cachix.org-1:VXD1o4jdYUFm5EaWWrO/gm5IqT9w5p6WeTf/GqkVorU=" ];
  };

  outputs = {flake-parts, ...} @ inputs:
    flake-parts.lib.mkFlake {inherit inputs;} {
      systems = ["x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin"];

      imports = [
        ./nix/apps.nix
        ./nix/devshells.nix
        ./nix/packages/rust.nix
        ./nix/packages/python.nix
      ];
    };

  inputs = {
    nixpkgs.url = "https://channels.nixos.org/nixos-unstable/nixexprs.tar.xz";
    flake-parts.url = "github:hercules-ci/flake-parts";
  };
}
