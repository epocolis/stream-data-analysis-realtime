from pyspark import SparkConf, SparkContext
from pyspark.mllib.feature import HashingTF
from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.classification import NaiveBayes

text = "test text Hashing term frequency vectorizer with 50k features"
# Hashing term frequency vectorizer with 50k features
htf = HashingTF(50000)
lp = LabeledPoint("0", htf.transform(text))
t1 = "this is a test"
t2= "you have won"
t3= "i have won"
t4 = "real test"
data = [LabeledPoint(0.0, htf.transform(t1)),
        LabeledPoint(1.0, htf.transform(t2)),
        LabeledPoint(0.0, htf.transform(t4)),
        LabeledPoint(1.0, htf.transform(t3))]

#data = [LabeledPoint(0.0, [0.0, 0.0]), LabeledPoint(0.0, [0.0, 1.0]),LabeledPoint(1.0, [1.0, 0.0])]
model = NaiveBayes.train(sc.parallelize(data))
model.predict(array([0.0, 1.0]))
