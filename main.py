from sys import argv
from os import listdir
from os.path import join, dirname, splitext, isdir
from json import loads, dumps

path = dirname(__file__)
blacklist = open(join(path, "blacklist.csv"), "r").read().strip("\r\n").split("\n")
original = open(join(path, "original.csv"), "r").read().strip("\r\n").split("\n")
for i in range(len(original)):
    original[i] = loads(original[i])
replacement = open(join(path, "replacement.csv"), "r").read().strip("\r\n").split("\n")
for i in range(len(replacement)):
    replacement[i] = loads(replacement[i])
multiplication = open(join(path, "multiplication.csv"), "r").read().strip("\r\n").split("\n")


def handle(dname, fname):
    if splitext(fname)[1] == ".json":
        fd = loads(open(join(dname, fname), "r").read())
        if fname in multiplication:
            fd["result"]["count"] = 4
        if fname not in blacklist:
            if "key" in fd:
                for i in fd["key"]:
                    for j in range(min(len(original), len(replacement))):
                        if fd["key"][i] == original[j]:
                            fd["key"][i] = replacement[j]
            elif "ingredients" in fd:
                for i in range(len(fd["ingredients"])):
                    for j in range(min(len(original), len(replacement))):
                        if fd["ingredients"][i] == original[j]:
                            fd["ingredients"][i] = replacement[j]
        fl = open(join(dname, fname), "w")
        fl.write(dumps(fd, indent=2))
        fl.close()


def dealpath(dname, act):
    for i in listdir(dname):
        if isdir(join(dname, i)):
            dealpath(join(dname, i), act or i == "recipes")
        elif act:
            handle(dname, i)


dealpath(argv[1], False)
