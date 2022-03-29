import flask
from flask import Flask, render_template, request, flash
import json
from FDataBase import FDataBase
import datetime
import requests
import hashlib
import logging

app = Flask(__name__)

logging.basicConfig(filename="test.log", level=logging.DEBUG,
                   format="%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s")


app.config["SECRET_KEY"] = "SecretKey01"
db = FDataBase()
shop_id = 5
secretKey = "SecretKey01"
payway = "perfectmoney_usd"
USD = 840
EUR = 978
RUB = 643


def generate_hash(keys):
    res = ""
    for i in range(0, len(keys) - 1):
        res += f"{keys[i]}:"
    res += str(keys[-1])
    res += secretKey
    hash = hashlib.sha256(res.encode("utf-8")).hexdigest()
    return hash


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        data = request.form
        date = datetime.datetime.today()
        try:
            amount = format(float(data["sum"]), ".2f")
        except:
            flash("Wrong amount field format")
            return render_template("index.html")
        payment_id = db.add_payment_info(data["sum"], data["currency"], data["comment"], date)
        if data["currency"] == "EUR":
            currency = EUR
            keys = [amount, currency,  shop_id, payment_id]
            hash = generate_hash(keys)
            return render_template("pay.html", amount=keys[0], currency=keys[1], shop_id=keys[2], shop_order_id=keys[3], sign=hash)

        elif data["currency"] == "USD":
            payer_currency = USD
            currency = USD
            keys = [payer_currency, amount, currency, shop_id, payment_id]
            hash = generate_hash(keys)
            desc = db.get_description(payment_id)
            dictToSend = {"description": desc,
                          "payer_currency": payer_currency,
                          "shop_amount": amount,
                          "shop_currency": currency,
                          "shop_id": shop_id,
                          "shop_order_id": payment_id,
                          "sign": hash
                          }

            res = requests.post("https://core.piastrix.com/bill/create", json=dictToSend)
            dictFromServer = res.json()
            if dictFromServer["data"] == None:
                return render_template("errors.html", message=dictFromServer["message"], error_code=dictFromServer["error_code"])
            else:
                url = dictFromServer["data"]["url"]
                return flask.redirect(url)
        elif data["currency"] == "RUB":
            currency = RUB
            keys = [amount, currency, payway, shop_id, payment_id]
            hash = generate_hash(keys)
            dictToSend = {
                "amount": amount,
                "currency": currency,
                "payway": payway,
                "shop_id": shop_id,
                "shop_order_id": payment_id,
                "sign": hash
            }

            response = requests.post("https://core.piastrix.com/invoice/create", json=dictToSend)

            dictFromServer = response.json()
            if dictFromServer["data"] == None:
                return render_template("errors.html", message=dictFromServer["message"],
                                       error_code=dictFromServer["error_code"])
            else:
                method = dictFromServer["data"]["method"]
                url = dictFromServer["data"]["url"]
                invoice_response_data = dictFromServer["data"]["data"]
                return render_template("invoice.html", method=method, url=url, **invoice_response_data)

    return render_template("index.html")

if __name__ == "__main__":

    app.run(debug=True)