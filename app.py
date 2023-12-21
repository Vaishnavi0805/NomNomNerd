import streamlit as st
from PIL import Image
import ast
import google.generativeai as genai
import os
import json
from trulens_eval import Tru
tru = Tru()
tru.reset_database()
from trulens_eval.tru_custom_app import instrument

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
class App:  
    @instrument
    def generate_recipe_data(self,image, serving_size):
        generation_config = genai.GenerationConfig(temperature=0.1, max_output_tokens=2048)
        response = vision_model.generate_content(["""Please generate a list of the dish name,a list for the ingredients required to prepare it,adjust the ingredients for serving size for %s people, and the nutritional value of the ingredients.
            Additionally, please provide a list for detailed instructions to prepare the recipe step by step

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
            } Very important: Make sure that your response starts from { and end with a }
            Note:If any food item is not present in the image return a message saying 'The uploaded image may not contain recognizable food. Please upload an image of food. ' string""" % (serving_size), image], generation_config=generation_config)
        response.resolve()
        op1 = response.text
        print (op1)
        return op1
nomnomapp=App()
from trulens_eval import TruCustomApp
tru_app = TruCustomApp(nomnomapp, app_id = 'nomapp',initial_app_loader=App)

# Streamlit app
st.set_page_config(layout="wide", page_title="Recipe Magic", page_icon="🪄")

# Hero section
with st.container():
    st.markdown(f"<h1 style='font-family: {fontFamily}; color: {primaryColor}'>NomNomNerd ༼ つ ◕_◕ ༽つ🍰🍔🍕</h1>", unsafe_allow_html=True)
    # st.image('bg.png', width=800, output_format='auto')
    # st.image('bg.png', width=800, output_format='auto')
    col1, col2, col3,col4,col5 = st.columns([1,1,6,1,1])

    with col1:
        pass
    with col2:
        pass
    with col3:
        st.image("bg.png")

    with col4:
        pass

    with col5:
        pass


# Image upload and serving size section
with st.container():
    st.markdown("<style>div{text-align:center;}</style>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown(f"<h3 style='font-family: {fontFamily}; color: {primaryColor}'>Upload your food picture:</h3>", unsafe_allow_html=True)
    uploaded_image = st.file_uploader("", type=["jpg", "jpeg", "png"])
    st.markdown(f"<p style='font-family: {fontFamily}; color: {primaryColor}'>Number of people eating:</p>", unsafe_allow_html=True)
    serving_size = st.text_input("")

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
                recipe_data_str = nomnomapp.generate_recipe_data(image, serving_size)
                if "The uploaded image may not contain recognizable food" in recipe_data_str:
                    st.warning("The uploaded image may not contain recognizable food. Please upload an image of food.")
                    break
                
                else:
                    recipe_data_str = recipe_data_str.replace("```", "\"\"\"")
                    recipe_data_str = recipe_data_str.strip()
                    recipe_data = ast.literal_eval(recipe_data_str)

            # Display recipe data
            if type(recipe_data)==dict:
                with st.container():
                    st.markdown("<style>div{text-align:center;}</style>", unsafe_allow_html=True)
                    st.markdown("---")

                    # Display recipe name with formatting
                    st.markdown(f"<h2 style='font-family: {fontFamily}; color: {primaryColor}'> {recipe_data['name'][0]}</h2>", unsafe_allow_html=True)
                
                    # Initialize feedback variable
                    human_feedback = None

                    # Define Streamlit buttons
                    thumbs_up_button = st.button('Like👍')
                    thumbs_down_button = st.button('Dislike👎')

                    # Function to handle thumbs up button click
                    def on_thumbs_up_button_clicked():
                        global human_feedback
                        human_feedback = "1"

                    # Function to handle thumbs down button click
                    def on_thumbs_down_button_clicked():
                        global human_feedback
                        human_feedback = "0"

                    # Assign button click functions to Streamlit buttons
                    if thumbs_up_button:
                        on_thumbs_up_button_clicked()

                    if thumbs_down_button:
                        on_thumbs_down_button_clicked()

                    print("HUMAN FEEDBACK:",human_feedback)

                    # Display serving size
                    st.write(f"Serving size: {recipe_data['serving size'][0]}")

                    # Display nutritional value and ingredients
                    st.markdown(f"<h3 style='font-family: {fontFamily}; color: {primaryColor}'>Ingredients and Nutrition:</h3>", unsafe_allow_html=True)

                    for ingredient, values in recipe_data["nutritional value and ingredients"].items():
                        # Display ingredient name and quantity
                        st.write(f"- *{ingredient}*: {values[0]}")

                        # Create string with nutritional values using string formatting
                        nutritional_info = f"\tProtein: {values[1]}, Carbs: {values[2]}, Fats: {values[3]}, Calories: {values[4]}"
                        st.write(nutritional_info)

                    # Display recipe steps
                    st.markdown(f"<h3 style='font-family: {fontFamily}; color: {primaryColor}'>Steps:</h3>", unsafe_allow_html=True)
                    for i, step in enumerate(recipe_data["Recipe steps"]):
                        st.write(f"- {step}")
                        # st.write(f"- {step}")
                    with tru_app as recording:
                        nomnomapp.generate_recipe_data(image,serving_size)
                        records, feedback = tru.get_records_and_feedback(app_ids=["nomapp"])
                        print("------")
                        print(type(records))
                        print("Records:",records)
                        records.to_csv('records.csv')
                        print("------")
                        print(type(feedback))
                        print("Feedback:",feedback)
                        record_id = records.record_id[-1:].values[0]
                    if human_feedback != None :
                        # add the human feedback to a particular app and record
                        tru.add_feedback(
                                        name="Human Feedack",
                                        record_id=record_id,
                                        app_id=tru_app.app_id,
                                        result=human_feedback
                        )
                        tru.get_leaderboard(app_ids=[tru_app.app_id])
                        tru.run_dashboard()

