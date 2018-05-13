# "Database code" for the DB Forum.

import datetime
import psycopg2
import bleach

#POSTS = [("This is the first post.", datetime.datetime.now())]
DBNAME = "forum"

def get_posts():
  """Return all posts from the 'database', most recent first."""
  # from original - return reversed(POSTS)
  # connect to database "forum"
  db = psycopg2.connect(database=DBNAME)
  # create a cursor
  c = db.cursor()
  # select statement
  c.execute("select content, time from posts order by time desc")
  # store all posts in a new variable
  contents = c.fetchall()
  # close cursor
  db.close()
  # return posts
  return contents

def add_post(content):
  """Add a post to the 'database' with the current timestamp."""
  # from original - POSTS.append((content, datetime.datetime.now()))
  # connect to database "forum"
  db = psycopg2.connect(database=DBNAME)
  # create a cursor
  c = db.cursor()
  # bleach statement
  content = bleach.clean(content)
  # insert statement
  c.execute("insert into posts values (%s)", (content,))
  # commit to database
  db.commit()
  # close cursor
  db.close()




