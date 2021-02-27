from pandas import DataFrame

def store_stimulation(simulation, filename="name.csv"):
    data = DataFrame(data = {'debate': simulation, 'positions': simulation.positions})
    data.to_csv(filename)