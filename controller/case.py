from flask import jsonify

from Model import Case


class case:
    @staticmethod
    def get_case():
        case_item = Case.query.all()
        print(case_item)
        result = []
        for case in case_item:
            result.append({
                'id': case.case_id,
                'Owner_name': case.Owner_name,
                'car_Model': case.car_Model,
                'LICENSE_PLATE_NUMBER': case.LICENSE_PLATE_NUMBER,
                'phoneNumber': case.phoneNumber,
                'car_detail': case.car_detail,
                'car_symptoms': case.car_symptoms,
                'date': case.date,
                'Part_type': case.Part_type,
                'Car_part': case.Car_part,
                'Mec_name': case.Mec_name,
                'car_progress': case.car_progress
            })
        return jsonify(result)