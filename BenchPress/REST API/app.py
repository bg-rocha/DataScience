from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort
from prediction.prediction import *

model = joblib.load('models/lgbm_v1.pkl')

app = Flask(__name__)
api = Api(app)

predict_args = reqparse.RequestParser()
predict_args.add_argument('Sex', type=str, help="Missing Sex", required=True)
predict_args.add_argument('Equipment', type=str, help="Missing Type of equipmnt", required=True)
predict_args.add_argument('Age', type=int, help="Missing Age", required=True)
predict_args.add_argument('BodyweightKg', type=float, help="Missing BodyweightKg", required=True)
predict_args.add_argument('BestSquatKg', type=str, help="Missing BestSquatKg", required=True)
predict_args.add_argument('BestDeadliftKg', type=float, help="Missing BestDeadliftKg", required=True)

equipments = ['Raw', 'Wraps', 'Single-ply', 'Multi-ply']
json_expected = {
  "Sex": "str: ['M', 'F']",
  "Age": "int",
  "Equipment": f"str: {equipments}",
  "BodyweightKg": "float",
  "BestSquatKg": "float",
  "BestDeadliftKg": "float"
}

 
def check_args(args):
    if args['Sex'] not in ['M', 'F']:
        abort(400, message=f"Invalid Sex, expected one of :{['M', 'F']}")
    elif args['Equipment'] not in equipments:
        abort(400, message=f"Invalid equipment, expected one of :{equipments}")
    elif (args['Age'] <1) or (args['Age'] > 130):
        abort(400, message="Invalid age")


class BenchPress(Resource):

    def get(self):
        return {"json_expected":json_expected}
    
    def post(self):
        args =predict_args.parse_args()
        check_args(args)
        values = list(dict(args).values())

        return {"Bench Press (kg) predction": BP_predict(model, values)}

api.add_resource(BenchPress, '/')


if __name__ == "__main__":
    app.run(debug=False)
