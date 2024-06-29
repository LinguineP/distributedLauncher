import csv
import math
import os
import dbAdapter
import utils
from config import cfg
from datetime import datetime
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt


db_adapter = dbAdapter.SQLiteDBAdapter()


def generate_csv_from_combined_data():
    # data from all sessions or just from one?
    current_datetime = datetime.now()
    filename = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")
    filepathname = utils.escape_chars(f"{cfg['dbPath']}\{'csv'}\{filename}.csv")

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


def plot_times_with_stats(session_name: str, batch_param, times, unit, batchId):
    mean_time = calculate_mean_time(times)
    std_deviation = calculate_standard_deviation(times)

    current_datetime = datetime.now()
    filename = (
        session_name
        + "_"
        + str(batchId)
        + "_"
        + current_datetime.strftime("%Y-%m-%d_%H-%M-%S")
    )
    save_path = utils.escape_chars(
        f"{cfg['dbPath']}/images/{session_name}/batchresults/{filename}.png"
    )

    plt.figure(figsize=(10, 6))  # Adjust figure size if necessary
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

    plt.legend()
    plt.xlabel(f"Execution Time[{unit}]")
    plt.ylabel("Frequency")
    plt.title(
        f"Execution times distribution in session {session_name} with params {batch_param}",
        wrap=True,
    )

    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    plt.savefig(save_path, bbox_inches="tight")
    plt.clf()
    plt.close()

    return std_deviation, mean_time, save_path


def analyse_session_batches(session_id, session_name):
    db_adapter.batch_results.reset_batch_results_for_session(session_id)
    session_batches_data = db_adapter.analysis.get_session_batches_with_times(
        session_id
    )

    for batch in session_batches_data:
        times, unit = batch["batch_times"], "s"
        std_deviation, mean, graph_path = plot_times_with_stats(
            str(session_name), batch["param_used"], times, unit, batch["batch_id"]
        )
        db_adapter.batch_results.insert_batch_result(
            batch["batch_id"], std_deviation, mean, graph_path
        )


def plot_meantime_nodes_number(session_name, nodes, meantime, unit, batchId):
    current_datetime = datetime.now()
    filename = (
        session_name
        + "_"
        + "meantime"
        + "_"
        + current_datetime.strftime("%Y-%m-%d_%H-%M-%S")
    )
    save_path = utils.escape_chars(
        f"{cfg['dbPath']}/images/{session_name}/{filename}.png"
    )

    nodes = [int(node) for node in nodes]

    plt.figure(figsize=(10, 6))  # Adjust figure size if necessary
    plt.plot(nodes, meantime, "o", label="Mean time as functions of number of nodes")

    for i, txt in enumerate(batchId):
        plt.annotate(txt, (nodes[i], meantime[i]))

    plt.plot(nodes, meantime, "r-", alpha=0.3)

    plt.xlabel("Number of nodes")
    plt.ylabel(f"Meantime[{unit}]")
    plt.title(f"{session_name} mean time")

    plt.xticks(nodes)

    plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left")

    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    plt.savefig(save_path, bbox_inches="tight")

    plt.clf()
    plt.close()

    return save_path


def plot_std_dev_nodes_number(session_name, nodes, std_dev, unit, batchId):
    current_datetime = datetime.now()
    filename = (
        session_name
        + "_"
        + "standard_deviation"
        + "_"
        + current_datetime.strftime("%Y-%m-%d_%H-%M-%S")
    )
    save_path = utils.escape_chars(
        f"{cfg['dbPath']}/images/{session_name}/{filename}.png"
    )

    nodes = [int(node) for node in nodes]

    plt.figure(figsize=(10, 6))  # Adjust figure size if necessary
    plt.plot(nodes, std_dev, "o", label="Std Deviation")

    for i, txt in enumerate(batchId):
        plt.annotate(txt, (nodes[i], std_dev[i]))

    plt.plot(nodes, std_dev, "b-", alpha=0.3)

    plt.xlabel("Number of Nodes")
    plt.ylabel(f"Standard Deviation [{unit}]")
    plt.title(f"{session_name} standard deviation")

    plt.xticks(nodes)

    plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left")

    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    plt.savefig(save_path, bbox_inches="tight")

    plt.clf()
    plt.close()

    return save_path


def analyse_session(session_id, session_name):
    db_adapter.session_results.reset_session_results(session_id)

    session_batches = db_adapter.analysis.get_session_batches(session_id)
    batchId = [batch["batch_id"] for batch in session_batches]
    number_of_nodes = [int(batch["batch_number_of_nodes"]) for batch in session_batches]
    meantimes = [batch["batch_mean_time"] for batch in session_batches]
    std_dev = [batch["batch_std_deviation"] for batch in session_batches]

    cmean_times, unit = meantimes, "s"
    cstd_dev, unit = std_dev, "s"

    meantimePlot = plot_meantime_nodes_number(
        session_name, number_of_nodes, cmean_times, unit, batchId
    )
    stddevPlot = plot_std_dev_nodes_number(
        session_name, number_of_nodes, cstd_dev, unit, batchId
    )

    db_adapter.session_results.insert_session_result(
        session_id, meantimePlot, stddevPlot
    )


def do_analysis(session_id, session_name):
    analyse_session_batches(session_id, session_name)
    analyse_session(session_id, session_name)

    batchesResultList = db_adapter.batch_results.get_batch_results_for_session(
        session_id
    )
    sessionResults = db_adapter.session_results.get_session_result_paths(session_id)

    return {"sessionResults": sessionResults, "batchesResultList": batchesResultList}
