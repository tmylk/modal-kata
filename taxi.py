# # Use DuckDB to analyze lots of datasets in parallel
#
# The Taxi and Limousine Commission of NYC posts
# [datasets](https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page)
# with all trips in New York City.
# They are all Parquet files, which are very well suited for
# [DuckDB](https://duckdb.org/) which has excellent
# [Parquet support](https://duckdb.org/docs/data/parquet).
# In fact, DuckDB lets us query remote Parquet data
# [over HTTP](https://duckdb.org/docs/guides/import/http_import)
# which is excellent for what we want to do here.
#
# Running this script should generate a plot like this in just 10-20 seconds,
# processing a few gigabytes of data:
#
#
# ## Basic setup
#
# We need various imports and to define an image with DuckDB installed:
#
# CREDIT: This is a tiny bit simplified version of [modal-examples](https://github.com/modal-labs/modal-examples/blob/main/10_integrations/duckdb_nyc_taxi.py)

import io
import os
from datetime import datetime

import modal

stub = modal.Stub(
    "taxi-data-kata",
    image=modal.Image.debian_slim().pip_install("matplotlib", "duckdb", "pandas", "sqlalchemy"),
)

# ## DuckDB Modal function
#
# Defining the function that queries the data.
# This lets us run a SQL query against a remote Parquet file over HTTP
# Our query is pretty simple: it just aggregates total count numbers by date,


@stub.function(interactive=False)
def get_data():
    url = f"https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2022-06.parquet"

    import duckdb
    print("processing", url, "...")

    con = duckdb.connect(database=":memory:")
    con.execute("install httpfs") 
    con.execute("load httpfs")
    q = """
        CREATE TABLE daily_pickups AS
        SELECT 
            tpep_pickup_datetime::date d,
            COUNT(1) c
        FROM read_parquet(?)
        GROUP by d;
    """
    
    con.execute(q, parameters=[url])
    
    con.execute("SELECT * FROM daily_pickups")

    # import IPython
    # IPython.embed()
    # run in ipython:
    # my_df = con.df()
    # my_df.d.apply(lambda x:x.year).value_counts()

    l = list(con.fetchall())
    return l

# ## Plot results
#
# Let's define a separate function which:
# 1. Parallelizes over all files and dispatches calls to the previous function
# 2. Aggregate the data and plot the result


@stub.function
def create_plot():
    from matplotlib import pyplot

    data = get_data.call()

    # Initialize plotting
    pyplot.style.use("ggplot")
    pyplot.figure(figsize=(16, 9))

    # For each weekday, plot

    data.sort()
    dates = [d for d, _ in data]
    counts = [c for _, c in data]
    pyplot.plot(dates, counts, linewidth=3, alpha=0.8)

    # Plot annotations
    pyplot.title("Number of NYC yellow taxi trips daily, 2018-2022")
    pyplot.ylabel("Number of daily trips")
    
    pyplot.tight_layout()

    # Dump PNG and return
    with io.BytesIO() as buf:
        pyplot.savefig(buf, format="png", dpi=300)
        return buf.getvalue()


# ## Entrypoint
#
# Finally, we have some simple entrypoint code that kicks everything off.
# Note that the plotting function returns raw PNG data that we store locally.


OUTPUT_DIR = "/tmp/nyc"

if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    fn = os.path.join(OUTPUT_DIR, "nyc_taxi_chart.png")

    with stub.run():
        png_data = create_plot.call()
        with open(fn, "wb") as f:
            f.write(png_data)
        print(f"wrote output to {fn}")
