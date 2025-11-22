python smart-claim/backend/utils/generate_patient.py 1
sleep 1
python smart-claim/backend/utils/convert_to_frontend.py smart-claim/backend/data/claims.json
sleep 1
python smart-claim/backend/utils/add_to_mockdata.py smart-claim/backend/data/claims_frontend.json
