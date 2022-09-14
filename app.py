import requests
from bs4 import BeautifulSoup as bs
from flask import Flask, render_template, request
from flask_cors import cross_origin

app = Flask(__name__)

@app.route('/',methods=['GET'])
@cross_origin()
def homePage():
    return render_template("index.html")

@app.route('/review',methods=['POST','GET'])
@cross_origin()
def index():
    if request.method == 'POST':
        try:
            search = request.form['content']
            res1 = requests.get(f'https://www.flipkart.com/search?q={search}')
            soup1 = bs(res1.text, "lxml")
            link1 = soup1.select('._1fQZEK')
            link2 = soup1.select('._2rpwqI')
            if len(link1) > 0:
                product_link = 'https://www.flipkart.com' + link1[0]['href']
            else:
                product_link = 'https://www.flipkart.com' + link2[0]['href']
            res2 = requests.get(product_link)
            soup2 = bs(res2.text, "lxml")
            for i in range(len(soup2('a'))):
                if 'reviews' in soup2('a')[i].getText():
                    f = soup2('a')[i]
            review_link = 'https://www.flipkart.com' + f['href']
            res3 = requests.get(review_link)
            soup3 = bs(res3.text, "lxml")
            customer = soup3.select('._2sc7ZR._2V5EHH')
            rating = soup3.select('._3LWZlK._1BLPMq')
            heading = soup3.select('._2-N8zT')
            review = soup3.select('.t-ZTKy')
            filename = search + ".csv"
            file_csv = open(filename, "w",newline='\n',encoding='utf-8')
            headers = 'Customer Name,Rating,Heading,Comment\n'
            file_csv.write(headers)
            reviews = []
            for j in range(len(customer)):
                mydict = {"Product": search, "Name": customer[j].getText(), "Rating": rating[j].getText(), "CommentHead": heading[j].getText(), "Comment": review[j].div.div.getText()}
                reviews.append(mydict)
                csv_reviews = (f'{customer[j].getText()},{rating[j].getText()},{heading[j].getText()},{review[j].div.div.getText()}\n')
                file_csv.write(csv_reviews)
            return render_template('results.html', reviews=reviews[0:(len(reviews) - 1)])
        except Exception as e:
            print('The Exception message is: ', e)
            return 'something is wrong'
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)