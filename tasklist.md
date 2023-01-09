# Spec

Plot number of rides per day in NYC taxis 2018-2023

## Gitpod setup for modal

- Run `modal token new`
- Press `Q` to exit Lynx browser
- Manually go to the linnk in your browser to get the token
- See this output
  ```
  Success!
    Verifying token against https://api.modal.com
    Token verified successfully
    Token written to /home/gitpod/.modal.toml
    ```

## Task List

- [-] Done: read NYC Taxi rides for June 2022 and plot a simple graph of weekly rides
- [ ] START HERE: run the code in Modal with `python taxi.py` command
- [ ] Look at the png graph returned. I expected it to show only June 2022, but it shows dates 2004 - 2024. Why is that? When plotting, we didn't specify any date ranges.
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
- [ ] Make the month and year a parameter
  - [ ] let `get_data` take the year and month in the  arguments
  - [ ] check all the old tests are working
  - [ ] create a new test that reads July 2021 and check we get the right month and year back from `get_data`. 
  - [ ] make it pass.
  
- [ ] Read all the month files for 2018-2021. The file name is in the format yellow_tripdata_2021-06.parquet, yellow_tripdata_2021-07.parquet etc
  - [ ] create a new function  'get_all_years' and test that we have 4 years returned 
  - [ ] create a list of tuples (month, year) for 2018-2022 in 'get_all_years'
  - [ ] call `get_data` for each month with [`starmap`](https://modal.com/docs/reference/modal.Function#starmap) in `get_all_years` 
  - [ ] how is the runtime change? do the months get fetched sequentially or in parallel?
  - [ ] In `create_plot` use 'get_all_years' instead of 'get_data'
  - [ ] see the big new plot `png`


