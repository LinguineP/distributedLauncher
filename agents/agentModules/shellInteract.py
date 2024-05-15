import subprocess
import threading
import queue
import sys
import os
import agentConfig


class ShellHandler:
    _instance = None
    _venv_name = "venv_ptbfla"

    # shell singleton
    def __new__(self):
        if self._instance is None:
            self._instance = super(ShellHandler, self).__new__(self)
        return self._instance

    def __init__(self):
        if not hasattr(self, "_initialized"):
            self.process = None
            self.shell_setup = False
            self.output_queue = queue.Queue()
            self.error_queue = queue.Queue()
            self.__open_shell()
            self._initialized = True

    def __open_shell(self):
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
                text=True,
            )
            self.shell_setup = True
            self.__start_session_IO()
            self.__setup_venv()
            print("shell setup and ready for use....")

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
            output = self.read_output(timeout=10)
            for line in output:
                print(line)
        # venv activation
        if sys.platform == "win32":
            self.send_command(f"{self._venv_name}\\Scripts\\activate")  # For Windows
        else:
            self.send_command(f"source {self._venv_name}/bin/activate")  # For Linux
        print(f"venv activated: ({self._venv_name})")

    def __start_session_IO(self):
        """starts output stream handling threads"""

        # stdout handling daemon
        self.output_thread = threading.Thread(
            target=self.__enqueue_output, args=(self.process.stdout, self.output_queue)
        )
        self.output_thread.daemon = True
        self.output_thread.start()

        # stderr handling daemon
        self.error_thread = threading.Thread(
            target=self.__enqueue_output, args=(self.process.stderr, self.error_queue)
        )
        self.error_thread.daemon = True
        self.error_thread.start()

    def __enqueue_output(self, out, queue):
        """enqueues lines from output streams"""
        try:
            for line in iter(out.readline, ""):
                queue.put(line)
        except Exception as e:
            print(f"Error reading stream: {e}")
        out.close()

    def send_command(self, command):
        """simulates command entered"""
        if self.process and self.shell_setup:
            try:
                self.process.stdin.write(command + "\n")
                self.process.stdin.flush()
            except Exception as e:
                print(f"Error sending command: {e}")

    def send_input(self, input_data):
        """simulates user input"""
        if self.process and self.shell_setup:
            try:
                self.process.stdin.write(input_data + "\n")
                self.process.stdin.flush()
            except Exception as e:
                print(f"Error sending input: {e}")

    def read_output(self, timeout=None):
        """Reads messages from the output queue until it is empty and then retuns them"""
        output = []
        try:
            while True:
                try:
                    line = self.output_queue.get(timeout=timeout)
                    output.append(line.strip())
                except queue.Empty:
                    break
        except Exception as e:
            print(f"Error reading output: {e}")
        return output

    def read_errors(self, timeout=None):
        """Reads messages from the error queue until it is empty and then retuns them"""
        errors = []
        try:
            while True:
                try:
                    line = self.error_queue.get(timeout=timeout)
                    errors.append(line.strip())
                except queue.Empty:
                    break
        except Exception as e:
            print(f"Error reading errors: {e}")
        return errors

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


# example usage and test for this module
"""
if __name__ == "__main__":
    shell_handler = ShellHandler()

    script_command = "python3 src/examples/hellow.py"
    shell_handler.send_command(script_command)

    shell_handler.send_input(" ")

    output = shell_handler.read_output(timeout=1)
    for line in output:
        print(line)

    errors = shell_handler.read_errors(timeout=1)
    for line in errors:
        print(line, file=sys.stderr)

    script_command = "python3 src/examples/hellow.py"
    shell_handler.send_command(script_command)

    shell_handler.send_input(" ")

    output = shell_handler.read_output(timeout=1)
    for line in output:
        print(line)

    errors = shell_handler.read_errors(timeout=1)
    for line in errors:
        print(line, file=sys.stderr)

    shell_handler.close_shell()
"""
