import json
from netmiko import ConnectHandler

with open('blacklist.txt') as f:
	ips = [line.strip() for line in f]

with open('devices.json', 'r') as f:
	devices = json.load(f)
	
	for device in devices:
		print("Connecting to device IP: {0}".format(device["ip"]))
		ssh = ConnectHandler(**device)

		for ip in ips:
			output = ssh.send_command("show firewall name FROM-OUTSIDE-TO-DMZ")
	
			if ip in output:
				print("IP address {0} already exists in firewall rules".format(ip))
				continue
	

			high_rule = 0
			for line in output.split('\n'):
				try:
					value = int(line.split(' ')[0])
				except:
					continue
				if isinstance(value, int) and value > high_rule and value != 10000:
					high_rule = int(value)

			high_rule += 10
	
			commands = [
				"set firewall name FROM-OUTSIDE-TO-DMZ rule {0} description 'Block traffic for ip address {1}'".format(high_rule,ip),
				"set firewall name FROM-OUTSIDE-TO-DMZ rule {0} action drop".format(high_rule),
				"set firewall name FROM-OUTSIDE-TO-DMZ rule {0} protocol all".format(high_rule),
				"set firewall name FROM-OUTSIDE-TO-DMZ rule {0} source address {1}".format(high_rule,ip)
			]

			output = ssh.send_config_set(commands, exit_config_mode=False)
			print(output)
	
			output = ssh.commit()
			print(output)
	
			output = ssh.save_config()
			print(output)
	
			output = ssh.exit_config_mode()
			print(output)

		ssh.disconnect()