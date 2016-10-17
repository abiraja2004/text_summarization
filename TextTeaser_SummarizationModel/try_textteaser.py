#!/usr/bin/python
# -*- coding: utf-8 -*-

from textteaser import TextTeaser

model = TextTeaser()

file = open('C:/Users/Ksenia/Desktop/summary_examples/example1.txt', 'r')

# file should consist of two lines:
# 1 - title of the article
# 2 - the full text
lines = [line.strip() for line in file]
title = lines[0]
text = lines[1]

summary = model.summarize(title, text)

for line in summary:
  print(line)
