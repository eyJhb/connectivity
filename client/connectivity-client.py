import subprocess
import json
import time
import sys

class connectivity_client(object):
    def __init__(self, config_file):
        # config
        self.config = json.loads(self.read_file(config_file))

        # last run
        self.last_run = 0

        # cmd
        self.cmd_iperf3 = "iperf3 -c {0} -p {1} -B {2} -J -t {3}"
        self.cmd_iperf3_re = "iperf3 -c {0} -p {1} -B {2} -J -t {3} -R"
        self.cmd_curl = 'curl -d "name={0}&date={1}&sent_value={2}&recv_value={3}" -X POST '+self.config['api_url']+'/api/add_reading'
        self.cmd_addr_linux = "ifconfig {0} | perl -n -e'/inet addr:([0-9\.]+)/ && print $1'"
        self.cmd_addr_unix = "ifconfig {0} | perl -n -e'/inet ([0-9\.]+)/ && print $1'"

    def read_file(self, filename):
        f = open(filename)
        data = f.read()
        f.close()
        return data

    def exec_cmd(self, cmd):
        cmd = "timeout "+str(self.config['timeout'])+" "+cmd
        print("Running - "+cmd)
        try:
            result = subprocess.check_output(cmd, shell=True).strip()
        except:
            return False

        return result

    def get_ip(self, interface):
        ip = self.exec_cmd(self.cmd_addr_linux.format(interface))
        if not ip:
            ip = self.exec_cmd(self.cmd_addr_unix.format(interface))

        return ip

    def run_test(self, interface):
        #get ip
        bind_ip = self.get_ip(interface)

        server = self.config['iperf_server']

        for port in self.config['iperf_ports']:
            cmd = self.cmd_iperf3.format(server, port, bind_ip, self.config['test_time'])
            cmd = self.exec_cmd(cmd)

            if cmd:
                break
            elif "error - the server is busy":
                continue
            else:
                return False

        if not cmd:
            return False

        res = json.loads(cmd)

        sent_value = (res['end']['sum_sent']['bytes']*8.0)/res['end']['sum_sent']['seconds']
        recv_value = (res['end']['sum_received']['bytes']*8.0)/res['end']['sum_received']['seconds']

        return [sent_value, recv_value]

    def send_reading(self, name, sent_value, recv_value, date = False):
        if not date:
            date = time.strftime("%Y-%m-%d %H:%M:%S")

        cmd = self.exec_cmd(self.cmd_curl.format(name, date, sent_value, recv_value))

        try:
            res = json.loads(cmd)
        except:
            return False

        if not res['success']:
            print(res)
            return False

        return True

    def main(self):
        while True:
            time.sleep(1)
            if (int(time.time())-self.last_run) > self.config['interval']:
                for interface in self.config['interfaces']:
                    print("Running for interface - "+interface['name'])
                    result = self.run_test(interface['if'])
                    if not result:
                        print("Could not run test..")
                        result = [0.0, 0.0]

                    if not self.send_reading(interface['name'], result[0], result[1]):
                        print("Could not send data to backend..")
                    print("Success")
                self.last_run = int(time.time())

#get arguments
args = sys.argv

if len(args) != 2:
    print("python connectivity-client.py config.json")
    exit()

config_file = args[1]

x = connectivity_client(config_file)
x.main()

