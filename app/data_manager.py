import subprocess

def crawl_data():
  """
  Crawl the data and insert the info into a database.
  """
  subprocess.call("python " + "crawler.py", shell=True)

