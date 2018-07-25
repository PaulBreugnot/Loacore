for file in ./raw/uci/*.txt; do
	echo "Process $file"
	vim -c ":%s/\t0/\tneg/g" -c ":%s/\t1/\t1\t0\t0/g" -c ":%s/\tneg/\t0\t1\t0/g" -c ":wq" $file
done
