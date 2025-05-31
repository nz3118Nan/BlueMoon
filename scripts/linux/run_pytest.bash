#!/bin/bash

# Create test reports directory if it doesn't exist
mkdir -p reports

# Function to run tests and generate report
run_tests() {
    local test_type=$1
    local report_file=$2
    
    echo "Running $test_type tests..."
    pytest -m $test_type -v --html=reports/$report_file.html --self-contained-html
}

# Run unit tests
run_tests "unit" "unit_test_report" 

# Run integration tests
run_tests "integration" "integration_test_report"

# Run smoke tests
run_tests "smoke" "smoke_test_report"

echo "All test reports have been generated in reports/"
