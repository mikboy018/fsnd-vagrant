#!/usr/bin/env python3
# 
# A buggy web service in need of a database.

from flask import Flask, flash, request, redirect, url_for

from newsdatadb import get_posts, add_post, most_popular_articles, most_popular_author, check_failure_rate

app = Flask(__name__)

# HTML template for the forum page
HTML_WRAP = '''\
<!DOCTYPE html>
<html>
  <head>
    <title>Log Analysis Project</title>
    <style>
      h1, h3, title, form { text-align: center; }
      textarea { width: 400px; height: 100px; }
      div.post { border: 1px solid #999;
                 padding: 10px 10px;
                 margin: 10px 20%%; }
      hr.postbound { width: 50%%; }
      em.date { color: #999 }
      button { margin: 10px;}
    </style>
  </head>
  <body>
    <div name=title>
      <h1>Log Analysis: News Data</h1>
      <h3>By: Mike Boyer</h3>
      <a name=Projects href="https://mikboy018.github.io/">Other Projects<a>
      <a name=LinkedIn href="https://www.linkedin.com/in/michael-boyer-14316a50/">LinkedIn</a>
    </div>
    <form method=post>
      <div><textarea id="content" name="content" placeholder="Enter a whole number here, then press a button below."></textarea></div>
      <div><button formaction="/articles/" id="go" type="submit">Show Top Articles</button></div>
      <div><button formaction="/authors/" id="go" type="submit">Show Top Authors</button></div>
      <div><button formaction="/failrates/" id="go" type="submit">Show Days with Failure Rates Above Threshold</button></div>
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
  print("Searching authors!")
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

