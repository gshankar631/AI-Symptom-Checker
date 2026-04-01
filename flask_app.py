import os
import pandas as pd
from flask import Flask, render_template, request
from symptom_checker import SymptomChecker

app = Flask(__name__)
checker = SymptomChecker(r"F:\Project\Data\symptoms_dataset.csv")
excel_file = r"F:\Project\Data\bookings.xlsx"  # Excel file path for storing bookings

@app.route("/")
def welcome():
    return render_template("welcome.html")

@app.route("/check", methods=["GET", "POST"])
def check():
    result = None
    user_input = ""
    if request.method == "POST":
        user_input = request.form.get("symptoms", "")
        if user_input.strip():
            result = checker.check_symptoms(user_input)
            return render_template("doctor.html", 
                                   condition=result['Condition'], 
                                   doctor=result['Doctor'])
    return render_template("index.html", result=result, user_input=user_input)

@app.route("/booking", methods=["GET", "POST"])
def booking():
    condition = request.args.get("condition", "")
    doctor = request.args.get("doctor", "")

    if request.method == "POST":
        name = request.form.get("name")
        nhs_id = request.form.get("nhs_id")
        date = request.form.get("date")
        time = request.form.get("time")

        # Save booking to Excel
        new_entry = pd.DataFrame([{
            "Name": name,
            "NHS_ID": nhs_id,
            "Condition": condition,
            "Doctor": doctor,
            "Date": date,
            "Time": time
        }])

        if os.path.exists(excel_file):
            df_existing = pd.read_excel(excel_file)
            df_all = pd.concat([df_existing, new_entry], ignore_index=True)
        else:
            df_all = new_entry

        df_all.to_excel(excel_file, index=False)

        return render_template("confirmation.html", name=name, nhs_id=nhs_id,
                               date=date, time=time, condition=condition, doctor=doctor)
    
    return render_template("booking.html", condition=condition, doctor=doctor)

if __name__ == "__main__":
    app.run(debug=True)
