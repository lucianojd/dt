# `dt` (Data Transformer)

# History

I was trying to track my personal finances when I realized how tedious it was to manually enter each line item into a spreadsheet. I could export my financial statements as CSV file, but each financial institution had their own structure for the document and data. I created `dt` to be a reliable application for converting one CSV schema and the entries in the file into a standardized schema.

# Purpose

The purpose of `dt` is to be an accessible, free, and one stop shop for tracking all of your finances.It is also intended to be private. The application runs locally to ensure no data needs to leave your machine. It should ultimately be able to produce any graphs, charts, or documents necessary to fully understand your income and expenses.

# Introduction

A brief description of the application's use cases are given here, but for a more detailed outlined see `docs/applications.md`.

There are two methods for interacting with the application:

1. `cli.py`
2. `gui.py`

Each interface is intended to have the same functionality. The only difference is the mechanism the user wishes to use when managing their documents. To see what has been completed and what has yet to be completed see `docs/to-do.md`.

## CLI

`cli.py` is broken up into several applications:

* `config` with `add`, `info`, `list`, and `delete` methods for managing configurations.
* `transform` for appling the selected configuration to the specified files.

## GUI

`gui.py` is not yet functional.