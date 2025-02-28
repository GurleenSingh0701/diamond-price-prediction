import streamlit as st
import pickle
import numpy as np
import pandas as pd
import bz2

# Load the trained model
with bz2.BZ2File("diamond_price_model.pkl", "rb") as file:
    model = pickle.load(file)

# Custom CSS to make the form bigger and center it nicely
st.markdown("""
    <style>
    .big-font {
        font-size: 20px !important;
    }
    .form-container {
        background-color: #f9f9f9;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
    }
    .stSlider > div { padding: 5px 0; }
    .stSelectbox > div { padding: 5px 0; }
    </style>
""", unsafe_allow_html=True)

# App Title
st.title("💎 Diamond Price Prediction App")

# Centering the form with columns
col1, col2, col3 = st.columns([1, 3, 1])  # Make middle column wider

with col2:
    st.markdown('<div class="form-container">', unsafe_allow_html=True)
    st.subheader("📋 Enter Diamond Features")

    with st.form("diamond_form"):
        # Sliders for Carat and Volume with larger space
        carat, volume = st.columns([1, 1])
        with carat:
            carat = st.slider("💎 Carat", 0.2, 5.0, step=0.01)
        with volume:
            volume = st.slider("📏 Volume", 1.0, 500.0, step=1.0)

        # Selectboxes for Cut and Clarity
        cut, clarity = st.columns([1, 1])
        with cut:
            cut = st.selectbox("✂️ Cut Type", ["Fair", "Good", "Very Good", "Premium", "Ideal"], index=0)
        with clarity:
            clarity = st.selectbox("🔎 Clarity", [
                'Very Slightly Included2', 'Slightly Included2', 'Slightly Included1',
                'Included1', 'Very Very Slightly Included', 'Very Slightly Included1', 'Internally Flawless'
            ], index=0)

        # Selectbox for Color
        color = st.selectbox("🌈 Color", [
            'Colorless1', 'Colorless2', 'Colorless3',
            'Near Colorless1', 'Near Colorless2', 'Near Colorless3', 'Near Colorless4'
        ], index=0)

        # Prediction button (submit form)
        submitted = st.form_submit_button("💰 Predict Price", type="primary")

    st.markdown('</div>', unsafe_allow_html=True)

    # Prediction logic (only runs if form is submitted)
    if submitted:
        cut_dict = {"Fair": 0, "Good": 1, "Very Good": 2, "Premium": 3, "Ideal": 4}
        color_dict = {
            'Colorless1': 0, 'Colorless2': 1, 'Colorless3': 2,
            'Near Colorless1': 3, 'Near Colorless2': 4, 'Near Colorless3': 5, 'Near Colorless4': 6
        }
        clarity_dict = {
            'Very Slightly Included2': 0, 'Slightly Included2': 1, 'Slightly Included1': 2,
            'Included1': 3, 'Very Very Slightly Included': 4,
            'Very Slightly Included1': 5, 'Internally Flawless': 6
        }

        # Convert categorical to numeric
        cut_value = cut_dict[cut]
        color_value = color_dict[color]
        clarity_value = clarity_dict[clarity]

        # Prepare features for prediction
        features = pd.DataFrame([[carat, volume, cut_value, color_value, clarity_value]],
                                columns=["carat", "volume", "cut", "color", "clarity"])

        # Predict and display result
        try:
            predicted_price = model.predict(features)[0]
            st.success(f"💰 Predicted Diamond Price: ${np.expm1(predicted_price):,.2f}")
        except Exception as e:
            st.error(f"⚠️ Error during prediction: {e}")
