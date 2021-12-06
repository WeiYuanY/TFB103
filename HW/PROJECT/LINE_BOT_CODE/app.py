from flask import Flask, request, render_template
import model
import drugInteraction
import noticesform

#宣告app 物件
app = Flask(__name__)

#定義接口
@app.route('/')
def index():
    return  "Hello Flask!"

#總表(訂值)
@app.route('/show_notices')
def notice():
    notices_data = model.getNotices()
    column = ['健保代碼', '英文名', '中文名','用藥注意','用藥頻率','建議用藥時間']
    return render_template('show_notices.html', notices_data=notices_data,
                                              column=column)

# #總表(還沒解決錯誤，所以先用訂值呈現)
# @app.route('/show_noticesform', methods=['GET', 'POST'])
# def noticesform():
#     outStr = """
#         <h1>請輸入身分證字號</h1>
#          <form action="/show_noticesform" method="POST">
#              <input name="NEWID">
#              <button type="submit">SUBMIT</button>
#          </form>
#          """
#     method = request.method
#     if method == 'GET':
#         return outStr
#     if method == 'POST':
#         NEWID = request.form.get('NEWID')
#         noticesform_data = noticesform.getNoticesform(NEWID)
#         column = ['健保代碼', '英文名', '中文名','用藥注意','用藥頻率','建議用藥時間']
#         return render_template('show_noticesform.html',method=method,noticesform_data=noticesform_data,column=column)


#藥物交互作用
@app.route('/show_interaction', methods=['GET', 'POST'])
def interaction():
    outStr = """
        <h1>請輸入病患的身分證字號</h1>
         <form action="/show_interaction" method="POST">
             <input name="ID">
             <button type="submit">SUBMIT</button>
         </form>
         """
    method = request.method
    if method == 'GET':
        return outStr
    if method == 'POST':
        ID = request.form.get('ID')
        drug_interaction = drugInteraction.getInteracion(ID)
        column = ['DRUG_NAME','INTER_DRUG_NAME','DRUG_INTERACTION']
        return render_template('show_interaction.html',method=method,
                               drug_interaction=drug_interaction,column=column)

#啟動伺服器
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000,debug=False)