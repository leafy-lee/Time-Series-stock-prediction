

from loaddata import Data_Reader
from granger import granger_test
from predict import Predictor


def posprocess(predictor, prediction):
    prediction = pdt.auto_predict()
    for stock in prediction:
        print("prediction of %d" % stock)
        absmax = 0
        ave = 0
        for influence in prediction[stock]:
            print("\t from %d with lags %d is %lf" % influence)
            ave += influence[2]
            if abs(influence[2]) > abs(absmax):
                absmax = influence[2]
        ave /= len(prediction[stock])
        print("the bravest prediction is ", absmax)
        print("average prediction is", ave)
        print("the ground truth is ", list(gt["stock"+str(stock)])[0])


def main():
    loader = Data_Reader()
    granger_data = loader.forward()
    granger_result = granger_test(granger_data)
    predictor = Predictor(granger_data, granger_result)
    prediction = predictor.auto_predict()
    posprocess(predictor, prediction)


if __name__ == "__main__":
    main()
