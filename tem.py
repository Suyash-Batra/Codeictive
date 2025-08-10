from flask import Flask, redirect, url_for, request, send_file,render_template
import hakoton.sel as sel
import hakoton.t as t
import os

app = Flask(__name__)
plt = ''
us = ''

@app.route("/")
def index():
  return render_template("index.html")

@app.route('/about')
def about():
  return render_template('about.html')

@app.route("/xlogin")
def xlogin():
  return render_template("xlogin.html")

@app.route("/linkedinlogin")
def linkedinlogin():
  return render_template("linkedinlogin.html")

@app.route('/downloadl')
def downloadl():
  return render_template('downloadl.html')

@app.route('/downloadx')
def downloadx():
  return render_template('downloadx.html')

@app.route('/link',methods=['GET', 'POST'])
def link():
    global plt
    us=request.form["un"]
    ps=request.form["p"]
    plt=request.form["plt"]
    if(plt=='x'):
        em=request.form["em"]
        t.pw(us,em,ps)
        return redirect(url_for("downloadx"))
    else:
        sel.sr(us,ps)
        return redirect(url_for("downloadl"))
        
@app.route('/downx')
def downx():
  return send_file(f'X.zip', as_attachment=True)

@app.route('/downl')
def downl():
  return send_file(f'merged_chats.pdf',as_attachment=True)

if __name__ == '__main__':
   app.run(debug = True)
   #print(os.getcwd())