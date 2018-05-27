#!/usr/bin/env python

"""

HTML template for the forum page from the Database Forum Examples
used in Udacity's Full-Stack Web Developer Nanodegree

The following resources were very helpful:
https://sites.duke.edu/compsci316_01_s2017/help/flask/
https://stackoverflow.com/questions/29375046/adding-google-fonts-to-flask
Google Fonts: https://fonts.google.com/?selection.family=Aldrich

"""

from flask import Flask, flash, request, redirect, url_for

from newsdatadb import (get_posts, add_post, most_popular_articles,
                        most_popular_author, check_failure_rate)

app = Flask(__name__)

HTML_WRAP = '''\
<!DOCTYPE html>
<html>
  <head>
    <title>Log Analysis Project</title>
    <link rel="stylesheet" type="text/css" href="static/style.css">
    <link href="{{ https://fonts.googleapis.com/css?family=Aldrich }}"
      rel="stylesheet">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta charset="utf-8">
  </head>
  <body>
    <div>
      <h1>Log Analysis: News Data</h1>
      <h3>By: Mike Boyer</h3>
      <a id=title name=Projects href="https://mikboy018.github.io/">
        Other Projects
      </a>
      <a id=title name=LinkedIn href="https://www.linkedin.com/in/boyermikee">
        LinkedIn
      </a>
      <h5>Enter a number (>0.00001) and hit one of the three buttons.</h5>
      <h5>Example: Entering 2, and pressing Authors or Articles buttons</h5>
      <h5>will display the top 2 Authors/Articles. Pressing Failure Rate</h5>
      <h5>button will display errors greater than 2 percent.</h5>
      </div>
    </div>
    <form method=post>
      <div>
        <textarea id="content" name="content" placeholder="1"></textarea>
      </div>
      <div>
        <button formaction="/articles/" id="go" type="submit">
          Show Top Articles
        </button>
      </div>
      <div>
        <button formaction="/authors/" id="go" type="submit">
          Show Top Authors
        </button>
      </div>
      <div>
        <button formaction="/failrates/" id="go" type="submit">
          Show Days with Failure Rates Above Threshold
        </button>
      </div>
    </form>
    <!-- post content will go here -->
%s
  </body>
</html>
'''

# HTML template for an individual comment
POST = '''\
    <div class=post><em class=date>%s</em><br>%s</div>
'''


@app.route('/', methods=['GET'])
def main():
    '''Main page of the forum.'''
    posts = "".join(POST % (date, text) for text, date in get_posts())
    html = HTML_WRAP % posts
    return html


@app.route('/articles/', methods=['POST'])
def articles():
    '''New post submission.'''
    print("Searching Articles!")
    message = request.form['content']
    most_popular_articles(message)
    print("Articles Retrieved!")
    return redirect(url_for('main'))


@app.route('/authors/', methods=['POST'])
def authors():
    print("Searching Authors!")
    message = request.form['content']
    most_popular_author(message)
    print("Authors Retrieved!")
    return redirect(url_for('main'))


@app.route('/failrates/', methods=['POST'])
def fail_rate():
    print("Searching Errors!")
    message = request.form['content']
    check_failure_rate(message)
    return redirect(url_for('main'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
