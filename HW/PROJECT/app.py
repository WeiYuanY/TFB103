from flask import Flask, request, jsonify, render_template
import model

#宣告app 物件
app = Flask(__name__)

#定義接口(街口名稱所需的字串)
@app.route('/')
def index(): #定義函數(首頁的概念)
    return  "Hello Flask!"  #回傳給使用者的東西

@app.route('/show_notices')
def hello_google():
    notices_data = model.getNotices()
    column = ['健保代碼', '英文名', '中文名', '臨床用途', '主要副作用', '儲存方式','用藥注意','其他說明']
    return render_template('show_notices.html', notices_data=notices_data,
                                              column=column)



#啟動伺服器
# if __name__ == "__main__":
#     app.run(debug=True,port=1234)
#
import os
if __name__ == "__main__":
    # port = int(os.environ.get('PORT', 80))
    app.run(host='0.0.0.0', port=5000)