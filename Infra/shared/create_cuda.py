#/usr/bin/env python

from yaml import load, dump
import os, sys, re
import subprocess

nv_device = '/dev/nvidia'
uvm_device = '{0}-uvm'.format(nv_device)
ctl_device = '{0}ctl'.format(nv_device)

cuda_version_label = 'com.nvidia.cuda.version'

nv_bins_volume = '/usr/local/bin'

nv_bins = ['nvidia-cuda-mps-control',
         'nvidia-cuda-mps-server',
         'nvidia-debugdump',
         'nvidia-persistenced',
         'nvidia-smi'
         ]

nv_libs_volume = '/usr/local/nvidia'
nv_libs_cuda = ['cuda', 'nvcuvid', 'nvidia-compiler', 'nvidia-encode', 'nvidia-ml']

def no_error(cmds):
	try:
		for cmd in cmds.split():
			subprocess.check_call([cmd], stdout=None, stderr=None)
	except subprocess.CalledProcessError:
		return False

def grep(cmd, grp):
	grep = subprocess.Popen(['grep', grp], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
	orig = subprocess.Popen(cmd, stdout=grep.stdin)
	output = grep.communicate()[0]
	orig.wait()
	return output

def query_nvsmi(section, gpu_id=False):
	cmd = ['nvidia-smi','-q']
	if gpu_id:
		cmd.extend(['-i', gpu_id])

	res = grep(cmd, section)
	return res.split()[-1]

def library_path(lib):
	pat = grep(['ldconfig', '-p'], 'lib{0}.so'.format(lib))
	if pat:
		return pat.split('=>')[-1].strip(' \t\n\r')
	else:
		print('Could not find library: {0}'.format(lib))

def library_arch(lib):
	proc = subprocess.Popen(['file', '-L', lib], stdout=subprocess.PIPE)
	out, errs = proc.communicate()

	if errs:
		print('There was an error with `which {0}`: {1}'.format(b, errs))
	elif out:
		return re.sub('-bit', '', out.split()[2])

def which(b):
	proc = subprocess.Popen(['which', b], stdout=subprocess.PIPE)
	out, errs = proc.communicate()
	if errs:
		print('There was an error with `which {0}`: {1}'.format(b, errs))
	elif out:
		return out.strip(' \n\t\r')


def format_mount(a, b=None):
	if not b:
		b = a
	return '{0}:{1}'.format(a, b)

driver_version = query_nvsmi('Driver Version')
no_error('nvidia-smi nvidia-modprobe')

gpus = sys.argv[1:]

d = {
	'devices': [],
	'volumes': []
}

## Add devices
devices = [uvm_device, ctl_device]
d['devices'] = [format_mount(dev) for dev in devices]

for gpu in gpus:
	gpu_minor_version = query_nvsmi('Minor Number', gpu)
	if gpu_minor_version:
		d['devices'].append(format_mount('{0}{1}'.format(nv_device, gpu_minor_version)))
	else:
		print('Could not find minor version for gpu: {0}'.format(gpu))

library_paths = [library_path(lib) for lib in nv_libs_cuda]

for lib in library_paths:
	basename = os.path.basename(lib)
	arch = library_arch(lib)
	if arch:
		mount = None
		if arch == '32':
			mount = format_mount(lib, '{0}/lib/{1}'.format(nv_libs_volume, basename))
		if arch == '64':
			mount = format_mount(lib, '{0}/lib64/{1}'.format(nv_libs_volume, basename))
		if mount:
			d['volumes'].append(mount)

for binary in nv_bins:
	b = which(binary)
	if b:
		d['volumes'].append(format_mount(b, '{0}/{1}'.format(nv_bins_volume, binary)))

out = dump(d,
	indent=4,
	default_flow_style=False
).replace('- ', '  - ')

print out