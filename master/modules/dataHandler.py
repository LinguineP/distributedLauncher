import os
import dbAdapter
import utils
from config import cfg


db_adapter = dbAdapter.SQLiteDBAdapter()


data_passer: dbAdapter.SQLiteDBAdapter.DataPasser = (
    dbAdapter.SQLiteDBAdapter().dataPasser
)


def get_files(path):
    for file in os.listdir(path):
        if (
            os.path.isfile(os.path.join(path, file))
            and file.endswith(".py")
            and not file.startswith((".", "_"))
        ):
            yield file


data_passer: dbAdapter.SQLiteDBAdapter.DataPasser = (
    dbAdapter.SQLiteDBAdapter().dataPasser
)


def getAvailableScripts():
    scripts = (
        []
    )  # it is assumed that the the script names are consistent across nodes, there are no duplicate scripts and proper paths  to scripts are given in cfg
    for path in cfg["scriptPaths"]:
        scripts.extend(get_files(utils.escape_chars(path)))

    return scripts


def get_params_settings():
    return db_adapter.params.get_all_settings()


def insert_params_setting(param):
    newParam = param["value"]
    return db_adapter.params.insert_setting(newParam)


def update_param(item_id, data):
    updated_param = data["value"]
    return db_adapter.params.update_setting(item_id, updated_param)


def delete_param(item_id):
    return db_adapter.params.delete_setting(item_id)


def insert_session(param):
    return db_adapter.sessions.insert_session(
        param["sessionName"], param["sessionScript"]
    )


def get_all_sesisions():
    return db_adapter.sessions.get_all_sessions()


def get_session_results(session_id):
    return db_adapter.session_results.get_session_result_paths(session_id)


def get_session_batch_results(session_id):
    db_adapter.batch_results.get_batch_results_for_session(session_id)


def check_measurement_status_exists():
    return data_passer.exists("status")


def retrive_measurment_status():
    return data_passer.retrieve("status")


def check_measurement_repetition_number_exists():
    return data_passer.exists("repetitionNumber")


def retrive_repetition_number():
    return data_passer.retrieve("repetitionNumber")
