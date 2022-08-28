"""Docstring"""
import matplotlib.pyplot as plt
import numpy as np
import os

def data_tuple_from_line(line_str):
    """ 
    Takes a line of input and returns a tuple containing:
    (install_ID, install_date, size, subsidy, cost, zip, city, state)
    Where the Install_ID, install_date, zip, city and state are all strings and
    the size, cost and subsidy are all floats
    """

    split_list = line_str.split(',')
    for number in split_list[2:5]:
        split_list[split_list.index(number)] = float(number)
        split_list[-2] = split_list[-2].title()
    return tuple(split_list)

def is_valid_line_data(line_data_tuple):
    """
    Takes a list of values and returns True if none of the values
    in line_data equals -1 or '-1'.
    Assumes relevant values have been converted to floats
    """

    return all(item != -1 and item != '-1' for item in line_data_tuple)

def read_solar_data(filename):
    """ 
    Takes a list of values and returns True if none of the values
    in line_data equals -1 or '-1'.
    Assumes relevant values have been converted to floats
    """

    info = []
    with open(filename, 'r') as data:
        for line in data.read().splitlines()[1:]:
            if is_valid_line_data(data_tuple_from_line(line)):
                info.append(data_tuple_from_line(line))
    return info

def installs_by_state(solar_data):
    """ 
    Takes a solar data list (as generated by read_solar_data) and
    returns a dictionary where the keys are city names and the value
    associated with each key is the number of solar installations in
    that city.
    """

    info_dict = dict()
    for installation in solar_data:
        info_dict[installation[7]] = info_dict.get(installation[7], 0 ) + 1
    return info_dict

def installs_by_year(solar_data):
    """ 
    Takes a solar data list (as generated by read_solar_data) and
    returns a dictionary where the keys are years (as ints) and the value
    associated with each year is the number of solar installations in
    that year.
    """

    info_dict = dict()
    for installation in solar_data:
        year = int(installation[1].split('-')[0])
        info_dict[year] = info_dict.get(year, 0 ) + 1
    return info_dict

def total_kw_by_year(solar_data):
    """
    Takes a solar data list (as generated by read_solar_data) and
    returns a dictionary where the keys are years (as ints) and the value
    associated with each year is the combined total size of solar installs
    in that year.
    """

    info_dict = dict()
    for installation in solar_data:
        year = int(installation[1].split('-')[0])
        info_dict[year] = info_dict.get(year, 0 ) + installation[2]
    return info_dict

def average_net_cost_per_kw_by_year(solar_data):
    """
    Takes a solar data list (as generated by read_solar_data) and
    return a dictionary where the keys are years (as ints) and the value
    associated with each year is the average cost of solar installs
    in that year
    """

    cost_dict = dict()
    for installation in solar_data:
        year = int(installation[1].split('-')[0])
        net_cost_per_kw = (installation[3]-installation[4])/installation[2]
        cost_dict[year] = cost_dict.get(year, 0) + net_cost_per_kw
    install_per_year = installs_by_year(solar_data)
    for key, value in cost_dict.items():
        cost_dict[key] = cost_dict.get(key) / install_per_year.get(key)
    return cost_dict

def create_lists(data_dict):
    """
    Mini functions to create x and ys from a dictionary
    """

    xs = list(data_dict.keys())
    ys = list(data_dict.values())
    return xs, ys

def bar_graph_from_dict(data_dict, title, xlabel, ylabel):
    """
    Plots a bar grah from given dictionary with specific
    title, xlabel and ylabel
    """

    sorted_dict = dict(sorted(data_dict.items()))
    xs, ys = create_lists(sorted_dict)
    xs.sort()
    xticks = np.arange(0, (len(xs)))
    axes = plt.axes()
    axes.set_title(title)
    axes.set_xlabel(xlabel)
    axes.set_xticks(xticks)
    axes.set_xticklabels(xs)
    axes.set_ylabel(ylabel)
    axes.bar(xs, ys, color='darkgreen')
    plt.show()

def plot_from_dict(data_dict, title, xlabel, ylabel):
    """
    Plots a graph given dictionary with specific
    title, xlabel and ylabel
    """

    sorted_dict = dict(sorted(data_dict.items()))
    xs, ys = create_lists(sorted_dict)
    xs.sort()
    axes = plt.axes()
    axes.grid(True)
    axes.set_title(title)
    axes.set_xlabel(xlabel)
    axes.set_xticks(xs)
    axes.set_xticklabels(xs)
    axes.set_ylabel(ylabel)
    axes.plot(xs, ys, color='darkgreen', linestyle='-', marker='o')
    plt.show()

def plot_yearly_installs_vs_costs(cost_dict, installs_dict):
    """
    Takes two dictionaries, one with year:avg_cost_per_kwh mappings
    and the other with year:num_installs mappings.
    
    Plots the number of installs vs the average cost. The x values are
    the average costs and the y values are the number of installs.
    """

    xs = list(cost_dict.values())
    ys = list(installs_dict.values())
    axes = plt.axes()
    axes.grid(True)
    axes.set_title("Installs vs Average cost per kw")
    axes.set_xlabel("Average net cost ($/kw)")
    axes.set_ylabel("Yearly number of installs")
    axes.plot(xs, ys, color='darkgreen', linestyle='', marker='o')
    plt.show()

def fit_line_to_installs_vs_year(yearl_installs_dict, last_year_to_include):
    """
    Fits a straight line to the equation:
    log_base_e(installs) = a * year + b
    Only includes years up to last year to include.
    Actual data is plotted as green dots, with points order by year
    Fitted line, which is the plot of e^(a*year + b) as orange
    """

    edited_dict = dict((k, v) for k, v in yearl_installs_dict.items() if k <= last_year_to_include)
    sorted_dict = dict(sorted(edited_dict.items()))
    xs, ys = create_lists(sorted_dict)
    new_ys = np.log(ys)
    alpha, beta = np.polyfit(xs, new_ys, 1)
    predicted_installs = np.exp(alpha*np.array(xs)+beta)
    axes = plt.axes()
    axes.grid(True)
    axes.set_title(f"Installs up to {last_year_to_include}")
    axes.set_xlabel("Year")
    axes.set_ylabel("Yearly number of installs")
    axes.set_xticks(xs)
    axes.set_xticklabels(xs, rotation=90)
    axes.plot(xs, ys, color='darkgreen', linestyle='-', marker='o', label = 'actual')
    axes.plot(xs, predicted_installs, color='orange', linestyle='--', marker='+', label = 'fitted')
    axes.legend()
    plt.show()

def main():
    data = read_solar_data(r"C:\Users\domin\Desktop\UNI\COSC131\test_data\data_500_a.txt")
    installed = installs_by_year(data)
    fit_line_to_installs_vs_year(installed, 2020)


if __name__ == "__main__":
    main()