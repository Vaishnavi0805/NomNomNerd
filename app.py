from dotenv import load_dotenv
import os
import google.generativeai as genai
from io import BytesIO
from llama_index.multi_modal_llms.gemini import GeminiMultiModal
from PIL import Image
import requests
from io import BytesIO
import matplotlib.pyplot as plt
from llama_index.multi_modal_llms.generic_utils import (
    load_image_urls,
)
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
import streamlit as st
from PIL import Image
import ast
# Mock function to get dish information
def get_dish_info(num_people):
    image_urls = [
    "https://images.slurrp.com/prodarticles/5iyqpeyd4ec.webp",
    # Add yours here!
    ]
    image_documents = load_image_urls(image_urls)

    gemini_pro = GeminiMultiModal(model_name="models/gemini-pro-vision")
    img_response = requests.get(image_urls[0])
    print(image_urls[0])
    img = Image.open(BytesIO(img_response.content))
    plt.imshow(img)
    vision_model = genai.GenerativeModel('gemini-pro-vision')
    a=genai.GenerationConfig(temperature=0.1,
        max_output_tokens=2048)
    response = vision_model.generate_content(["""Please generate a list of the dish name,a list for the ingredients required to prepare it,adjust the ingredients for serving size for 60 people, and the nutritional value of the ingredients.
                                                Additionally, please provide a list for detailed instructions to prepare the recipe step by step as follows :
                                                Step 1:
                                                Step 2:
                                                Step n:

                                                return the final response in below format and keep in mind to use measurements for protien - in grams, fats - in grams, calories - in calories and Quanity as required by the recipe given :
                                                {
                                                    'name':['Name of the dish'],
                                                    'servig size':['Serving size mentioned']
                                                    'nutritional value and ingredients': {'ing1:['Quantity:','protien:', 'carbs:','fats:','calories:']',
                                                                                        'ing2:['Quantity:','protien:', 'carbs:','fats:','calories:']',
                                                                                        'ing3:['Quantity:','protien:', 'carbs:','fats:,calories:']'},
                                                    'Recipe steps':[Step 1:
                                                                    Step 2:
                                                                    Step n:]
                                                }""",img],generation_config =a)
    response.resolve()
    op1=response.text
    response_string = op1.replace("```", "\"\"\"")
    recipe_data = ast.literal_eval(response_string)
    print (recipe_data)



    # return "Spaghetti Bolognese", ["Pasta", "Tomato Sauce", "Beef", "Onion"], {"Calories": 500, "Protein": 20, "Carbs": 60}, "Cook the pasta, brown the beef, mix with sauce, and serve."

def main():
    st.title("Dish Information App")

    # Upload image
    uploaded_file = st.file_uploader("Choose an image of the dish", type=["jpg", "jpeg", "png"])

    # Get user input for the number of people
    num_people = st.text_input("Number of People to Prepare For", type="default")
    try:
        num_people = int(num_people)
    except ValueError:
        num_people = None
    
    # Display dish information only if both image and number of people are provided
    if uploaded_file is not None and num_people is not None:
        st.image(uploaded_file, caption="Uploaded Image.", use_column_width=True)

        # Get dish information
        dish_name, ingredients, nutritional_values, recipe = get_dish_info( num_people)

        # Display dish information
        st.subheader("Dish Information")
        st.write(f"**Dish Name:** {dish_name}")
        st.write(f"**Ingredients:** {', '.join(ingredients)}")
        st.write("**Nutritional Values:**")
        for nutrient, value in nutritional_values.items():
            st.write(f"- {nutrient}: {value}g")
        st.subheader("Recipe")
        st.write(recipe)

if __name__ == "__main__":
    main()