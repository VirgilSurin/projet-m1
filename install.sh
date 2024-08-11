command_exists() {
    command -v "$1" >/dev/null 2>&1
}

echo "Checking for Rust..."
if command_exists rustc; then
    echo "Rust is installed."
else
    echo "Rust is not installed. Please install Rust from https://rustup.rs/"
    exit 1
fi

check_and_install_package() {
    PACKAGE=$1
    echo "Checking for Python package $PACKAGE..."
    if python3 -c "import $PACKAGE" >/dev/null 2>&1; then
        echo "$PACKAGE is already installed."
    else
        echo "$PACKAGE is not installed. Installing $PACKAGE..."
        pip install $PACKAGE
    fi
}

echo "Checking for pip..."
if command_exists pip3; then
    echo "pip is installed. Ensuring pip is up to date..."
    pip3 install --upgrade pip
else
    echo "pip is not installed. Installing pip..."
    python3 -m ensurepip --upgrade
fi

REQUIRED_PACKAGES=(networkx tqdm numpy matplotlib)
for PACKAGE in "${REQUIRED_PACKAGES[@]}"; do
    check_and_install_package $PACKAGE
done

echo "All checks passed and installations completed."
