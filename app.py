import streamlit as st
from PIL import Image
import ast
import google.generativeai as genai
import os
import json

# Set Google API key
os.environ['GOOGLE_API_KEY'] = st.secrets['GOOGLE_API_KEY']
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])


# Load the Gemini model
vision_model = genai.GenerativeModel('gemini-pro-vision')

# Define custom colors and fonts
primaryColor = "#F7CAC9"
secondaryColor = "#FADEAD"
accentColor = "#FFAC81"
fontFamily = "Raleway"

def generate_recipe_data(image, serving_size):
    generation_config = genai.GenerationConfig(temperature=0.1, max_output_tokens=2048)
    response = vision_model.generate_content(["""Please generate a list of the dish name,a list for the ingredients required to prepare it,adjust the ingredients for serving size for {serving_size} people, and the nutritional value of the ingredients.
        Additionally, please provide a list for detailed instructions to prepare the recipe step by step as follows :
        Step 1:
        Step 2:
        Step n:

        return the final response in below format and keep in mind to use measurements for protein - in grams, fats - in grams, calories - in calories and Quantity as required by the recipe given :
        {
            'name':['Name of the dish'],
            'serving size':['Serving size mentioned']
            'nutritional value and ingredients': {'ing1':['Quantity:','protein:', 'carbs:','fats:','calories:']',
                                                   'ing2':['Quantity:','protein:', 'carbs:','fats:,calories:']',
                                                   'ing3':['Quantity:','protein:', 'carbs:','fats:,calories:']},
            'Recipe steps':['Step 1: step',
                            'Step 2: step',
                            'Step n: step']
        } Very important: Make sure that your response starts from { and end with a }""", image], generation_config=generation_config)
    response.resolve()
    op1 = response.text
    print (op1)
    return op1

# Streamlit app
st.set_page_config(layout="wide", page_title="Recipe Magic", page_icon="🪄")

# Hero section
with st.container():
    st.markdown(f"<h1 style='font-family: {fontFamily}; color: {primaryColor}'>NomNomNerd ༼ つ ◕_◕ ༽つ🍰🍔🍕</h1>", unsafe_allow_html=True)
    # st.image('bg.png', width=800, output_format='auto')
    # st.image('bg.png', width=800, output_format='auto')
    col1, col2, col3,col4,col5 = st.columns([1,1,6,1,1])

    with col1:
        st.write("")
    with col2:
        st.write("")
    with col3:
        st.image("bg.png")

    with col4:
        st.write("")

    with col5:
        st.write("")


# Image upload and serving size section
with st.container():
    st.markdown("<style>div{text-align:center;}</style>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown(f"<h3 style='font-family: {fontFamily}; color: {primaryColor}'>Upload your food picture:</h3>", unsafe_allow_html=True)
    uploaded_image = st.file_uploader("", type=["jpg", "jpeg", "png"])
    st.markdown(f"<p style='font-family: {fontFamily}; color: {primaryColor}'>Number of people eating:</p>", unsafe_allow_html=True)
    serving_size = st.number_input("", min_value=1, value=1)

# Display uploaded image and recipe generation button
with st.container():
    if uploaded_image is not None:
        # Display uploaded image
        image = Image.open(uploaded_image)
        st.image(image, caption="Uploaded Image", width=400)

        # Recipe generation button
        button_html = f"<button style='background-color: {accentColor}; color: white; font-family: {fontFamily}'>Get Cooking!</button>"
        if st.markdown(button_html, unsafe_allow_html=True):
            recipe_data = None
            while not isinstance(recipe_data, dict):
                recipe_data_str = generate_recipe_data(image, serving_size)
                recipe_data_str = recipe_data_str.replace("```", "\"\"\"")
                recipe_data_str = recipe_data_str.strip()
                recipe_data = ast.literal_eval(recipe_data_str)

            # Display recipe data
            with st.container():
                st.markdown("<style>div{text-align:center;}</style>", unsafe_allow_html=True)
                st.markdown("---")

                # Display recipe name with formatting
                st.markdown(f"<h2 style='font-family: {fontFamily}; color: {primaryColor}'>Delicious {recipe_data['name'][0]}</h2>", unsafe_allow_html=True)

                # Display serving size
                st.write(f"Serving size: {recipe_data['serving size'][0]} people", font_family=fontFamily)

                # Display nutritional value and ingredients
                st.markdown(f"<h3 style='font-family: {fontFamily}; color: {primaryColor}'>Ingredients and Nutrition:</h3>", unsafe_allow_html=True)

                for ingredient, values in recipe_data["nutritional value and ingredients"].items():
                    # Display ingredient name and quantity
                    st.write(f"- **{ingredient}**: {values[0]}", font_family=fontFamily)

                    # Create string with nutritional values using string formatting
                    nutritional_info = f"\tProtein: {values[1]}, Carbs: {values[2]}, Fats: {values[3]}, Calories: {values[4]}"
                    st.write(nutritional_info, font_family=fontFamily)

                # Display recipe steps
                st.markdown(f"<h3 style='font-family: {fontFamily}; color: {primaryColor}'>Steps:</h3>", unsafe_allow_html=True)
                for i, step in enumerate(recipe_data["Recipe steps"]):
                    st.write(f"- {step}", font_family=fontFamily)
