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
  #python erosion.py ${f:0:7} ${f:7:12}
  #python centering.py ${f:0:7} ${f:7:12}
  #python slopes.py ${f:0:7} ${f:7:12}
  #python rotation.py ${f:0:7} ${f:7:12}
  python binarization.py ${f:0:7} ${f:7:12}
  python sectionMap.py ${f:0:7} ${f:7:12}
done
