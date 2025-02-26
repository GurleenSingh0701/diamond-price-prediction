import streamlit as st
import pickle
import numpy as np
import pandas as pd

import pickle
import bz2


# Load the trained model
with open("diamond_price_model.pkl", "rb") as file:
    model = pickle.load(file)

# Streamlit App Title
st.title("💎 Diamond Price Prediction App")

# Sidebar for User Input
st.sidebar.header("Enter Diamond Features")

carat = st.sidebar.slider("Carat", 0.2, 5.0, step=0.01)
volume = st.sidebar.slider("Volume", 1.0, 500.0, step=1.0)

cut = st.sidebar.selectbox("Cut", ["Fair", "Good", "Very Good", "Premium", "Ideal"])
clarity = st.sidebar.selectbox("Clarity", ['Very Slightly Included2', 'Slightly Included2', 'Slightly Included1', 'Included1', 'Very Very Slightly Included', 'Very Slightly Included1', 'Internally Flawless'])
color = st.sidebar.selectbox("Color", ['Colorless1', 'Colorless2', 'Colorless3', 'Near Colorless1','Near Colorless2', 'Near Colorless3', 'Near Colorless4'])

# Map categorical values to numerical encoding (update based on your encoding)
cut_dict = {"Fair": 0, "Good": 1, "Very Good": 2, "Premium": 3, "Ideal": 4}
color_dict = {'Colorless1':0, 'Colorless2':1, 'Colorless3':2, 'Near Colorless1':3,'Near Colorless2':4, 'Near Colorless3':5, 'Near Colorless4':6}
clarity_dict = {'Very Slightly Included2':0, 'Slightly Included2':1, 'Slightly Included1':2, 'Included1':3, 'Very Very Slightly Included':4, 'Very Slightly Included1':5, 'Internally Flawless':6}

# Convert categorical values safely
cut_value = cut_dict.get(cut, -1)
color_value = color_dict.get(color, -1)
clarity_value = clarity_dict.get(clarity, -1)


# **Fix: Check if any category returns -1 (meaning mapping failed)**
if -1 in [cut_value, color_value, clarity_value]:
    st.error("⚠ Invalid category detected! Please check your categorical encoding.")
else:
    # Convert user input into a DataFrame with correct formatting
    features = pd.DataFrame([[
        float(carat), float(volume), float(cut_value), float(color_value), float(clarity_value)
    ]], columns=["carat", "volume", "cut", "color", "clarity"])

    st.write("🛠 Debug: Feature Types")
    st.write(features.dtypes)

    # Prediction Button
    if st.sidebar.button("Predict Price"):
        try:
            predicted_price = model.predict(features)[0]
            st.success(f"💰 Predicted Diamond Price: ${np.expm1(predicted_price):,.2f}")
        except Exception as e:
            st.error(f"⚠ An error occurred during prediction: {e}")

# Footer
st.sidebar.markdown("Developed by [Your Name]")