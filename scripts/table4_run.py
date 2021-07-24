import os
import subprocess
import re
import time
from numpy import average 
from ExpStats import runExpWithName

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))

def parseThroughput(out):
    try:
        m = re.search(r'Requests/sec: ([0-9,.]+)', out)
        # m = re.search(r'([0-9,]+) ns/iter', out)
        s = m.group(1)
        result  = float(s.strip())
        #s = s.replace(',', '')
        #result = int(s)
    except Exception:
        print(out)
        print("Run experiment failed")
        return None

    return result

def parseZola(out):
    try:
        m = re.search(r'Done in ([0-9]+)ms.', out)
        # m = re.search(r'([0-9,]+) ns/iter', out)
        s = m.group(1)
        result  = float(s.strip())
        #s = s.replace(',', '')
        #result = int(s)
    except Exception:
        print(out)
        print("Run experiment failed")
        return None

    return result

def test_swc():
    print("Testing swc")
    safe_time, _, _ = runExpWithName("swc/test_bc-safe", None, 20, False)
    unsafe_time, _, _ = runExpWithName("swc/test_bc-unsafe", None, 20, False)
    perf_diff = (safe_time - unsafe_time) / unsafe_time
    print("Performance difference of swc is: {:2.2%}".format(perf_diff))

def test_warp():
    print("Testing warp")
    out = subprocess.Popen([ROOT_PATH + '/runWarp.sh', 'safe'],  stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out, _ = out.communicate()
    out = out.decode("utf-8")  # convert to string from bytes
    safe_throughput = parseThroughput(out)

    out = subprocess.Popen([ROOT_PATH + '/runWarp.sh', 'unsafe'],  stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out, _ = out.communicate()
    out = out.decode("utf-8")  # convert to string from bytes
    unsafe_throughput = parseThroughput(out)

    if safe_throughput and unsafe_throughput:
        perf_diff = (unsafe_throughput - safe_throughput) / unsafe_throughput 
        print("Performance difference of warp is: {:2.2%}".format(perf_diff))


def test_iron():
    print("Testing iron")
    out = subprocess.Popen([ROOT_PATH + '/runIron.sh', 'safe'],  stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out, _ = out.communicate()
    out = out.decode("utf-8")  # convert to string from bytes
    safe_throughput = parseThroughput(out)

    out = subprocess.Popen([ROOT_PATH + '/runIron.sh', 'unsafe'],  stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out, _ = out.communicate()
    out = out.decode("utf-8")  # convert to string from bytes
    unsafe_throughput = parseThroughput(out)

    if safe_throughput and unsafe_throughput:
        perf_diff = (unsafe_throughput - safe_throughput) / unsafe_throughput 
        print("Performance difference of iron is: {:2.2%}".format(perf_diff))


def test_zola():
    print("Testing zola")

    time_list = []
    for _ in range(100):
        out = subprocess.Popen([ROOT_PATH + '/runZola.sh', 'safe'],  stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        out, _ = out.communicate()
        out = out.decode("utf-8")  # convert to string from bytes
        time = parseZola(out)
        time_list.append(time)

    unsafe_time = average(time_list)

    time_list = []
    for _ in range(100):
        out = subprocess.Popen([ROOT_PATH + '/runZola.sh', 'safe'],  stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        out, _ = out.communicate()
        out = out.decode("utf-8")  # convert to string from bytes
        time = parseZola(out)
        time_list.append(time)
    safe_time = average(time_list)
    perf_diff = (safe_time - unsafe_time) / unsafe_time
    print("Performance difference of zola is: {:2.2%}".format(perf_diff))
    

def test_rustpython():
    arg = ROOT_PATH + "/../benchmarks/RustPython/benches/benchmarks/pystone.py"
    safe_time, _, _ = runExpWithName("RustPython/test_bc-safe", arg, 10, False)
    unsafe_time, _, _ = runExpWithName("RustPython/test_bc-unsafe", arg, 10, False)
    perf_diff = (safe_time - unsafe_time) / unsafe_time
    print("Performance difference of RustPython is: {:2.2%}".format(perf_diff))

os.chdir(ROOT_PATH + "/../benchmarks")
test_iron()
test_swc()
test_warp()
test_zola()
test_rustpython()
