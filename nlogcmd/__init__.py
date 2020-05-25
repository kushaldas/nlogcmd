# Nginx log parser shell

import os
import pickle
from pprint import pprint
import datetime

import cmd2
from cmd2 import Cmd
from clfparser import CLFParser


def find_actual_url(data):
    "Find the actual URL value except any query data"
    data = data.strip('"')
    words = data.split()
    url = words[1].split("?")[0]
    return words[0], url, words[2]


def view_counter(work_data):
    "Show the views stat"
    msg = ""
    counter = {}
    for rec in work_data:
        words = find_actual_url(rec["r"])
        value = counter.get(words[1], 0)
        value += 1
        counter[words[1]] = value
    values = [(v, k) for k, v in counter.items()]
    values.sort(reverse=True)
    for v, k in values:
        msg += f"{cmd2.ansi.style(k, fg='blue')} : {cmd2.ansi.style(v, fg='green')}\n"
    return msg


class REPL(Cmd):
    prompt = "log> "
    intro = "Welcome to nginx log viewer"

    def __init__(self):
        Cmd.__init__(self)
        self.data = []
        self.work_data = []

    def do_load_from_file(self, line):
        print("Loading data from file.")
        with open("access.log") as fobj:
            for line in fobj:
                line = line.strip()
                parsed = CLFParser.logDict(line)
                self.data.append(parsed)

    def do_select(self, line):
        "Selects the kind of file we should search"
        line = line.strip()
        self.select_data(line)

    def do_views(self, line):
        "Shows the total views by sort order"
        msg = view_counter(self.work_data)
        self.ppaged(msg)

    def do_len(self, lines):
        "Shows data length"
        print(f"DATA = {len(self.data)} and work_data = {len(self.work_data)}")

    def do_msg(self, line):
        value = cmd2.ansi.style(line, fg="red") + " " + cmd2.ansi.style(line, fg="white")
        print(value)

    def select_data(self, line):
        "Selects given format into working data"
        default = {"format": "html", "status": "200"}
        for command in line.split():
            k, v = command.split("=")
            print(k, v)
            default[k.strip()] = v.strip()
        self.work_data = [
            rec
            for rec in self.data
            if rec["r"].find(".{}".format(default["format"])) != -1
            and rec["s"] == "{}".format(default["status"])
        ]
        # Now extra filter fields

        if "date" in default:
            value = default["date"]
            date_match = datetime.datetime.today()
            if value == "today":
                self.work_data = [rec for rec in self.work_data if rec["time"].date() == date_match.date()]
            elif value == "yesterday":
                date_match = date_match - datetime.timedelta(days=1)
                self.work_data = [rec for rec in self.work_data if rec["time"].date() == date_match.date()]



def main():
    app = REPL()
    app.cmdloop()
