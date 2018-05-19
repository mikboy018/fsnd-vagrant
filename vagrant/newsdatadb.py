"""

 "Database code" for the DB Forum modified to suit the needs of the project.

"""

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
    """ Queries for most popular articles, limiting by number specified """
    # verify input
    num = check_num(number, "integer")
    # mark start time
    start = datetime.datetime.now()
    # setup db connect
    db = psycopg2.connect(database=DBNAME)
    # create a cursor
    c = db.cursor()
    # select statement
    c.execute("""
        SELECT title, count(status) AS numViews
        FROM log, articles
        WHERE concat('/article/', articles.slug) = log.path
        GROUP BY title
        ORDER BY numViews DESC
        LIMIT %s;
    """, [num, ])
    # mark time query completed
    query_complete = datetime.datetime.now()
    # store answer to query
    num = c.rowcount
    contents = ("Most popular " +
                str(num) +
                " articles (Title / Number of Views) <br />")
    for row in c:
        article_name = str(row[0])
        # https://docs.python.org/2/library/string.html#string.capwords
        article_name = capwords(article_name)
        view_count = row[1]
        # https://mkaz.blog/code/python-string-format-cookbook/
        contents = (contents + article_name +
                    " / " + str("{:,}".format(view_count)) + "<br />")
    # mark time complete
    stop = datetime.datetime.now()
    # append to posts, with runtime info
    contents = (contents + "Query Duration: " +
                str(query_complete - start) +
                "<br />")
    contents = (contents +
                "Python Duration: " +
                str(stop - query_complete) +
                "<br />")
    contents = (contents + "Total Runtime: " +
                str(stop - start) + "<br />")
    POSTS.append((contents, datetime.datetime.now()))
    # make notice in the log
    # close cursor
    db.close()


def most_popular_author(number):
    """ Queries for most popular authors, limiting by number specified """
    # verify input
    num = check_num(number, "integer")
    # mark time start
    start = datetime.datetime.now()
    # setup db connection
    db = psycopg2.connect(database=DBNAME)
    # create a cursor
    c = db.cursor()
    # select statement
    c.execute("""
              SELECT authors.name, count(status) AS numViews
              FROM log, articles, authors
              WHERE concat('/article/', articles.slug) = log.path
              AND authors.id = articles.author
              GROUP BY authors.name
              ORDER BY numViews DESC
              LIMIT %s;
    """, [num, ])
    # mark time query completed
    query_complete = datetime.datetime.now()
    # store answer to query
    num = c.rowcount
    contents = ("The most popular " + str(num) +
                " authors (Name / Number of Views): <br />")
    for row in c:
        author_name = str(row[0])
        view_count = row[1]
        contents = (contents + author_name + " / " +
                    str("{:,}".format(view_count)) + "<br />")
    # mark time complete
    stop = datetime.datetime.now()
    # append to posts, with runtime info
    contents = (contents + "Query Duration: " +
                str(query_complete - start) + "<br />")
    contents = (contents + "Python Duration: " +
                str(stop - query_complete) + "<br />")
    contents = (contents + "Total Runtime: " +
                str(stop - start) + "<br />")
    POSTS.append((contents, datetime.datetime.now()))
    # close cursor
    db.close()


def check_failure_rate(min_rate):
    """ Queries for a minimum specified failure rate """
    # verify input
    min_rate = check_num(min_rate, "percent")
    # mark time start
    start = datetime.datetime.now()
    # setup db connection
    db = psycopg2.connect(database=DBNAME)
    # create a cursor
    c = db.cursor()
    # select statement
    c.execute("""
              SELECT to_char(time, 'MM/DD/YYYY') AS day,
              (SELECT cast(count(status) filter
              (WHERE status != '200 OK') AS float) / cast(count(status)
              AS float)*100)
              AS failRate
              FROM log
              GROUP BY day
              ORDER BY failRate DESC;
    """)
    # mark time query completed
    query_complete = datetime.datetime.now()
    # store answer to query
    contents = ("Days with a failure rate >= " + str(min_rate) +
                " percent (Day / Percent): <br />")
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
    contents = (contents + "Query Duration: " +
                str(query_complete - start) + "<br />")
    contents = (contents + "Python Duration: " +
                str(stop - query_complete) + "<br />")
    contents = (contents + "Total Runtime: " +
                str(stop - start) + "<br />")
    POSTS.append((contents, datetime.datetime.now()))
    # make notice in the log
    print("Errors > " + str(min_rate) + " percent retrieved!")
    # close cursor
    db.close()


def check_num(number, type):
    """
    Performs input validation, if no number assigned,
    Passes in default value (1)
    A very special thanks to: http://www.pythonforbeginners.com/error-handling/exception-handling-in-python # NOQA

    """
    if type == "integer":
        try:
            num = int(number)
            if num < 1:
                num = 1
        except ValueError:
            num = 1
    if type == "percent":
        try:
            num = float(number)
        except ValueError:
            num = 0.00001
    return num
