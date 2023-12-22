import streamlit as st
from PIL import Image
import ast
import google.generativeai as genai
import os
import json
from trulens_eval import Tru
tru = Tru()
from trulens_eval.tru_custom_app import instrument
from st_aggrid import AgGrid

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
        return op1
nomnomapp=App()
from trulens_eval import TruCustomApp
tru_app = TruCustomApp(nomnomapp, app_id = 'nomapp')

# Streamlit app
st.set_page_config(layout="wide", page_title="Recipe Magic", page_icon="🪄")

# Hero section
with st.container():
    st.markdown(f"<h1 style='font-family: {fontFamily}; color: {primaryColor}'>NomNomNerd ༼ つ ◕_◕ ༽つ🍰🍔🍕</h1>", unsafe_allow_html=True)
    # st.image('bg.png', width=800, output_format='auto')
    # st.image('bg.png', width=800, output_format='auto')
    col1, col2, col3,col4,col5 = st.columns([1,1,4,2,1])
    with col1:
        pass
    with col2:
        pass
    with col3:
        st.image("bg.png",width=800,output_format='auto')
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
        col1, col2, col3,col4,col5 = st.columns([1,3.5,4,3,1])

        with col1:
            pass
        with col2:
            pass
        with col3:
            st.image(image, caption="Uploaded Image", width=400)
        with col4:
            pass

        with col5:
            pass

        # Recipe generation button

        
        # Recipe generation button
        # Recipe generation button
        col1, col2, col3,col4,col5 = st.columns([1,1,1,5,5])
        
       
        with col1:
            pass
        with col2:
            darker_primary_color = "#E39B92"  # Adjust the color code to a slightly darker shade
            left_margin = "55px"  # Adjust the left margin as needed

            button_html = f"""
                <button class="button-34" style='background: {darker_primary_color}; border-radius: 999px; box-shadow: {darker_primary_color} 0 10px 20px -10px;
                    box-sizing: border-box; color: #FFFFFF; cursor: pointer; font-family: Inter,Helvetica,"Apple Color Emoji","Segoe UI Emoji",
                    NotoColorEmoji,"Noto Color Emoji","Segoe UI Symbol","Android Emoji",EmojiSymbols,-apple-system,system-ui,"Segoe UI",
                    Roboto,"Helvetica Neue","Noto Sans",sans-serif; font-size: 16px; font-weight: 700; line-height: 24px; opacity: 1;
                    outline: 0 solid transparent; padding: 8px 18px; user-select: none; -webkit-user-select: none; touch-action: manipulation;
                    width: fit-content; word-break: break-word; border: 0; margin-left: {left_margin};'>
                    Get Cooking!
                </button>
            """
        with col3:
            pass
        with col4:
            pass
        with col5:
            pass

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
                    human_feedback = None

                    # Initialize feedback variable
                    col1, col2,col3,col4 = st.columns([5.5,1,2,5])

                     # Define Streamlit buttons in the columns
                    
                    with col1:
                        pass

                    thumbs_up_button = col2.button('Like👍', key="thumbs_up")
                    thumbs_down_button = col3.button('Dislike👎', key="thumbs_down")
                    with col4:
                        pass

        # Custom HTML and CSS to adjust button positioning
                    st.markdown("""
                    <style>
                        .stButton>button {
                            margin: 0 5px;  /* Adjust the margin to bring buttons closer together */
                        }
                    </style>
                    """, unsafe_allow_html=True)

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
                        

