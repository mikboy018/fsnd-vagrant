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
  column_names = []
  # verify input
  num = check_num(number)
  # setup db connect
  db = psycopg2.connect(database=DBNAME)
  # create a cursor
  c = db.cursor()
  # select statement
  c.execute("select path, count(status) as numViews, articles.slug from log, articles where concat('/article/', articles.slug) ilike log.path group by path, slug order by numViews desc limit %s;" %(str(num),))
  # store answer to query
  #https://stackoverflow.com/questions/10252247/how-do-i-get-a-list-of-column-names-from-a-psycopg2-cursor
  column_names = [desc[0] for desc in c.description]
  contents = "Most popular " + str(num) + " articles: <br />"
  contents = contents + "Title " + " / " + " Number of Views" + "<br />" 
  for row in c:
    # https://www.tutorialspoint.com/python/string_replace.htm
    article_name = str(row[2])
    article_name = article_name.replace("-", " ")
    # https://docs.python.org/2/library/string.html#string.capwords
    article_name = capwords(article_name)
    view_count = row[1]
    # https://mkaz.blog/code/python-string-format-cookbook/
    contents = contents + article_name + " / " + str("{:,}".format(view_count)) + "<br />"
  #contents = "Most popular articles: " + str(c.fetchall())+ " with " + str(c.fetchall()) + " reads!"
  # append to posts
  POSTS.append((contents, datetime.datetime.now()))
  # close cursor
  db.close()

def most_popular_author(number):
  # verify input
  number = check_num(number)
  # setup db connection
  db = psycopg2.connect(database=DBNAME)
  # create a cursor
  c = db.cursor()
  # select statement
  c.execute("select path, count(status) as numViews, articles.slug, articles.author, authors.id, authors.name from log, articles, authors where concat('/article/', articles.slug) ilike log.path and authors.id = articles.author group by authors.id, articles.author, authors.name, log.path, articles.slug order by numViews desc limit %s;", (num,))
  # store answer to query
  contents = "The most popular " + num + " authors: " + str(c.fetchall())
  # append to posts
  POSTS.append((contents, datetime.datetime.now()))
  # close cursor
  db.close()

def check_failure_rate(min_rate):
  # verify input
  min_rate = check_num(min_rate)
  # setup db connection
  db = psycopg2.connect(database=DBNAME)
  # create a cursor
  c = db.cursor()
  # select statement
  c.execute("select to_char(time, 'MM/DD/YYYY') as day, (select cast(count(status) filter (where status != '200 OK') as float) / cast(count(status) as float)*100) as failRate from log group by day order by failRate desc;")
  # store answer to query
  contents = "Days with a failure rate >= " + min_rate + " percent: " + str(c.fetchall())
  # append to posts
  POSTS.append((contents, datetime.datetime.now()))
  # close cursor
  db.close()

def check_num(number):
  # performs input validation, if no number assigned, passes in default value (1)
  # a very special thanks to: http://www.pythonforbeginners.com/error-handling/exception-handling-in-python
  try:
    num = int(number)
  except ValueError:
    num = 1
  
  return num;





