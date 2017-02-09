##run inference procedures

#python bigramanneal.py #bigrams, annealing
#python bigramMDL1anneal.py #bigrams, MDL1, annealing
#python unibigramanneal.py #uni+bigrams, annealing
#python unibigramMDL1anneal.py #uni+bigrams, MDL1, annealing
#python unibigramMDL1anneal.py #uni+bigrams, MDL2, annealing
#python unibigramMDL1anneal.py #uni+bigrams, MDL1, prior on component membership, annealing

##get f-, v-, NVI measures
for fn in *MAP.txt;
do
  echo $fn;
  python2.6 fvmeasure.py $fn;
done


##get MAP configuration for simulation, for chain = {0,1,2}:
#python getmapnum.py [simulation] [chain]
