# Log Analysis

### Project Details

Udacity Full Stack Web Developer Nanodegree Project 3 - Update 19 May 18 - Mike Boyer - Boyer.Mike.E@gmail.com

Developed for Python 2.7 with Chrome, Firefox, Sublime Text, and [Reindent](https://pypi.org/project/Reindent/0.1.1/#description "Reindent")

The front-end was built using Udacity's Python forum in-class examples. This was great starter code to learn how to play with queries in PostgreSQL/psycopg2. I could've submitted this days ago, but implementing psycopg2 made it a lot more fun.

The objective of the project is to build an internal tool to analyze a newspaper site database. At a minimum the tool must answer the following questions:

1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time? 
3. On which days did more than 1% of requests lead to errors? 

### Requirements

* Vagrant (See instructions below)
* [VirtualBox](https://www.virtualbox.org/ "VirtualBox")

### Instructions:

1. To use, make sure you have Chrome or Firefox installed.
2. Retrieve from GitHub [here](https://github.com/mikboy018/fsnd-vagrant "Project on GitHub")
3. Setup Vagrant: [(instructions here)](https://classroom.udacity.com/nanodegrees/nd004/parts/8d3e23e1-9ab6-47eb-b4f3-d5dc7ef27bf0/modules/bc51d967-cb21-46f4-90ea-caf73439dc59/lessons/5475ecd6-cfdb-4418-85a2-f2583074c08d/concepts/14c72fe3-e3fe-4959-9c4b-467cf5b7c3a0 "Udacity Vagrant Instructions")
4. Download the newsdata [here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip "Udacity Newsdata for Log Analysis Project")
5. Move the newsdata file into the vagrant directory created in step 3
6. Open the command prompt, navigate to your vagrant directory, and enter `psql -d news -f newsdata.sql`
7. Log into Vagrant ( enter `vagrant up` next `vagrant ssh` then `cd /vagrant`)
8. Launch with `python newsdata.py`
9. Open your web browser, and navigate to Localhost:8000
10. Enter your desired value in the textbox, for the first two buttons (authors and articles) this number will limit the top articles/authors displayed to your specification. If you wish to query for a certain failure rate, enter a percent (no less than .00001).
   Example: Entering 2, and pressing the Authors/Articles buttons will display the top 2 Authors/Articles. Pressing the Failure Rate button will display errors greater than 2%.
11. Log data will be displayed below.

### Notes:
I added functionality to display performance. If you have any suggestions regarding how I can speed up the queries on multiple tables (30 sec on avg with an AMD Phenom II Black Edition / 8 GB Ram / Ubuntu 16.04).
