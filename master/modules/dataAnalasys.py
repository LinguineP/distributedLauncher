import csv
import dbAdapter
import utils
from config import cfg
from datetime import datetime
import matplotlib.pyplot as plt
import math

db_adapter = dbAdapter.SQLiteDBAdapter()


def generate_csv_from_combined_data():
    # data from all sessions or just from one?
    current_datetime = datetime.now()
    filename = current_datetime.strftime("%Y-%m-%d_%H:%M:%S")
    filepathname = utils.escape_chars(f"{cfg['dbPath']}\{'csv'}\{filename}")

    data = db_adapter.analysis.get_detailed_combined_data()

    with open(filepathname, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        # Write headers
        writer.writerow(
            [
                "Session Name",
                "Session Script",
                "Batch Number",
                "Param Used",
                "Number of Nodes",
                "Run Number",
                "Execution Time",
            ]
        )
        # Write rows
        for row in data:
            writer.writerow(row)
    print(f"CSV file '{filename}' has been generated successfully.")


def calculate_mean_time(times):
    if not times:
        return None
    total_time = sum(times)
    mean_time = total_time / len(times)
    return mean_time


def calculate_standard_deviation(times):
    if not times:
        return None
    mean_time = sum(times) / len(times)
    squared_diff_sum = sum((time - mean_time) ** 2 for time in times)
    variance = squared_diff_sum / len(times)
    std_deviation = math.sqrt(variance)
    return std_deviation


def plot_times_with_stats(session_name, batch_param, times, unit):
    # Calculate mean time and standard deviation
    mean_time = calculate_mean_time(times)
    std_deviation = calculate_standard_deviation(times)

    current_datetime = datetime.now()
    filename = session_name + "_" + current_datetime.strftime("%Y-%m-%d_%H:%M:%S")
    save_path = utils.escape_chars(
        f"{cfg['dbPath']}\{'images'}\{session_name}\batchresults\{filename}"
    )

    plt.hist(times, bins=20, alpha=0.7, color="blue", edgecolor="black")

    plt.axvline(mean_time, color="red", linestyle="dashed", linewidth=1, label="Mean")
    plt.axvline(
        mean_time + std_deviation,
        color="green",
        linestyle="dashed",
        linewidth=1,
        label="Std Deviation",
    )
    plt.axvline(
        mean_time - std_deviation, color="green", linestyle="dashed", linewidth=1
    )

    # Add legend and labels
    plt.legend()
    plt.xlabel(f"Execution Time[{unit}]")
    plt.ylabel("Frequency")
    plt.title(
        "Execution times distribution in session "
        + session_name
        + "with params"
        + batch_param
    )

    plt.savefig(save_path)

    return std_deviation, mean_time, save_path


def convert_times(list_of_times):

    max_time = max(
        list_of_times
    )  # we re basing our conversion on a max value, so that every value is properly represented

    if max_time < 1e-6:
        # Convert to ns
        converted_times = [time * 1e9 for time in list_of_times]
        unit = "ns"
    elif max_time < 1e-3:
        # Convert to microseconds
        converted_times = [time * 1e6 for time in list_of_times]
        unit = "µs"
    elif max_time < 1:
        # Convert to ms
        converted_times = [time * 1e3 for time in list_of_times]
        unit = "ms"
    else:
        # just seconds
        converted_times = list_of_times
        unit = "s"

    return converted_times, unit


def convert_to_seconds(value, unit):
    if unit == "ns":
        return value / 1e9
    elif unit == "µs":
        return value / 1e6
    elif unit == "ms":
        return value / 1e3
    elif unit == "s":
        return value
    else:
        raise ValueError("Invalid unit of measurement")


def analyse_session_batches(session_id, session_name):
    db_adapter.batch_results.reset_batch_results_for_session(session_id)
    session_batches_data = db_adapter.analysis.get_session_batches_with_times(
        session_id
    )

    for batch in session_batches_data:
        times, unit = convert_times(batch["batch_times"])
        std_deviation, mean, graph_path = plot_times_with_stats(
            session_name, batch["param_used"], times, unit
        )
        db_adapter.batch_results.insert_batch_result(
            batch["batch_id"],
            convert_to_seconds(std_deviation, unit),
            convert_to_seconds(mean, unit),
            graph_path,
        )


def plot_meantime_nodes_number(session_name, nodes, meantime, unit):

    current_datetime = datetime.now()
    filename = (
        session_name
        + "_"
        + "meantime"
        + "_"
        + current_datetime.strftime("%Y-%m-%d_%H:%M:%S")
    )
    save_path = utils.escape_chars(
        f"{cfg['dbPath']}\{'images'}\{session_name}\{filename}"
    )

    plt.plot(nodes, meantime, "o", label="Mean time as functions of number of nodes")

    # Draw line connecting points
    plt.plot(nodes, meantime, "r-", alpha=0.3)

    # Add labels and title
    plt.xlabel("Number of nodes")
    plt.ylabel(f"Meantime[{unit}]")
    plt.title(f"{session_name} mean time")

    # Show legend
    plt.legend()

    plt.savefig(save_path)


def plot_std_dev_nodes_number(session_name, nodes, std_dev, unit):

    current_datetime = datetime.now()
    filename = (
        session_name
        + "_"
        + "standard_deviation"
        + "_"
        + current_datetime.strftime("%Y-%m-%d_%H:%M:%S")
    )
    save_path = utils.escape_chars(
        f"{cfg['dbPath']}\{'images'}\{session_name}\{filename}"
    )

    plt.plot(
        nodes,
        std_dev,
        "o",
        label="Standard Deviation as functions of number of nodes",
    )

    # Draw line connecting points
    plt.plot(nodes, std_dev, "b-", alpha=0.3)

    plt.xlabel("Number of Nodes")
    plt.ylabel(f"Standard Deviation [{unit}]")
    plt.title(f"{session_name} standard deviation")

    plt.legend()

    plt.savefig(save_path)

    return save_path


def analyse_session(session_id, session_name):
    db_adapter.session_results.reset_session_results(session_id)

    session_batches = db_adapter.analysis.get_session_batches(session_id)
    number_of_nodes = [batch["number_of_nodes"] for batch in session_batches]
    meantimes = [batch["batch_mean_time"] for batch in session_batches]
    std_dev = [batch["batch_std_deviation"] for batch in session_batches]

    cmean_times, unit = convert_times(meantimes)
    cstd_dev, unit = convert_times(std_dev)

    meantimePlot = plot_meantime_nodes_number(
        session_name, number_of_nodes, cmean_times, unit
    )
    stddevPlot = plot_std_dev_nodes_number(
        session_name, number_of_nodes, cstd_dev, unit
    )

    db_adapter.session_results.insert_session_result(
        session_id, meantimePlot, stddevPlot
    )


def do_analysis(session_id, session_name):
    analyse_session_batches(session_id, session_name)
    analyse_session(session_id, session_name)

    batchesResultList = db_adapter.batch_results.get_batch_results_for_session
    sessionResults = db_adapter.session_results.get_session_result_paths

    return {"sessionResults": sessionResults, "batchesResultList": batchesResultList}
