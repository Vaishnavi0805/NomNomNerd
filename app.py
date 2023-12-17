import streamlit as st
from PIL import Image
import requests
from io import BytesIO
import ast
import google.generativeai as genai
import os
os.environ['GOOGLE_API_KEY'] = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key = os.environ['GOOGLE_API_KEY'])
# Load the Gemini model
vision_model = genai.GenerativeModel('gemini-pro-vision')

def generate_recipe_data(image, serving_size):
    # Generate content using the provided code
    generation_config = genai.GenerationConfig(temperature=0.1, max_output_tokens=2048)
    response = vision_model.generate_content(["""Please generate a list of the dish name,a list for the ingredients required to prepare it,adjust the ingredients for serving size for {serving_size} people, and the nutritional value of the ingredients.
                                                Additionally, please provide a list for detailed instructions to prepare the recipe step by step as follows:
                                                'Recipe steps':[Step 1:
                                                                    Step 2:
                                                                    Step n:]

                                                return the final response in below format and keep in mind to use measurements for protien - in grams, fats - in grams, calories - in calories and Quanity as required by the recipe given and also give the titles along with measurements for examp Quantity:val and so on :
                                                {
                                                    'name':['Name of the dish'],
                                                    'servig size':['Serving size mentioned']
                                                    'nutritional value and ingredients': {'ing1':['Quantity' :'val','Protien : 'val', 'Carbs': 'val','Fats' :'val','Calories' : 'val'],
                                                                                        'ing2':['Quantity:val','protien:val', 'carbs:val','fats:val','calories:val'],
                                                                                        'ing3':['Quantity:val','protien:val', 'carbs:val','fats:val','calories:val']},
                                                   'Recipe steps':[Step 1:
                                                                    Step 2:
                                                                    Step n:]
                                                }Very important: Make sure that your response starts from { and end with a }""", image], generation_config=generation_config)
    response.resolve()
    op1 = response.text
    response_string = op1.replace("", "\"\"\"")
    recipe_data = ast.literal_eval(response_string)
    return recipe_data

# Streamlit app
st.set_page_config(page_title="NomNomNerd 🍲", page_icon="🍔")

st.title("NomNomNerd ༼ つ ◕_◕ ༽つ🍰🍔🍕")

# Upload image
uploaded_image = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

# Specify serving size
serving_size = st.text_input("Enter Serving Size:")

if uploaded_image and serving_size is not None:
    # Display the uploaded image
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Generate recipe data on button click
    if st.button("Generate Recipe"):
        # Generate and display recipe data
        recipe_data = generate_recipe_data(image, serving_size)
        

        # If recipe_data is a string, convert it to a dictionary
        while not isinstance(recipe_data, dict):
            
            recipe_data_str = generate_recipe_data(image, serving_size)
            recipe_data_str = recipe_data_str.replace("", "\"\"\"")
            recipe_data_str=recipe_data_str.strip()
            recipe_data = ast.literal_eval(recipe_data_str)

        print(type(recipe_data))
        print(recipe_data)
        st.markdown(f"*{recipe_data['name'][0]}*")

        # Create a layout with dynamic number of columns
        num_columns = 4
        cols = [st.columns(num_columns) for _ in range((len(recipe_data['nutritional value and ingredients']) + num_columns - 1) // num_columns)]
        # Display nutritional value and ingredients in columns
        ingredient_nutrients = {}
        ingredients = list(recipe_data['nutritional value and ingredients'].keys())

        for col, chunk in zip(cols, [ingredients[i:i + num_columns] for i in range(0, len(ingredients), num_columns)]):
            for i, ingredient in enumerate(chunk):
                details = recipe_data['nutritional value and ingredients'][ingredient]
                nutrient_details = {}
                for nutrient in details:
                    # Check if the string contains ':'
                    if ':' in nutrient:
                        nutrient_name, nutrient_value = nutrient.split(':', 1)
                        nutrient_details[nutrient_name.strip()] = nutrient_value.strip()
                    else:
                        st.warning(f"Invalid format for nutrient ({nutrient}) in {ingredient}. Skipping.")
                ingredient_nutrients[ingredient] = nutrient_details

                # Display ingredients in a row
                col[i].write(f'  - {ingredient}:')
                for nutrient, value in nutrient_details.items():
                    col[i].write(f'    {nutrient}: {value}')


        # Display recipe steps in the right column
        st.markdown("&nbsp;")
        # st.markdown(f"*Recipe Steps*")
        st.markdown('<p class="big-font">Recipe Steps</p>', unsafe_allow_html=True)
        for step in recipe_data.get('Recipe steps') or recipe_data.get('recipe_steps'):
            st.write(step)
else:
    st.warning("Please upload an image.")