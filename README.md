Small command line tool to view statistics from nginx `access.log` file.
Remember that the tool keeps the data on memory when it is running. It is better
that you use this on a different system than your actual server.


The log file should be in the same directory.

## How to use?

First create a virtualenv and install the dependencies.

```
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt
```

Then open the tool's shell.

```
python3 ./run.py
```

First load all the data.

```
✦ ❯ python3 ./run.py 
Welcome to nginx log viewer
log> load_from_file 
Loading data from file.
```

It will take a few seconds to load the data from the disk.

Then you use select statement to filter the data, and `views` to view the statistics.

`select format=html status=200`, this is the default command when you use just `select`.

You can also choose to view today's numbers.

```
select date=today
```

Or yesterday's numbers.

```
select date=yesterday
```

You can use these in combination.

```
select format=php date=yesterday
```

You can also use `from` and `till` to choose a date range. Dates must be given
in the format of `year-month-day`, example `2020-05-01`. If you mention only
the `from`, then it counts till today.

```
select from=2020-04-01 till=2020-04-30
```

