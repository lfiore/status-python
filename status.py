#! /usr/bin/python3
import sys, os, socket, shutil, math

colours = {
	'red' : '\033[31m',
	'green' : '\033[32m',
	'yellow' : '\033[33m',
	'blue' : '\033[34m',
	'reset' : '\033[0m'
}

info = {
}
def main():

	# get server info
	info['server'] = {}

	# get host name
	info['server']['hostname'] = socket.gethostname()

	# get ip address
	info['server']['ip'] = socket.gethostbyname(info['server']['hostname'])

	# get uptime
	with open('/proc/uptime', 'r') as uptime_file:
		uptime = uptime_file.read()

		uptime_raw = float(uptime.split(' ')[0])

		info['server']['uptime_raw'] = uptime_raw

		info['server']['uptime_days'] = math.floor(uptime_raw / 86400)

		info['server']['uptime_hours'] = math.floor((uptime_raw / 3600) % 24)

		info['server']['uptime_minutes'] = math.floor((uptime_raw / 60) % 60)

		info['server']['uptime_seconds'] = math.floor(uptime_raw % 60)

	# get software info
	info['software'] = {}

	# get distro info
	# set distro to Unknown incase it's not found later
	info['software']['distro'] = 'Unknown'

	with open('/etc/os-release', 'r') as distro_file:
		distro_info = distro_file.read()

		for distro_line in distro_info.split('\n'):

			if 'PRETTY_NAME' in distro_line:
				info['software']['distro'] = distro_line.split('=')[1].strip('"')

				break

	# get kernel version
	info['software']['kernel'] = os.uname()[2]

	# get system type
	if os.uname()[4] == 'x86_64':
		info['software']['type'] = '64-bit (x64)'
	else:
		info['software']['type'] = '32-bit (x86)'

	# get cpu info
	info['cpu'] = {}

	# get cpu model name
	with open('/proc/cpuinfo', 'r') as cpuinfo_file:
		cpuinfo = cpuinfo_file.read()

		for cpuinfo_line in cpuinfo.split('\n'):

			if 'model name' in cpuinfo_line:
				cpuinfo_line = cpuinfo_line.split(':')

				info['cpu']['model'] = cpuinfo_line[1].strip()

	# get cpu load
	with open('/proc/loadavg', 'r') as cpuload_file:
		cpuload = cpuload_file.read().split(' ')

		info['cpu']['load1'] = cpuload[0]
		info['cpu']['load5'] = cpuload[1]
		info['cpu']['load15'] = cpuload[2]

	# get memory info
	info['memory'] = {}

	with open('/proc/meminfo', 'r') as meminfo_file:
		meminfo = meminfo_file.read()

		for meminfo_line in meminfo.split('\n'):

			# phsyical memory info
			if 'MemTotal' in meminfo_line:
				meminfo_line = meminfo_line.split(':')

				info['memory']['total'] = (int(meminfo_line[1].strip().split(' ')[0]) * 1024)

			elif 'MemFree' in meminfo_line:
				meminfo_line = meminfo_line.split(':')

				info['memory']['free'] = (int(meminfo_line[1].strip().split(' ')[0]) * 1024)

			elif 'Cached' in meminfo_line:
				meminfo_line = meminfo_line.split(':')

				info['memory']['cached'] = (int(meminfo_line[1].strip().split(' ')[0]) * 1024)

			# swap memory info
			elif 'SwapTotal' in meminfo_line:
				meminfo_line = meminfo_line.split(':')

				info['memory']['swap_total'] = (int(meminfo_line[1].strip().split(' ')[0]) * 1024)

			elif 'SwapFree' in meminfo_line:
				meminfo_line = meminfo_line.split(':')

				info['memory']['swap_free'] = (int(meminfo_line[1].strip().split(' ')[0]) * 1024)

	info['memory']['used'] = (info['memory']['total'] - (info['memory']['free'] + info['memory']['cached']))

	info['memory']['swap_used'] = (info['memory']['swap_total'] - info['memory']['swap_free'])

	# get disk info
	info['disk'] = {}

	info['disk']['total'], info['disk']['used'], info['disk']['free'] = shutil.disk_usage('/')

	# output system info
	print('\n' + ' ==== Server Info =============================================================' + '\n')

	print(' Hostname\t' + colours['blue'] + info['server']['hostname'] + colours['reset'])
	print(' IP Address\t' + colours['blue'] + info['server']['ip'] + colours['reset'])
	print(' Uptime\t\t' + colours['blue'] +
		str(info['server']['uptime_days']) + ' days, ' +
		str(info['server']['uptime_hours']) + ' hours, ' +
		str(info['server']['uptime_minutes']) + ' minutes and ' +
		str(info['server']['uptime_seconds']) + ' seconds' +
		colours['reset'])

	print('\n' + ' ==== Software Info ===========================================================' + '\n')

	print(' Distro\t\t' + colours['blue'] + info['software']['distro'] + colours['reset'])
	print(' Kernel\t\t' + colours['blue'] + info['software']['kernel'] + colours['reset'])
	print(' System Type\t' + colours['blue'] + info['software']['type'] + colours['reset'])

	print('\n' + ' ==== CPU Info ================================================================' + '\n')

	print(' Model\t\t' + colours['blue'] + info['cpu']['model'] + colours['reset'])
	print(' Load\t\t' + colours['blue'] + info['cpu']['load1'] + ', ' + info['cpu']['load5'] + ', ' + info['cpu']['load15'] + colours['reset'])

	print('\n' + ' ==== Memory Usage ============================================================' + '\n')

	# display memory usage as a bar
	# calculate colour of bar depending on usage
	if info['memory']['used'] >= (info['memory']['total'] * 0.8):
		ram_colour = 'red'

	elif info['memory']['used'] >= (info['memory']['total'] * 0.6):
		ram_colour = 'yellow'

	else:
		ram_colour = 'green'

	block_size = 35

	ram_block_size = math.floor(info['memory']['total'] / block_size)

	ram_used_blocks = math.floor(info['memory']['used'] / ram_block_size)

	ram_free_blocks = (block_size - ram_used_blocks)

	ram_bar =''
	ram_bar_free = ''

	for x in range(ram_used_blocks):
		ram_bar += '#'

	for y in range(ram_free_blocks):
		ram_bar_free += '-'

	if (info['memory']['total'] >= 1073741824):
		pretty_free_ram = str(round(info['memory']['used'] / 1073741824, 2))
		pretty_total_ram = str(round(info['memory']['total'] / 1073741824, 2))
		pretty_ram_symbol = 'G'
	else:
		pretty_free_ram = str(round(info['memory']['used'] / 1048576, 2))
		pretty_total_ram = str(round(info['memory']['total'] / 1048576, 2))
		pretty_ram_symbol = 'M'

	print(' RAM\t\t[' + colours[ram_colour] + ram_bar + colours['reset'] + ram_bar_free + '] (' + pretty_free_ram + ' / ' + pretty_total_ram + ' ' + pretty_ram_symbol + 'B' + ')')

	# display swap usage as a bar
	# calculate colour of bar depending on usage

	if info['memory']['swap_used'] >= (info['memory']['swap_total'] * 0.8):
		swap_colour = 'red'

	elif info['memory']['swap_used'] >= (info['memory']['swap_total'] * 0.6):
		swap_colour = 'yellow'

	else:
		swap_colour = 'green'

	swap_block_size = math.floor(info['memory']['swap_total'] / block_size)

	swap_used_blocks = math.floor(info['memory']['swap_used'] / swap_block_size)

	swap_free_blocks = (block_size - swap_used_blocks)

	swap_bar =''
	swap_bar_free = ''

	for x in range(swap_used_blocks):
		swap_bar += '#'

	for y in range(swap_free_blocks):
		swap_bar_free += '-'

	if (info['memory']['swap_total'] >= 1073741824):
		pretty_free_swap = str(round(info['memory']['swap_used'] / 1073741824, 2))
		pretty_total_swap = str(round(info['memory']['swap_total'] / 1073741824, 2))
		pretty_swap_symbol = 'G'
	else:
		pretty_free_swap = str(round(info['memory']['swap_used'] / 1048576, 2))
		pretty_total_swap = str(round(info['memory']['swap_total'] / 1048576, 2))
		pretty_swap_symbol = 'M'

	print(' Swap\t\t[' + colours[swap_colour] + swap_bar + colours['reset'] + swap_bar_free + '] (' + pretty_free_swap + ' / ' + pretty_total_swap + ' ' + pretty_swap_symbol + 'B' + ')')

	print('\n' + ' ==== Disk Usage ==============================================================' + '\n')

	# display disk usage as a bar
	# calculate colour of bar depending on usage

	if info['disk']['used'] >= (info['disk']['total'] * 0.8):
		disk_colour = 'red'

	elif info['disk']['used'] >= (info['disk']['total'] * 0.6):
		disk_colour = 'yellow'

	else:
		disk_colour = 'green'

	disk_block_size = math.floor(info['disk']['total'] / block_size)

	disk_used_blocks = math.floor(info['disk']['used'] / disk_block_size)

	disk_free_blocks = (block_size - disk_used_blocks)

	disk_bar =''
	disk_bar_free = ''

	for x in range(disk_used_blocks):
		disk_bar += '#'

	for y in range(disk_free_blocks):
		disk_bar_free += '-'

	if (info['disk']['total'] >= 1099511627776):
		pretty_free_swap = str(round(info['disk']['used'] / 1099511627776, 2))
		pretty_total_swap = str(round(info['disk']['total'] / 1099511627776, 2))
		pretty_disk_symbol = 'T'
	else:
		pretty_free_swap = str(round(info['disk']['used'] / 1073741824, 2))
		pretty_total_swap = str(round(info['disk']['total'] / 1073741824, 2))
		pretty_disk_symbol = 'G'

	print(' Disk\t\t[' + colours[disk_colour] + disk_bar + colours['reset'] + disk_bar_free + '] (' + pretty_free_swap + ' / ' + pretty_total_swap + ' ' + pretty_disk_symbol + 'B' + ')')

	print(colours['reset'])

if __name__ == '__main__':
	main()