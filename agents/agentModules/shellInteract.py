import subprocess
import agentModules.agentConfig as agentConfig




class ShellHandler:

    def __new__(self): #singleton
        if not hasattr(self, 'instance'):
            self.instance = super(ShellHandler, self).__new__(self)
        return self.instance

    def __init__(self): #initialization of new instance
        self.process = None
        self.pythonCmd=''
        self.shell_setup=False
        self.open_shell('pwd')

    def open_shell(self, command):

        #todo figure this out how to make it work close to real time
        self.process = subprocess.Popen(command,cwd=agentConfig.cfg['baseProjectPath'], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

    def send_command(self, command):
        if self.process:
            self.process.stdin.write(command + '\n')
            


    def read_output(self):
        if self.process:
            while True:
                output = self.process.stdout.readline()
                if output == '' and self.process.poll() is not None:
                    break
                if output:
                    print(output.strip())

    def close_shell(self):
        if self.process:
            self.process.stdout.close()
            self.process.terminate()
            self.process = None