# -*- coding: utf-8 -*-
"""
Created on Fri Nov 19 18:03:40 2021

@author: wli3535
"""

from tensorboard import default
from tensorboard import program


tracking_address = "logger/R1_34_env_multi_new_31"

if __name__ == "__main__":
    tb = program.TensorBoard()
    tb.configure(argv=[None,'--logdir',tracking_address])
    tb.main()