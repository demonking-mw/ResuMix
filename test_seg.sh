#!/bin/bash


# Takes one input, which is the file name of the test suite to run.

if [ ${#} -ne 1 ]; then
    echo "Usage: takes 1 argument: stem of test suite txt file" >&2
    exit 1
fi


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


