import streamlit as st
import requests
import pandas as pd
import os

# Backend API URL - set as an environment variable in the Codespace, or edit the default below
BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:7860")

st.set_page_config(page_title="SuperKart Sales Predictor", page_icon="cart", layout="wide")

st.title("SuperKart Sales Prediction")
st.markdown("Predict product-store sales revenue for SuperKart outlets using machine learning.")

option = st.sidebar.selectbox("Choose Prediction Mode", ["Single Prediction", "Batch Prediction"])

if option == "Single Prediction":
    st.header("Single Product Sales Prediction")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Product Details")
        product_weight = st.number_input("Product Weight (kg)", min_value=1.0, max_value=25.0, value=12.0, step=0.1)
        product_sugar_content = st.selectbox("Product Sugar Content", ["Low Sugar", "Regular", "No Sugar"])
        product_allocated_area = st.number_input("Product Allocated Area", min_value=0.001, max_value=0.5, value=0.05, step=0.001, format="%.3f")
        product_mrp = st.number_input("Product MRP", min_value=10.0, max_value=300.0, value=150.0, step=1.0)
        product_id_char = st.selectbox("Product Category (Id prefix)", ["FD", "DR", "NC"])
        product_type_category = st.selectbox("Product Type Category", ["Perishables", "Non Perishables"])

    with col2:
        st.subheader("Store Details")
        store_size = st.selectbox("Store Size", ["Small", "Medium", "High"])
        store_location = st.selectbox("Store Location City Type", ["Tier 1", "Tier 2", "Tier 3"])
        store_type = st.selectbox("Store Type", ["Supermarket Type1", "Supermarket Type2", "Departmental Store", "Food Mart"])
        store_age = st.number_input("Store Age (Years)", min_value=1, max_value=50, value=15)

    if st.button("Predict Sales", type="primary"):
        input_data = {
            "Product_Weight": product_weight,
            "Product_Sugar_Content": product_sugar_content,
            "Product_Allocated_Area": product_allocated_area,
            "Product_MRP": product_mrp,
            "Store_Size": store_size,
            "Store_Location_City_Type": store_location,
            "Store_Type": store_type,
            "Product_Id_char": product_id_char,
            "Store_Age_Years": store_age,
            "Product_Type_Category": product_type_category,
        }
        try:
            response = requests.post(f"{BACKEND_URL}/predict", json=input_data, timeout=30)
            result = response.json()
            if result.get("status") == "success":
                st.success(f"Predicted Sales Revenue: {result['prediction']:,.2f}")
            else:
                st.error(f"Error: {result.get('error', 'Unknown error')}")
        except requests.exceptions.RequestException as e:
            st.error(f"Connection Error: {e}. Please ensure the backend is running.")

elif option == "Batch Prediction":
    st.header("Batch Sales Prediction")
    st.info("The CSV must contain: Product_Weight, Product_Sugar_Content, Product_Allocated_Area, "
            "Product_MRP, Store_Size, Store_Location_City_Type, Store_Type, Product_Id_char, "
            "Store_Age_Years, Product_Type_Category")

    uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("Preview of uploaded data:")
        st.dataframe(df.head())

        if st.button("Predict All", type="primary"):
            try:
                uploaded_file.seek(0)
                files = {"file": ("batch_data.csv", uploaded_file, "text/csv")}
                response = requests.post(f"{BACKEND_URL}/predict_batch", files=files, timeout=60)
                result = response.json()
                if result.get("status") == "success":
                    predictions_df = pd.DataFrame(result["predictions"])
                    st.success(f"Predictions generated for {result['count']} records.")
                    st.dataframe(predictions_df)
                    csv = predictions_df.to_csv(index=False)
                    st.download_button("Download Predictions", data=csv,
                                       file_name="superkart_predictions.csv", mime="text/csv")
                else:
                    st.error(f"Error: {result.get('error', 'Unknown error')}")
            except requests.exceptions.RequestException as e:
                st.error(f"Connection Error: {e}. Please ensure the backend is running.")
