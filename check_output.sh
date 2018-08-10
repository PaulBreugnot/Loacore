for file in output/*
do
	echo $file
	tail -1 $file
done
