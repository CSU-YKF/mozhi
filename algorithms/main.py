import assessment
import comment
import dataset
import deepmodel
import utils
import time


from .assessment.main import score_main
from .deepmodel.main import main as deepmodel_main

def algorithm_main(image, template):
    while True:
        score1, comment = score_main(image, template)
        score2 = deepmodel_main(image)
        score = (score1 + score2) / 2
        time.sleep(0.05)
        func(score, comment)

if __name__ == '__main__':
    algorithm_main(image, template)
