# %%
import data_getter
import data_analyser
import pandas as pd
import importlib
importlib.reload(data_analyser)

# %%
if __name__ == '__main__':
    # This part of the program fetches the data from the API and writes it into a json files 
    months = [3, 4, 5, 6, 7, 8, 9]
    max_workers = 3
    period = 11
    loop_over = 3
    origins = ['BHX', 'MAN']
    destinations = ['IAS']

    """for origin in origins:
        for destination in destinations:
            object1 = data_getter.api_caller_one_way_tickets(origin, destination, adults =4, children = 0, months = months)
            object1.using_threads(max_workers, period, loop_over)
    """


    # This part of the program fetches the data that was written to the json files 
    list_filenames = data_analyser.filename_getter(origins, destinations)
    print(list_filenames)
    fetched_data_from_files = data_analyser.sanitisation(list_filenames)
    dict_dfs = data_analyser.creating_dfs(list_filenames, fetched_data_from_files)
    list_keys=[]
    for key in dict_dfs.keys():
        list_keys.append(key)
    fig, ax = data_analyser.making_plot()
    data_analyser.plot_graph(list_keys[0], dict_dfs[list_keys[0]].index, dict_dfs[list_keys[0]]['price'],ax, line_colour = 'red')
    data_analyser.plot_graph(list_keys[1], dict_dfs[list_keys[1]].index, dict_dfs[list_keys[1]]['price'],ax, line_colour = 'blue')

