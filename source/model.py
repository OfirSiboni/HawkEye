%load_ext autoreload
%autoreload 2

import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline

from steppy.base import Step, BaseTransformer

EXPERIMENT_DIR = './ex1'
import shutil

# By default pipelines will try to load previously trained models so we delete the cache to ba sure we're starting from scratch
shutil.rmtree(EXPERIMENT_DIR, ignore_errors=True)
