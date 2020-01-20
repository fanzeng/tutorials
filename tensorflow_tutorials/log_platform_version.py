import tensorflow as tf
import platform
import os

# get platform info and save it into a file
def log_platform_version():
    linux_version = ' '.join(platform.linux_distribution())
    python_version = platform.python_version()
    tensorflow_version = tf.__version__
    cuda_version = os.popen('/usr/local/cuda/bin//nvcc --version | grep -o "release.*$"').read().strip()
    cudnn_version = os.popen('grep -m 1 CUDNN_MAJOR -A 2 /usr/include/cudnn.h').read()
    cudnn_version = '.'.join([line.split(' ')[-1].strip() for line in cudnn_version.split('\n')[:-1]])
    with open("platform_version.txt", "w") as f:
        f.write('linux=' + linux_version + '\n')
        f.write('python=' + platform.python_version() + '\n')
        f.write('tensorflow=' + tensorflow_version + '\n')
        f.write('cuda=' + cuda_version + '\n')
        f.write('cudnn=' + cudnn_version + '\n')

    d_ver = {
        'linux_version': linux_version,
        'python_version': python_version,
        'tensorflow_version': tensorflow_version,
        'cuda_version': cuda_version,
        'cudnn_version': cudnn_version
    }
    return d_ver

def log_pip_list():
    with open("pip_list.txt", "w") as f:
        pip_list = os.popen('pip list').read().strip()
        f.write(pip_list)

if __name__ == '__main__':
    log_platform_version()
    log_pip_list()