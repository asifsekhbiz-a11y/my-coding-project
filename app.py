from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    # Pass dynamic data to the HTML template
    my_message = "This message was generated and sent by Python!"
    return render_template('index.html', message=my_message)

if __name__ == '__main__':
    app.run(debug=True)
