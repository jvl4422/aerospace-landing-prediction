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
import pandas as pd

def format_model():
    # Should add some error checking here to say that if there are more dests to serve than planes, it is impossible to
    # solve this model
    model = cp_model.CpModel()
    dests_to_serve = open("satisfy_destinations.txt", "r").read().split()
    a330200 = pd.read_csv("a330200.csv", skiprows=1)
    planes = a330200.columns.to_list()[1:]
    if len(dests_to_serve) > len(planes):
        print("It is impossible to solve this model. The number of destinations cannot exceed the number of planes.")
        exit(1)
    max_total_fit = 100

    # I think I can give it intuitive names
    # Gonna make this a set and see, just because I don't forsee myself needing it again.
    all_dests = []
    idx_to_serve = {}
    # Add all of our destinations to a list in case we need it later
    for dest in a330200["destination"]:
        all_dests.append(dest)
    # Find the indices of the destinations we need to serve. This will be useful in making sure that we only
    # check the data that we need instead of everything.
    for each in dests_to_serve:
        idx = all_dests.index(each)
        idx_to_serve[idx] = each

    # Now that we have isolated our data, we are ready to create our variables.
    varbs = {}
    rows_of_interest = idx_to_serve.keys()
    for eachplane in planes:
        for eachdest in dests_to_serve:
            # I am still not entirely sure what the fstring is for but anyway!
            varbs[eachplane, eachdest] = model.NewBoolVar(f"varbs[{eachplane},{eachdest}]")

    # Now we add our constraints
    # The variables that are true for one destination must all be different
    # Meaning one destination can only have one plane

    # This constraint makes sure that one plane is not assigned to multiple destinations
    tack = []
    for eachplane in planes:
        diffList = []
        for eachdest in dests_to_serve:
            diffList.append(varbs[eachplane,eachdest])
        tack.append(diffList)
        # print(diffList, "must cannot all be true")

    # TODO: Strange bug but this is the only way to get it to work and have unique planes flying to unique destinations
    i = 0
    while i < 8:
        model.AddExactlyOne(tack[i])
        print(tack[i])
        i += 1

    # model.AddExactlyOne(testing[0])
    # model.AddExactlyOne(testing[1])


    # Each destination is added to exactly one plane
    # destination = task
    # plane = worker
    # This constraint is supposed to make sure that one destination is not assigned to multiple planes
    # but it is broken and I do not know why

    for eachdest in dests_to_serve:
        diffList = []
        for eachplane in planes:
            diffList.append(varbs[eachplane, eachdest])
        # print(diffList, "cannot all be true")
        model.AddExactlyOne(diffList)

    # Now set the objective of maximizing the fit scores
    objective_terms = []
    for eachplane in planes:
        for eachdestidx in idx_to_serve.keys():
            #if a330200[eachplane][eachdestidx] == 75:
                # print("Found an optimal match for", eachplane, "to", idx_to_serve[eachdestidx])
            objective_terms.append(a330200[eachplane][eachdestidx] * varbs[eachplane, idx_to_serve[eachdestidx]])
    model.Maximize(sum(objective_terms))
    return model, planes, idx_to_serve, varbs, a330200

def solve_results(model, planes, dests, varbs, fitscores):
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print("Successful assignment!")
        print(f"Fit score = {solver.ObjectiveValue()}\n out of", len(planes)*100)
        print("Assignments are as follows: ")
        for plane in planes:
            for destination in dests.keys():
                if solver.BooleanValue(varbs[plane, dests[destination]]):
                    print(
                        f"Plane {plane} assigned to fly to {dests[destination]}."
                        + f" Fit score = {fitscores[plane][destination]}"
                    )
    else:
        print("No solution found.")

def main():
    model, planes, dests, varbs, fitscores = format_model()
    solve_results(model, planes, dests, varbs, fitscores)

main()

