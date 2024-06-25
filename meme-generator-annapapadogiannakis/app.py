from flask import Flask, render_template, request
import MemeEngine
import random,os, requests

# Import your Ingestor and MemeEngine classes
import MemeEngine
from QuoteEngine import Ingestor

app = Flask(__name__)

meme = MemeEngine.MemeEngine('./static')


def setup():
    """ Load all resources """

    quote_files = ['./_data/DogQuotes/DogQuotesTXT.txt',
                   './_data/DogQuotes/DogQuotesDOCX.docx',
                   './_data/DogQuotes/DogQuotesPDF.pdf',
                   './_data/DogQuotes/DogQuotesCSV.csv']

    # Use the Ingestor class to parse all files in the
    # quote_files variable
    quotes = []
    for f in quote_files:
        quotes.extend(Ingestor.parse(f))

    images_path = "./_data/photos/dog/"

    # Use the pythons standard library os class to find all
    # images within the images images_path directory
    imgs = None

    for root, dirs, files in os.walk(images_path):
        imgs = [os.path.join(root, name) for name in files]

    return quotes, imgs


quotes, imgs = setup()


@app.route('/')
def meme_rand():
    """ Generate a random meme """

    # @TODO:
    # Use the random python standard library class to:
    # 1. select a random image from imgs array
    # 2. select a random quote from the quotes array

    img = None
    quote = None
    img = random.choice(imgs)
    quote = random.choice(quotes)
    path = meme.make_meme(img, quote.body, quote.author)
    return render_template('meme.html', path=path)


@app.route('/create', methods=['GET'])
def meme_form():
    """ User input for meme information """
    return render_template('meme_form.html')


@app.route('/create', methods=['POST'])
def meme_post():
    """ Create a user defined meme """

    # 1. Use requests to save the image from the image_url
    #    form param to a temp local file.
    image_url = request.form['image_url']
    custom_request = requests.get(image_url, allow_redirects=True)
    image_name = random.randint(0, 1000000)
    tmp_file = f'./tmp/{image_name}.jpg'
    custom_image = open(tmp_file, 'wb')
    custom_image.write(custom_request.content)
    custom_image.close()


    # 2. Use the meme object to generate a meme using this temp
    #    file and the body and author form paramaters.

    meme = MemeEngine.MemeEngine('./static')
    path = meme.make_meme(tmp_file, request.form['body'], request.form['author'])

    # 3. Remove the temporary saved image.

    if os.path.exists(tmp_file):
        os.remove(tmp_file)

    return render_template('meme.html', path=path)


if __name__ == "__main__":
    app.run()
