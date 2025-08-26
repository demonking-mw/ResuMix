#!/bin/bash
echo "code segment tester"
# Must be ran at the repo root
touch grass
# Takes one input, which is the file name of the test suite to run.
if [ ${#} -ne 1 ]; then
    echo "Usage: takes 1 argument: stem of test suite txt file" >&2
    exit 1
fi

VENV_PATH="./venv"  # Change this if your venv is in a different location

# Check if venv is already activated
if [[ -z "$VIRTUAL_ENV" ]]; then
    if [[ -d "$VENV_PATH" ]]; then
        echo "Activating virtual environment..."
        source "$VENV_PATH/bin/activate"
    else
        echo "Error: Virtual environment not found at $VENV_PATH"
        exit 1
    fi
else
    echo -e "Virtual environment active.\n"
fi
echo "black-ing"
black .
echo -e "\n"
echo -e "update all.txt\n"

# Update all.txt
all_file="./backend/src/segment_tests/lists/all.txt"
> "$all_file"  # Clear the all.txt file
for file in ./backend/src/segment_tests/*; do
    if [ -f "$file" ]; then
        filename=$(basename -- "$file")
        stem="${filename%.*}"
        echo "$stem" >> "$all_file"
    fi
done

test_file="./backend/src/segment_tests/lists/$1.txt"

if [ ! -f "$test_file" ]; then
    echo "Error: Test suite file not found: $1" >&2
    exit 1
fi


pass_count=0
fail_count=0
for indiv_test in $(cat $test_file | tr -d '\r'); do
    echo -e "\nAttempt to run test $indiv_test: "
    python -m backend.src.segment_tests."$indiv_test"
    if [ $? -eq 0 ]; then
        echo "Test $indiv_test passed"
        pass_count=$((pass_count + 1))
    else
        echo "Test $indiv_test failed"
        fail_count=$((fail_count + 1))
    fi
done
echo -e "\n\nTests completed. Passed: $pass_count, Failed: $fail_count"
if [ $fail_count -eq 0 ]; then
    echo -e "🌸🎂🎉 Cheers! MW 🎉🎂🌸 \n\n"
fi

exit $fail_count


