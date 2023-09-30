from flask import jsonify

from Model import  db


class Case(db.Model):

    def to_dict(self):
        # Return a dictionary representation of the Case instance
        return {
            'Owner_name': self.Owner_name,
            'car_Model': self.car_Model,
            'LICENSE_PLATE_NUMBER': self.LICENSE_PLATE_NUMBER,
            'phoneNumber': self.phoneNumber,
            'car_symptoms': self.car_symptoms,
            'problems': self.problems,
            'sounds': self.sounds,
            'Mec_name': self.Mec_name,
            # Add other fields as needed
        }
class CaseDetail:
    @staticmethod
    def get_caseID(id):
        case = Case.query.get(id)
        if case is None:
            return jsonify({'error': 'Case not found'}), 404

        case_data = {
            'id': case.id,
            'Owner_name': case.Owner_name,
            'car_Model': case.car_Model,
            'LICENSE_PLATE_NUMBER': case.LICENSE_PLATE_NUMBER,
            'phoneNumber': case.phoneNumber,
            'date': case.date,
            'car_symptoms': case.car_symptoms,
            'problems': case.problems,
            'sounds': case.sounds,
            'car_progress':case.car_progress,
            'Mec_name': case.Mec_name
            # Add other fields as needed
        }
        return jsonify(case_data)