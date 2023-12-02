from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_configure
from nornir_netmiko.tasks import netmiko_send_config
from nornir_netmiko.tasks import netmiko_send_command
from nornir_utils.plugins.functions import print_result
from nornir_jinja2.plugins.tasks import template_file
from nornir_utils.plugins.tasks.data import load_yaml
import logging

nr = InitNornir(config_file="config.yaml",dry_run= True )


def load_variables(task):
    data = task.run(task=load_yaml, file=f"variables/{ task.host }.yaml")
    task.host['hostvars'] = data.result
    random_config(task)


def random_config(task):
    template = task.run(task=template_file, template="config.j2",path=f"templates/{task.host['layer']}/")
    task.host["run_config"] = template.result
    #print(template.result)
    #rendered = task.host["run_config"]
    #configuration = rendered.splitlines()
    run_result = task.run(task=napalm_configure,
                        name="Loading Configuration on the device",
                        dry_run=False,
                        replace=False,
                        configuration=task.host["run_config"],
                        severity_level=logging.INFO)
    print_result(run_result)

 
results = nr.run(task=load_variables)
#print_result(results)
