#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""IS211_Assignment11"""

import json
import os
import re

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


class Item:
    cnt = 1

    def __init__(self, task_name, email, priority):
        self.task_name = task_name
        self.email = email
        self.priority = priority
        self.id = Item.cnt + 1
        Item.cnt += 1


items = []


@app.route('/', methods=["POST", "GET"])
def index():
    global items
    return render_template("index.html", items=items)


@app.route('/submit', methods=["POST"])
def submit():
    task_name = request.form['task']
    email = request.form['email']
    priority = request.form['priority']

    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'

    if re.search(regex, email) and priority in ["Low", "Medium", "High"]:
        current_data = Item(task_name, email, priority)
        items.append(current_data)
        return redirect('/')
    else:
        return redirect('/')


@app.route('/clear', methods=["POST", "GET"])
def clear():
    global items
    items = []
    return redirect('/')


@app.route('/delete/<int:id>')
def delete(id):
    global items
    for i in range(0, len(items)):
        item = items[i]
        if item.id == id:
            items.pop(i)
            break
    return redirect('/')


@app.route('/save', methods=["POST", "GET"])
def save():
    global items
    file = open("saveItems.txt", "w")
    for item in items:
        file.write(item.task_name + "," + item.email + "," + item.priority + "\n")

    file.close()

    return redirect('/')


if __name__ == '__main__':

    """Read saved item"""
    if os.path.isfile("saveItems.txt"):
        with open("saveItems.txt", "r") as file:
            for line in file:
                line = line.strip().split(',')
                task_name = line[0]
                email = line[1]
                priority = line[2]
                item = Item(task_name, email, priority)
                items.append(item)

    app.run()
