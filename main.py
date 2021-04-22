"""
These are the URLs that will give you remote jobs for the word 'python'

https://stackoverflow.com/jobs?r=true&q=python
https://weworkremotely.com/remote-jobs/search?term=python
https://remoteok.io/remote-dev+python-jobs

Good luck!
"""
import requests
from flask import Flask, render_template, request, redirect, send_file
from bs4 import BeautifulSoup
import csv

app = Flask("DayThirteen")

urls = ['https://stackoverflow.com/jobs?r=true&q=',
'https://weworkremotely.com/remote-jobs/search?term=',
'https://remoteok.io/remote-dev+']

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}

db = {}

@app.route("/")
def home():
  return render_template('home.html')

@app.route("/list")
def list():
  term = request.args.get("term").lower()

  if term in db:
    return render_template('list.html', infos = db[term],term = request.args.get("term"))
  
  else:
    infos = []

    content = requests.get(urls[0]+term, headers=headers)
    soup = BeautifulSoup(content.text, "html.parser")
    jobs = soup.select('.-job.js-result.js-dismiss-overlay-container.ps-relative')
    for job in jobs:
      info = []
      info.append(job.select('.s-link.stretched-link')[0].text)
      info.append(job.select('h3 span')[0].text)
      info.append('https://stackoverflow.com'+job.select('.mb4.fc-black-800.fs-body3 a')[0]['href'])
      infos.append(info)

    content = requests.get(urls[1]+term)
    soup = BeautifulSoup(content.text, "html.parser")
    jobs = soup.select('.feature')
    for job in jobs:
      info = []
      info.append(job.select('.title')[0].text)
      info.append(job.select('.company')[0].text)
      info.append('https://weworkremotely.com'+job.select('a')[0]['href'])
      infos.append(info)


    content = requests.get(urls[2]+term+'-jobs', headers=headers)
    soup = BeautifulSoup(content.text, "html.parser")
    jobs = soup.select('.job')
    for job in jobs:
      info = []
      info.append(job.select('h2')[0].text)
      info.append(job.select('h3')[0].text)
      try:
        info.append('https://remoteok.io'+job.select('.source a')[0]['href'])
      except:
        continue
      infos.append(info)


    db[term]= infos
    

    return render_template('list.html', infos = infos, term = request.args.get("term"))

@app.route('/export')
def export():
  term = request.args.get('term').lower()
  jobs = db.get(term)
  file = open("jobs.csv", mode="w")
  writer = csv.writer(file)
  writer.writerow(['title','company','link'])
  # print(db)
  # print(jobs)
  for job in jobs:
    writer.writerow(job)

  return send_file('jobs.csv', as_attachment=True)

app.run(host='0.0.0.0')