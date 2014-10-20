# script requires RUN.py is in the same directory, and that sample ins/outs are in
# <LOCAL_DIR>/sample_tests
if [ ! -d test ]; then
    mkdir test 
fi
regex="in([0-9]+)\.txt"
for file in $(ls sample_tests)
do
    if [[ $file =~ $regex ]]; then
        num="${BASH_REMATCH[1]}"
	./RUN.py sample_tests/$file > test/out$num
        mydiff=$(diff sample_tests/out$num.txt test/out$num)
        if [[ -n $mydiff ]]; then
            OUTPUT=$OUTPUT"Test $num failed: $mydiff"
        fi
    fi
done
if [[ -z $OUTPUT ]]; then
    echo PASS
else
    echo $OUTPUT
fi
