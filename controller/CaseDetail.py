from flask import jsonify

from Model import Case


class case:
    @staticmethod
    def get_case():
        case = Case.query.all()
        result = []
        for case in case:
            result.append({
                'id': case.id,
                'Owner_name': case.Owner_name,
                'car_Model': case.car_Model,
                'LICENSE_PLATE_NUMBER': case.LICENSE_PLATE_NUMBER,
                'phoneNumber': case.phoneNumber,
                'car_symptoms': case.car_symptoms,
                'problems': case.problems,
                'sounds': case.sounds,
                'Mec_name': case.Mec_name

            # เพิ่มฟิลด์อื่น ๆ ตามต้องการ
        })
        return jsonify(result)