regex="in([0-9]+)\.txt"
for file in $(ls sample_tests)
do
    if [[ $file =~ $regex ]]; then
        num="${BASH_REMATCH[1]}"
	./RUN.py sample_tests/$file > test/out$num
        OUTPUT=$OUTPUT"$(diff sample_tests/out$num.txt test/out$num)"
    fi
done
if [[ -z $OUTPUT ]]; then
    echo PASS
fi
