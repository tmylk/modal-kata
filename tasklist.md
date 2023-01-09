# Task



## Task List

- [-] Done: read NYC Taxi rides for June 2022 and plot a simple graph of weekly rides

- [ ] Look at the graph returned. I expected it to show only June 2022, but it shows dates 2004 - 2024. Why is that? When plotting, we didn't specify any date ranges.
- [ ] Run the tests and see output with `pytest -s test_taxi.py`. What does it say?
- [ ] Let's explore the data in the database. Are all the entries from June 2022? Or are there some other dates? How many of them are there? Maybe we need to do data cleaning.
    - [ ] Change `get_data` annotation to make it interactive `@stub.function(interactive=True)`
    - [ ] Insert the drop into [interactive debugger](https://modal.com/docs/guide/developing-debugging) just before we return from `get_data` function
   ```python
   import IPython
    IPython.embed()
    ```
    - [ ] run `python taxi.py` in the terminal
    - [ ] what years are in the table?
      - spoiler solution to run in ipython: `con.df().d.apply(lambda x:x.year).value_counts()` 
    - once done with exploration, revert `@stub.function(interactive=False)`(needed so it returns value) and remove `ipython` call. 
- [ ] add a data cleaning in sql: only load entries that are from June 2022
- [ ] change the code to read all the files for 2018 - 2023. The file name is in the format yellow_tripdata_2022-06.parquet, yellow_tripdata_2022-07.parquet etc
  - [ ] pass the year and month in the `get_data` arguments
  - [ ] iterate through all months years with [`starmap`](https://modal.com/docs/reference/modal.Function#starmap) in `create_plot`