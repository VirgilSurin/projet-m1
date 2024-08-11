echo "Select what to run:"
echo "1 - Python - Interactive"
echo "2 - Python - Benchmark"
echo "3 - Rust   - Interactive"
echo "4 - Rust   - Benchmark"
echo "5 - Plotting utilities"
echo "Enter your choice: "

read -r choice

case $choice in
    1)
        echo "Running interactive Python script..."
        (
            cd ./code || exit
            python3 main.py
        )
        ;;
    2)
        echo "Running Python benchmark..."
        (
            cd ./code || exit
            python3 benchmark.py
        )
        ;;
    3)
        echo "Running interactive Rust script..."
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
    5)
        echo "Running plotting utilities..."
        (
            cd ./code || exit
            python3 plot.py
        )
        ;;
    *)
        echo "Invalid choice. Please select a valid option."
        ;;
esac
