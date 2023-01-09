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
        SELECT tpep_pickup_datetime::date d, COUNT(1) c
        FROM read_parquet(?)
        GROUP by d;
    """
    
    con.execute(q, parameters=[url])
    
    con.execute("SELECT * FROM daily_pickups")

    # import IPython
    # IPython.embed()
    # run in terminal:
    # my_df = con.df()
    # my_df.d.apply(lambda x:x.year).value_counts()

    l = list(con.fetchall())
    return l


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
    pyplot.legend()
    pyplot.tight_layout()

    # Dump PNG and return
    with io.BytesIO() as buf:
        pyplot.savefig(buf, format="png", dpi=300)
        return buf.getvalue()



OUTPUT_DIR = "/tmp/nyc"

if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    fn = os.path.join(OUTPUT_DIR, "nyc_taxi_chart.png")

    with stub.run():
        png_data = create_plot.call()
        with open(fn, "wb") as f:
            f.write(png_data)
        print(f"wrote output to {fn}")
