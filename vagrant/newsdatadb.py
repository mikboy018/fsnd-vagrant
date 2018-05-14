# "Database code" for the DB Forum modified to suit the needs of the project.

import datetime
import psycopg2
import bleach

from string import capwords

POSTS = [("Welcome!", datetime.datetime.now())]

DBNAME = "news"

def get_posts():
  """Return all posts from the 'database', most recent first."""
  return reversed(POSTS)

def add_post(content):
  """Add a post to the 'database' with the current timestamp."""
  POSTS.append((content, datetime.datetime.now()))

def most_popular_articles(number):
  # verify input
  num = check_num(number)
  # mark start time
  start = datetime.datetime.now()
  # setup db connect
  db = psycopg2.connect(database=DBNAME)
  # create a cursor
  c = db.cursor()
  # select statement
  c.execute("select path, title, count(status) as numViews, articles.slug from log, articles where concat('/article/', articles.slug) ilike log.path group by path, slug, title order by numViews desc limit %s;" %(str(num),))
  # mark time query completed
  query_complete = datetime.datetime.now()
  # store answer to query
  #https://stackoverflow.com/questions/10252247/how-do-i-get-a-list-of-column-names-from-a-psycopg2-cursor
  column_names = [desc[0] for desc in c.description]
  contents = "Most popular " + str(num) + " articles (Title / Number of Views) <br />" 
  for row in c:
    article_name = str(row[1])
    # https://docs.python.org/2/library/string.html#string.capwords
    article_name = capwords(article_name)
    view_count = row[2]
    # https://mkaz.blog/code/python-string-format-cookbook/
    contents = contents + article_name + " / " + str("{:,}".format(view_count)) + "<br />"
  #contents = "Most popular articles: " + str(c.fetchall())+ " with " + str(c.fetchall()) + " reads!"
  # mark time complete
  stop = datetime.datetime.now()
  # append to posts, with runtime info
  contents = contents + "Query Duration: " + str(query_complete - start) + "<br />"
  contents = contents + "Python Duration: " + str(stop - query_complete) + "<br />"
  contents = contents + "Total Runtime: " + str(stop - start) + "<br />"
  POSTS.append((contents, datetime.datetime.now()))
  # make notice in the log
  # close cursor
  db.close()

def most_popular_author(number):
  # verify input
  num = check_num(number)
  # mark time start
  start = datetime.datetime.now()
  # setup db connection
  db = psycopg2.connect(database=DBNAME)
  # create a cursor
  c = db.cursor()
  # select statement
  c.execute("select path, count(status) as numViews, articles.slug, articles.author, authors.id, authors.name from log, articles, authors where concat('/article/', articles.slug) ilike log.path and authors.id = articles.author group by authors.id, articles.author, authors.name, log.path, articles.slug order by numViews desc limit %s;", (num,))
  # mark time query completed
  query_complete = datetime.datetime.now()
  # store answer to query
  contents = "The most popular " + str(num) + " authors (Name / Number of Views): <br />"
  for row in c:
    author_name = str(row[5])
    view_count = row[1]
    contents = contents + author_name + " / " + str("{:,}".format(view_count)) + "<br />"
  # mark time complete
  stop = datetime.datetime.now()
  # append to posts, with runtime info
  contents = contents + "Query Duration: " + str(query_complete - start) + "<br />"
  contents = contents + "Python Duration: " + str(stop - query_complete) + "<br />"
  contents = contents + "Total Runtime: " + str(stop - start) + "<br />"
  POSTS.append((contents, datetime.datetime.now()))
  # close cursor
  db.close()

def check_failure_rate(min_rate):
  # verify input
  min_rate = check_num(min_rate)
  # mark time start
  start = datetime.datetime.now()
  # setup db connection
  db = psycopg2.connect(database=DBNAME)
  # create a cursor
  c = db.cursor()
  # select statement
  c.execute("select to_char(time, 'MM/DD/YYYY') as day, (select cast(count(status) filter (where status != '200 OK') as float) / cast(count(status) as float)*100) as failRate from log group by day order by failRate desc;")
  # mark time query completed
  query_complete = datetime.datetime.now()
  # store answer to query
  contents = "Days with a failure rate >= " + str(min_rate) + " percent (Day / Percent): <br />" 
  for row in c:
    if row[1] >= (min_rate):
      day = str(row[0])
      rate = str(row[1])
      contents = contents + day + " / " + rate + "<br />"
    else:
      contents = contents
  # mark time complete
  stop = datetime.datetime.now()
  # append to posts, with runtime info
  contents = contents + "Query Duration: " + str(query_complete - start) + "<br />"
  contents = contents + "Python Duration: " + str(stop - query_complete) + "<br />"
  contents = contents + "Total Runtime: " + str(stop - start) + "<br />"
  POSTS.append((contents, datetime.datetime.now()))
  # make notice in the log
  print("Errors > " + str(min_rate) + " percent retrieved!")
  # close cursor
  db.close()

def check_num(number):
  # performs input validation, if no number assigned, passes in default value (1)
  # a very special thanks to: http://www.pythonforbeginners.com/error-handling/exception-handling-in-python
  try:
    num = int(number)
    if num < 1:
      num = 1;
  except ValueError:
    num = 1
  return num;





