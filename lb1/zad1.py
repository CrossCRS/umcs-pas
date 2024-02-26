#!/usr/bin/env python

filename = input("Enter text file filename: ")

with open("lab1zad1.txt", "w") as file_write:
    with open(filename, "r") as file_read:
        file_write.write(file_read.read())
