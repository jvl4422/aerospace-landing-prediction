"""
This is a constraint satisfaction program which assigns British Airways' fleet
to the different routes that they offer, over a day.

Authors: Karina Verma and Jasmine van Leeuwen

GETTING STARTED:
If you made a new conda env, make sure to navigate to that env and activate it in terminal
(this can be done through the anaconda interface).
Once your environment has been activated (you'll know because it will have the name
surrounded in parentheses), execute the following in terminal: python -m pip install --upgrade --user ortools
Then hopefully colouring will show up, and you'll be able to verify it has been installed correctly.
"""


from ortools.sat.python import cp_model

