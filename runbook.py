from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_config
from nornir_netmiko.tasks import netmiko_send_command
from nornir_utils.plugins.functions import print_result
from nornir_jinja2.plugins.tasks import template_file
from nornir_utils.plugins.tasks.data import load_yaml


nr = InitNornir(config_file="config.yaml")
ios_devices = nr.filter(nr.host['platform']== 'ios')

def load_variables(task):
    data = task.run(task=load_yaml, file=f"variables/{ task.host }.yaml")
    task.host['hostvars'] = data.result
    random_config(task)


def random_config(task):
    template = task.run(task=template_file, template="config.j2",path=f"templates/{task.host.platform}/")
    task.host["ospf_config"] = template.result
    rendered = task.host["ospf_config"]
    configuration = rendered.splitlines()
    task.run(task=netmiko_send_config, config_commands=configuration)

    # command_list = [f"ntp server {task.host['ntp_server']}", "interface loopback0", f"ip address {task.host['loopback']} 255.255.255.255"]
    # task.run(task=netmiko_send_command, command_string= 'no username lauren')
    # task.run(task=netmiko_send_command, command_string= '\n',expect_string = r"('This operation will remove all username related configurations with same name.Do you want to continue? [confirm]')")

results = ios_devices.run(task=load_variables)
print_result(results)