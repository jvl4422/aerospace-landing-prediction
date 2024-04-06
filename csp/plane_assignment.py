"""
This is a constraint satisfaction program which assigns British Airways' fleet
to the different routes that they offer, over a day.

Authors: Karina Verma and Jasmine van Leeuwen

GETTING STARTED:
We recommend you make a new Python environment for this project to avoid any potential library clashes.
If you made a new conda env, make sure to navigate to that env and activate it in terminal
(this can be done through the anaconda interface).
Once your environment has been activated (you'll know because it will have the name
surrounded in parentheses), execute the following in terminal: python -m pip install --upgrade --user ortools
Then hopefully colouring will show up here which verifies it has been installed correctly.
"""
from ortools.sat.python import cp_model
import pandas as pd

"""
This function creates and formats the CP Model by reading in the data and adding the relevant constraints.

:returns model - CP Model, planes, idx_to_serve, varbs, a330200
         planes - list of all plane names
         idx_to_serve - dictionary with indices which correspond to the rows that are the destinations to be served
         varbs - the variables added to the CP Model
         a330200 - the fit score data frame
"""
def format_model():
    model = cp_model.CpModel()
    dests_to_serve = open("satisfy_destinations.txt", "r").read().split()
    a330200 = pd.read_csv("a330200.csv", skiprows=1)
    planes = a330200.columns.to_list()[1:]
    if len(dests_to_serve) > len(planes):
        print("It is impossible to solve this model. The number of destinations cannot exceed the number of planes.")
        exit(1)
    max_total_fit = 100

    # Made a list of all destinations
    all_dests = []
    idx_to_serve = {}
    # Add all of our destinations to a list in case we need it later
    for dest in a330200["destination"]:
        all_dests.append(dest)
    # Find the indices of the destinations we need to serve. This will be useful in making sure that we only
    # check the data that we need instead of everything.

    # Find the row index of each destination that is to be served.
    for each in dests_to_serve:
        idx = all_dests.index(each)
        idx_to_serve[idx] = each

    # Now that we have isolated our data, we are ready to create our variables.
    varbs = {}
    # Create a boolean variable for each plane and destination combination.
    for eachplane in planes:
        for eachdest in dests_to_serve:
            # Name our boolean variable and add it to our variable dictionary
            entry = model.NewBoolVar(f"v[{eachplane},{eachdest}]")
            varbs[(eachplane, eachdest)] = entry

    # Now we add our constraints

    # TODO: Modify constraints so that when there is a destination that ~cannot~ be served by a particular plane
    # The constraint enforces that. I am not sure whether that might require removing the boolean variable as an option.

    # This constraint makes sure that one plane is not assigned to multiple destinations
    tack = []
    xorlist = []
    for eachplane in planes:
        # Will track destinations to ensure that one plane is not assigned to multiple destinations
        diffList = []
        # Will track destinations to ensure that
        xorelems = []
        # This is a flag that represents if we need to add a constraint. It will flag if there is a destination
        # that a plane cannot serve. Then we must make sure it is grounded instead of flying to that destination
        findground = False
        for eachdestidx in idx_to_serve:
            score = a330200[eachplane][eachdestidx]
            if score < 1:
                # If we have not been assigned to a destination that is servable (We have been
                # assigned to an unservable destination) THEN we must be grounded
                # If we have not been assigned to any destinations that are servable, THEN we MUST be grounded
                xorelems.append(varbs[(eachplane, all_dests[eachdestidx])].Not())
                findground = True
            # We use one to correspond to grounded
            elif score == 1 and findground:
                xorelems.append(varbs[(eachplane, all_dests[eachdestidx])])
            diffList.append(varbs[eachplane,all_dests[eachdestidx]])
        tack.append(diffList)
        # If we have a plane with unservable destinations, add it to the list of constraints
        if len(xorelems) != 0:
            xorlist.append(xorelems)
        # print(diffList, "must cannot all be true")

    # Adding intermediate variable. It represents whether we have been able to add a servable destination
    b = model.NewBoolVar("b")

    # Add constraints to ensure one plane does not fly to multiple destinations
    i = 0
    while i < len(tack):
        model.AddExactlyOne(tack[i])
        i += 1

    # Add constraint to ensure that if our plane has not been assigned ONE servable destinations (Exclusive Or)
    # then it HAS to be grounded
    i = 0
    while i < len(xorlist):
        # We will only enforce this constraint if we have not been able to add a servable destination
        model.AddBoolAnd(xorlist[i]).OnlyEnforceIf(b.Not())
        i += 1


# Maybe I can make a constraint where if the plane has not been assigned a destination it can serve, then it MUST be grounded


    # This constraint ensures that one destination is not served by multiple planes
    # Ensure that one destination is not served by multiple planes.
    for eachdest in dests_to_serve:
        diffList = []
        for eachplane in planes:
            diffList.append(varbs[eachplane, eachdest])
        # print(diffList, "cannot all be true")
        if eachdest == "ground":
            # Logically, any number of none constraints can be true. THey can be true ONLY IF there are
            # destinations than planes, and the plane has not been assigned any other value.

            # Maybe if I pass and don't make any constraints it'll work
            pass
            # model.Add(diffList).OnlyEnforceIf(len(planes) > len(dests_to_serve))
        else:
            model.AddExactlyOne(diffList)

    # Now set the objective of maximizing the fit scores
    objective_terms = []
    for eachplane in planes:
        for eachdestidx in idx_to_serve.keys():
            if a330200[eachplane][eachdestidx] > 0:
                objective_terms.append(a330200[eachplane][eachdestidx] * varbs[eachplane, idx_to_serve[eachdestidx]])
    model.Maximize(sum(objective_terms))
    return model, planes, idx_to_serve, varbs, a330200

"""
This method solves the constraint satisfaction problem and prints the results to the console. 
"""
def solve_results(model, planes, dests, varbs, fitscores):
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print("Successful assignment!")
        if status == cp_model.OPTIMAL:
            print("Optimal Solution")
        print(f"Fit score = {solver.ObjectiveValue()}\n out of", len(planes)*100)
        print("Assignments are as follows: ")
        for plane in planes:
            for destination in dests.keys():
                if solver.BooleanValue(varbs[plane, dests[destination]]) and dests[destination] != "ground":
                    print(
                        f"Plane {plane} assigned to fly to {dests[destination]}."
                        + f" Fit score = {fitscores[plane][destination]}"
                    )
                elif solver.BooleanValue(varbs[plane, dests[destination]]) and dests[destination] == "ground":
                    print(
                        f"Plane {plane} has been grounded."
                        + f" Fit score = {fitscores[plane][destination]}"
                    )
        print("=====Stats:======")
        print(solver.SolutionInfo())
        print(solver.ResponseStats())
    else:
        print("No solution found.")

def main():
    model, planes, dests, varbs, fitscores = format_model()
    solve_results(model, planes, dests, varbs, fitscores)

main()

