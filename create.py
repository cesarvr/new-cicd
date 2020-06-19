#!/bin/python

import subprocess
from os import listdir
import sys

def readTemplates(file, arguments):
    content = open(file, "r").read()
    for name in arguments.keys():
        content =  content.replace("%" + name + "%", arguments[name])
    return content

def parseBuildTemplate(path, arguments):
    try:
        templates = listdir(path)
        templates = map(lambda template: path + "/" + template, templates)
        return map(lambda template: readTemplates(template, arguments), templates)


        USAGE = "Usage: deploy.py param_name=<value1> param_name=<value2>"
        args = sys.argv[1:]

        if not args:
            sys.exit(USAGE)

        ap = [pair.split("=") for pair in args]
        ap = map(lambda n: (n[0], n[1]), ap)
        ret = dict(ap)
    except:
        return []

    return ret

def getUserArguments():
    USAGE = "Usage: deploy.py param_name=<value1> param_name=<value2>"
    args = sys.argv[1:]

    if not args:
        sys.exit(USAGE)

    ap = [pair.split("=") for pair in args]
    ap = map(lambda n: (n[0], n[1]), ap)
    ret = dict(ap)

    return ret


def buildComponents(parsedTemplates, arguments):
    ns = arguments['project']
    cmd = ["oc", "apply", "-n", ns, "-f", "-"]

    for template in parsedTemplates:
        ocProcess = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        ocProcess.communicate(template)
        ocProcess.wait()

def applyPatches(patchTemplates, arguments):
    name = arguments['name']
    ns   = arguments['project']

    for template in patchTemplates:
        cmd  = ["oc", "patch", "dc", name, "-n", ns, "--patch", template]
        oc_proc = subprocess.Popen(cmd,  stdin=subprocess.PIPE)
        oc_proc.wait()


## Entry Point
print "Creating.."
arguments = getUserArguments()
ocp_components = parseBuildTemplate("templates/ocp", arguments)
buildComponents(ocp_components, arguments)

print "Patching.."
patches = parseBuildTemplate("templates/patches", arguments)
applyPatches(patches, arguments)
