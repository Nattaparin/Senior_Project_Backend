
from nltk import app
from PRO_BACK.controller.adminControll import adminController
from PRO_BACK.controller.mechanicControll import mecController


@app.route('/login', methods=['POST'])
def admin_login():
    return adminController.login()
@app.route('/login', methods=['POST'])
def mec_login():
    return mecController.login()

if __name__ == '__main__':
    app.run(debug=True)