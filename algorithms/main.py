import assessment
import comment
import dataset
import deepmodel
import utils
import time
from .assessment.main import score_main


def algorithm_main(image, template):
    while True:
        score, comment = score_main(image, template)
        time.sleep(0.05)
        func(score, comment)

if __name__ == '__main__':
    algorithm_main(image, template)
