from flask import request, jsonify

from Model import User, Case, db, Tracking


class register_case:
    @staticmethod
    def register_case():
        data = request.get_json()

        Owner_name = data.get('Owner_name')
        car_Model = data.get('car_Model')
        LICENSE_PLATE_NUMBER = data.get('LICENSE_PLATE_NUMBER')
        phoneNumber = data.get('phoneNumber')
        car_detail = data.get('car_detail')
        car_symptoms = data.get('car_symptoms')
        date = data.get('date')
        Part_type = data.get('Part_type')
        Car_part = data.get('Car_part')

        Mec_name  = data.get('Mec_name')


        save_bm = Case(
            Owner_name=Owner_name,
            car_Model=car_Model,
            LICENSE_PLATE_NUMBER=LICENSE_PLATE_NUMBER,
            phoneNumber=phoneNumber,
            car_symptoms=car_symptoms,
            date=date,
            Part_type=Part_type,
            Car_part=Car_part,
            Mec_name=Mec_name ,
            car_detail=car_detail,
            car_progress= 'รับรถแล้ว'
    )
        save_bm.mechanic = Mec_name
        db.session.add(save_bm)
        db.session.commit()
        case_dict = save_bm.to_dict()
        return jsonify({'car_case': case_dict}), 200