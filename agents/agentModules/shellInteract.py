import subprocess
import threading
import queue
import sys
import os
import time
import agentConfig
import builtins


class ShellHandler:
    _venv_name = "venv_ptbfla"

    def __init__(self):
        self.process: subprocess.Popen = None
        self.shell_setup = False
        self.open_shell()

    def open_shell(self):
        """shell setup"""
        if not self.process:
            if sys.platform == "win32":
                command = "cmd.exe"
            else:
                command = "bash"
            self.process = subprocess.Popen(
                command,
                cwd=agentConfig.cfg["baseProjectPath"],
                shell=True,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                text=True,
            )
            self.shell_setup = True
            print("shellopen")

        self.__setup_venv()
        # print(self.process.communicate(cmd))

    def __setup_venv(self):
        """activates the venv"""
        # if venv hasn't been initialised
        if not os.path.exists(
            os.path.join(agentConfig.cfg["baseProjectPath"], self._venv_name)
        ):
            self.send_command(f"python -m venv {self._venv_name}")
            output = self.read_output(timeout=10)
            for line in output:
                print(line)
            if sys.platform == "win32":
                self.send_command("py -m pip install -e src")
            else:
                self.send_command("python3 -m pip install -e src")

        # venv activation
        if sys.platform == "win32":
            self.send_command(
                f"call {self._venv_name}\\Scripts\\activate"
            )  # For Windows
        else:
            self.send_command(f"source {self._venv_name}/bin/activate")  # For Linux
        print(f"venv activated: ({self._venv_name})")

    def send_command(self, command):
        """simulates command entered"""
        if self.process and self.shell_setup:
            try:
                print(command)
                self.process.stdin.write(command + "\n")
                self.process.stdin.flush()
                # self.process.stdout.flush()
            except Exception as e:
                print(f"Error sending command: {e}")

    def run_command(self, command):
        """runs command on an open shell and closes it while returning the output"""
        if sys.platform == "win32":
            command += "\r\n"  # needed for the windows command to pass
        output, error = self.process.communicate(command)
        self.close_shell()
        return output, error

    def close_shell(self):
        """
        Terminates the shell gracefully
        """
        if self.process:
            try:
                self.process.stdin.close()
                self.process.terminate()
                self.process.wait()
                self.process = None
                self.shell_setup = False
            except Exception as e:
                print(f"Error closing shell: {e}")
