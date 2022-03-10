import db
from flask import Flask, abort

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
  return '<a href="/project">project list</a>'

@app.route("/project", methods=["GET"])
def proj_list():
    conn = db.get_connection()
    projects = db.get_projects(conn)
    conn.close()
    return projects

@app.route("/project/<int:proj_id>", methods=["GET"])
def switch_list(proj_id):
    conn = db.get_connection()
    switches = db.get_switches_by_project(conn, proj_id)
    conn.close()
    if not switches[proj_id]:
      abort(404)
    return switches[proj_id]

@app.route("/projectsummary/<int:proj_id>", methods=["GET"])
def project_summary(proj_id):
    conn = db.get_connection()
    summary = db.get_summary_by_project(conn, proj_id)
    conn.close()
    if not summary[proj_id]:
      abort(404)
    return summary[proj_id]


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)