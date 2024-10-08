{ pkgs ? import <nixpkgs> {} }:

let
  python-packages = ps: with ps; [
    networkx
    tqdm
    numpy
    matplotlib
  ];
  my-python = pkgs.python311.withPackages python-packages;
in
pkgs.mkShell {
  packages = [
    (my-python)
  ];
}
