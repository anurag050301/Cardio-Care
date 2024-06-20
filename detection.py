import streamlit as st
from PIL import Image
import pandas as pd
import numpy as np
import pickle

def main():
    st.set_page_config(page_title="Cardio Care", page_icon="🫀", layout="wide")
    st.title("Cardio Care: Protecting Hearts Through Detection")
    st.markdown("""
    <style>
    .main {
        max-width: 75%;  /* Adjust the width as needed */
        margin: 0 auto;
        justify-content: center;
    }      
    </style>
    <div class="intro">
    Cardio Care is an innovative web application designed to revolutionize cardiovascular disease detection. Leveraging the power of machine learning, specifically Logistic Regression, K-Nearest Neighbors (KNN), and Decision Tree models, Cardio Care provides a comprehensive and accurate assessment of an individual's risk for cardiovascular disease.
                
    Our application aims to empower users with the knowledge and tools necessary to proactively manage their heart health. By simply inputting key health metrics such as age, gender, chest pain type, resting blood pressure, cholesterol levels, and other relevant factors, Cardio Care generates a personalized risk assessment report. This report not only identifies the likelihood of developing cardiovascular disease but also provides valuable insights and recommendations for preventative measures.

    What sets Cardio Care apart is its commitment to accuracy and user-friendliness. Our machine learning models have been trained on a robust dataset, ensuring reliable and consistent results. The intuitive interface makes it easy for users to navigate and understand their results, promoting better understanding and engagement with their heart health.
                
    Join us in the fight against cardiovascular disease. With Cardio Care, early detection and prevention are within reach, paving the way for healthier hearts and lives.
    </div>
    """,
    unsafe_allow_html=True
    )
    image = Image.open("./images/cardio_care.jpg")
    st.image(image, caption="Cardio Care", use_column_width=True)
    st.header("Patient Information Form:")

    # Form inputs
    algo = st.selectbox("Select the Model", ['Logistic Regression', 'KNN', 'Decision Tree'])
    age = st.number_input("Age (years)", min_value=0, max_value=120, step=1)
    sex = st.selectbox("sex", ['M', 'F'])
    chest_pain_type = st.selectbox("Chest Pain Type", ['ATA', 'NAP', 'ASY', 'TA'])
    resting_bp = st.number_input("Resting Blood Pressure (mm Hg)", min_value=0)
    cholesterol = st.number_input("Cholesterol (mg/dl)", min_value=0)
    fasting_bs = st.selectbox("Fasting Blood Sugar",['False','True'])
    resting_ecg = st.selectbox("Resting ECG Results", ['Normal', 'ST', 'LVH'])
    max_heart_rate = st.number_input("Max Heart Rate Achieved (bpm)", min_value=0)
    exercise_angina = st.selectbox("Exercise Induced Angina", ['Y', 'N'])
    old_peak = st.number_input("Old Peak", min_value=0.0, step=0.1)
    st_slope = st.selectbox("Slope of the peak exercise ST segment", ['Up', 'Flat', 'Down'])

    # Convert categorical variables to numerical
    gender_num = 2 if sex == 'M' else 1
    chest_pain_type_num = ['ATA', 'NAP', 'ASY', 'TA'].index(chest_pain_type) + 1
    fasting_bs_num = 2 if fasting_bs == 'True' else 1
    resting_ecg_num = ['Normal', 'ST', 'LVH'].index(resting_ecg) +1
    exercise_angina_num = 2 if exercise_angina == 'Y' else 1
    st_slope_num = ['Up', 'Flat', 'Down'].index(st_slope) + 1

    # Prepare input data as a DataFrame
    input_data = pd.DataFrame({
        'age': [age],
        'sex': [gender_num],
        'chest_pain_type': [chest_pain_type_num],
        'resting_bp': [resting_bp],
        'cholesterol': [cholesterol],
        'fasting_bs': [fasting_bs_num],
        'resting_ecg': [resting_ecg_num],
        'max_heart_rate': [max_heart_rate],
        'exercise_angina': [exercise_angina_num],
        'old_peak': [old_peak],
        'st_slope': [st_slope_num]
    })

    # Submit button
    if st.button("Detect", key="detect", help="Click to submit the form"):
        st.write("Form Submitted Successfully!")
        if algo == 'Logistic Regression':
            picklefile = open("LR-model.pkl", "rb")
        elif algo == 'KNN':
            picklefile = open("KNN-model.pkl", "rb")
        else:
            picklefile = open("DT-model.pkl", "rb")
        model = pickle.load(picklefile)
        prediction = model.predict(input_data)
        if prediction[0] == 0:
            st.success('No Sign of Cardio Vascular Disease. Detected via ' + algo)
        elif prediction[0] == 1:
            st.error( 'Heart disease detected. Detected via ' + algo)

        # Check if the resting blood pressure is above the normal value
        normal_resting_bp = 120  # Adjust this value as needed
        if resting_bp > normal_resting_bp:
            st.warning("Your resting blood pressure is higher than normal.")
            st.write("""
            ### Precautions to Reduce High Blood Pressure:
            1. **Reduce Salt Intake:** Aim to eat less salt by avoiding processed foods and not adding extra salt to meals.
            2. **Eat a Balanced Diet:** Focus on whole grains, fruits, vegetables, and low-fat dairy products.
            3. **Exercise Regularly:** Engage in regular physical activity, such as walking, jogging, or cycling.
            4. **Maintain a Healthy Weight:** If you are overweight, losing even a small amount of weight can help reduce blood pressure.
            5. **Limit Alcohol Consumption:** Drink alcohol in moderation, if at all.
            6. **Quit Smoking:** Smoking increases blood pressure and heart rate.
            7. **Manage Stress:** Practice stress-reducing techniques like yoga, meditation, or deep breathing exercises.
            8. **Monitor Your Blood Pressure:** Keep track of your blood pressure at home and see your doctor regularly.
            9. **Take Prescribed Medications:** Follow your doctor's advice and take any prescribed medications as directed.
            """)

        #Check if the Cholesterol is above the normal value
        nomral_cholesterol = 200 
        if cholesterol > nomral_cholesterol:
            st.warning("Your Cholestrol level is higher than normal.")
            st.write("""
            ### Precautions to Reduce Cholesterol:
            1. **Eat Healthy:** Choose fruits, veggies, whole grains, and lean proteins. Avoid saturated fats and trans fats.
            2. **Stay Active:** Aim for regular exercise, like brisk walking, for at least 30 minutes most days.
            3. **Maintain Weight:** Keep a healthy weight to improve cholesterol levels.
            4. **Quit Smoking:** Smoking lowers good cholesterol and damages blood vessels.
            5. **Limit Alcohol**: Too much alcohol can raise cholesterol levels.
            6. **Medication:** In some cases, medication may be needed to lower cholesterol.
            7. **Regular Check-ups:** Monitor cholesterol levels and overall heart health regularly.
            """)

        #Check if the fasting blood sugar is above normal value.
        if fasting_bs =='True':
            st.warning("Your fasting Blood Sugar level is not normal.")
            st.write("""
            ### Precautions for blood sugar level:
            High Fasting Blood Sugar
            1. **Healthy Diet:** Eat a balanced diet rich in whole grains, fruits, vegetables, and lean proteins. Limit refined sugars and processed foods.
            2. **Regular Exercise:** Engage in regular physical activity to help manage blood sugar levels.
            3. **Monitor Blood Sugar:** Regularly check your blood sugar levels as recommended by your healthcare provider.
            4. **Medication Adherence:** Take prescribed medications or insulin as directed by your doctor.
            5. **Hydration:** Drink plenty of water to stay hydrated and help your body regulate blood sugar levels.
            6. **Portion Control:** Be mindful of portion sizes to avoid overeating and spikes in blood sugar.
            7. **Manage Stress:** Practice stress management techniques like meditation, yoga, or deep breathing exercises.
            8. **Regular Check-Ups:** Keep up with regular medical appointments to monitor and manage your condition.
            9. **Avoid Alcohol:** Limit alcohol consumption, as it can affect blood sugar levels.
            10. **Healthy Weight:** Maintain a healthy weight through diet and exercise to improve blood sugar control.
            """)
        
        # Check if the heart rate is above the normal value
        normal_max_heart_rate = 100  # Adjust this value as needed
        if max_heart_rate > normal_max_heart_rate:
            st.warning("Your maximum heart rate is higher than normal.")
            st.write("""
            ### Precautions to Reduce High Heart Rate:
            1. **Practice Deep Breathing:** Engage in deep breathing exercises to help calm your heart rate.
            2. **Stay Hydrated:** Drink plenty of water throughout the day.
            3. **Avoid Stimulants:** Reduce or avoid intake of caffeine and nicotine.
            4. **Engage in Regular Physical Activity:** Regular, moderate exercise can help lower your resting heart rate over time.
            5. **Manage Stress:** Practice relaxation techniques such as yoga or meditation.
            6. **Get Enough Sleep:** Ensure you are getting adequate rest each night.
            7. **Consult Your Doctor:** If high heart rate persists, seek medical advice for appropriate interventions.
            """)

if __name__ == "__main__":
    main()