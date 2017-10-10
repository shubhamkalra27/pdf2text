from flask import Flask, request, redirect, url_for, render_template, flash, session, Markup

import tika, re, pdb, time, os, sys
from tika import parser
tika.initVM()

script_dir = os.path.dirname(__file__)
UPLOAD_FOLDER  = (os.path.join(script_dir,r'static'))

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



@app.route('/')
def pdf():
    return '''
    <html>
	  <head>
	    <title>pdf2text</title>
	  </head>	
	  <body>
      <h2>Upload a pdf </h2>
	  <form method=post enctype=multipart/form-data action="/txt">
	  		<input type="file" name="file">
	    	 <input type="submit" value="Upload">
		</form>
		</body>
        </html>
	'''


@app.route('/txt', methods=['POST'])
def txt():
    uploaded_file = request.files.get('file')
    file = request.files['file']
    if not uploaded_file:
        return redirect(url_for('pdf')) 
    filename = (file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    file_perma_url = os.path.join(app.config['UPLOAD_FOLDER'], filename)    

    # print(uploaded_file, file=sys.stderr)
    # pdb.set_trace()
    # print("file saved to " + file_perma_url , file=sys.stderr)

    parsed = parser.from_file(file_perma_url)
    content = parsed['content'].replace("\n\n", "\n")
    content = re.sub('\s+', ' ', content).strip()
    print (content)

    value = Markup(content)
    return render_template('pdf.html',  messages={'pdf2text':value})


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8088, debug=True)

