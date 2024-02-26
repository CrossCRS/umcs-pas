#!/usr/bin/env python

filename = input("Enter png file filename: ")

with open("lab1zad2.png", "wb") as file_write:
    with open(filename, "rb") as file_read:
        file_write.write(file_read.read())
