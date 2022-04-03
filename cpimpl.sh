#Copies all deserialization.py from implementations directory
#Adds a number to the name
#Usage ./cpimpl
n=0
for f in `ls implementations`
do
cp implementations/$f/deserialization.py deserialization${n}.py
n=`expr $n + 1`
done
