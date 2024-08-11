echo "Select what to run:"
echo "1 - Benchmark Python"
echo "2 - Main Python"
echo "3 - Main Rust"
echo "4 - Benchmark Rust"
echo "Enter your choice: "

read -r choice

case $choice in
    1)
        echo "Running Python benchmark..."
        python3 ./code/benchmark.py
        ;;
    2)
        echo "Running Python main..."
        python3 ./code/main.py
        ;;
    3)
        echo "Running Rust main..."
        (
            cd ./code/rust_cliques || exit
            cargo run --bin interactive
        )
        ;;
    4)
        echo "Running Rust benchmark..."
        (
            cd ./code/rust_cliques || exit
            cargo run --bin benchmark
        )
        ;;
    *)
        echo "Invalid choice. Please select a valid option."
        ;;
esac
