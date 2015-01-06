FILES=images/*.*.bmp
for f in $FILES
do
  echo "Erasing $f file..."
  rm $f
done

FILES=images/*.bmp
for f in $FILES
do
  echo "Processing $f file..."
  #echo ${f:0:7}
  #echo ${f:7:12}
  #python3 erosion.py ${f:0:7} ${f:7:12}
  python3 sectionMap.py ${f:0:7} ${f:7:12}
done
