import os
import base64
import time
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.efficientnet import preprocess_input
from prometheus_client import start_http_server, Summary, Counter, Gauge, Info
import gradio as gr

# -----------------------------------------
# MODEL & CONFIG
# -----------------------------------------
MODEL_PATH = "model/ingredient_classifier_effnet.keras"   # Inside Docker container
RECIPE_IMAGE_FOLDER = "recipe_images"                     # Inside Docker container

class_names = ["bread", "cheese", "egg", "onion", "potato", "rice", "tomato"]
IMG_SIZE = (224, 224)

# Load model once
model = tf.keras.models.load_model(MODEL_PATH, compile=False)


# -----------------------------------------
# PROMETHEUS METRICS
# -----------------------------------------

# Use a unique feedback_id to ensure each feedback is a separate time series
feedback_comment_counter = Counter(
    "wastenot_feedback_comment_total",
    "Counts user feedback comments",
    ["predicted_ingredient", "feedback_type", "comment", "feedback_id"]  # Added feedback_id
)

prediction_counter = Counter(
    'wastenot_predictions_total',
    'Total predictions made',
    ['ingredient']
)

prediction_confidence_gauge = Gauge(
    'wastenot_prediction_confidence',
    'Confidence score of each prediction'
)

request_time = Summary(
    'wastenot_prediction_request_seconds',
    'Time spent processing prediction'
)

feedback_counter = Counter(
    'wastenot_feedback_total',
    'User feedback entries collected',
    ['feedback_type', 'predicted_ingredient']
)

# Start metrics server
start_http_server(8000)


# -----------------------------------------
# MODEL PREDICTION FUNCTION
# -----------------------------------------
@request_time.time()
def predict_ingredient(img):
    img = img.resize(IMG_SIZE)
    img_array = image.img_to_array(img)
    img_array = preprocess_input(img_array)
    img_array = np.expand_dims(img_array, axis=0)

    preds = model.predict(img_array)[0]
    index = np.argmax(preds)
    ingredient = class_names[index]
    confidence = float(preds[index])

    # Unknown image handling
    if confidence < 0.60:
        ingredient = "unknown"

    # Update metrics
    prediction_counter.labels(ingredient=ingredient).inc()
    prediction_confidence_gauge.set(confidence)

    return ingredient, confidence


# -----------------------------------------
# RECIPE DATABASE (NEW LOCAL PATHS)
# -----------------------------------------
def recipe_image(name):
    return f"{RECIPE_IMAGE_FOLDER}/{name}"

RECIPE_DB = [
    {
        "name": "Cheese Omelette",
        "ingredients": ["egg", "cheese"],
        "image": recipe_image("Cheese Omelette.webp"),
        "description": "Soft, cheesy omelette perfect for breakfast.",
        "ingredients_full": [
            "2 eggs", "1/4 cup shredded cheese", "Salt and pepper"
        ],
        "steps_full": [
            "Beat eggs with salt and pepper.",
            "Pour into a hot pan.",
            "Sprinkle cheese on top.",
            "Fold and serve immediately."
        ],
        "nutrition": {"Calories": "260 kcal", "Protein": "14g", "Carbs": "2g", "Fat": "22g"},
        "time": "8 min",
        "servings": "1"
    },
    {
        "name": "Cheese Stuffed Bread Rolls",
        "ingredients": ["bread", "cheese"],
        "image": recipe_image("Cheese Stuffed Bread Rolls.jpeg"),
        "description": "Soft bread rolls filled with melted cheese.",
        "ingredients_full": [
            "6 bread slices", "1 cup shredded cheese",
            "1 egg (for brushing)", "1 tsp mixed herbs"
        ],
        "steps_full": [
            "Flatten bread slices.",
            "Place cheese in the center and roll tightly.",
            "Brush with egg and herbs.",
            "Bake at 350°F for 10 minutes."
        ],
        "nutrition": {"Calories": "280 kcal", "Protein": "11g", "Carbs": "22g", "Fat": "17g"},
        "time": "20 min",
        "servings": "6"
    },
    {
        "name": "Cheesy Potato Casserole",
        "ingredients": ["potato", "cheese", "onion"],
        "image": recipe_image("Cheesy Potato Casserole.webp"),
        "description": "Creamy, cheesy potato casserole with onions.",
        "ingredients_full": [
            "4 potatoes", "1 onion", "1 cup shredded cheese",
            "1/2 cup cream", "2 tbsp butter"
        ],
        "steps_full": [
            "Layer potatoes, onions, and cheese.",
            "Pour cream over the top.",
            "Bake at 375°F for 1 hour."
        ],
        "nutrition": {"Calories": "380 kcal", "Protein": "10g", "Carbs": "40g", "Fat": "22g"},
        "time": "75 min",
        "servings": "6"
    },
    {
        "name": "Egg and Potato Breakfast Bake",
        "ingredients": ["potato", "egg", "cheese"],
        "image": recipe_image("Egg and Potato Breakfast Bake.jpeg"),
        "description": "Layered potatoes, eggs, and cheese baked to perfection.",
        "ingredients_full": [
            "4 potatoes", "6 eggs", "1 cup shredded cheese",
            "1/2 cup milk", "Salt and pepper"
        ],
        "steps_full": [
            "Layer sliced potatoes in a dish.",
            "Pour beaten egg mixture on top.",
            "Sprinkle cheese.",
            "Bake at 375°F for 40 minutes."
        ],
        "nutrition": {"Calories": "320 kcal", "Protein": "16g", "Carbs": "28g", "Fat": "17g"},
        "time": "50 min",
        "servings": "6"
    },
    {
        "name": "Egg Fried Rice",
        "ingredients": ["rice", "egg", "onion"],
        "image": recipe_image("Egg Fried Rice.jpeg"),
        "description": "Quick fried rice with egg and onions.",
        "ingredients_full": [
            "1 cup cooked rice", "2 eggs", "1/4 onion",
            "1 tsp soy sauce", "Salt and pepper"
        ],
        "steps_full": [
            "Scramble eggs and set aside.",
            "Stir-fry onions.",
            "Add rice and soy sauce.",
            "Mix in eggs and serve."
        ],
        "nutrition": {"Calories": "280 kcal", "Protein": "10g", "Carbs": "38g", "Fat": "8g"},
        "time": "12 min",
        "servings": "1"
    },
    {
        "name": "French Toast",
        "ingredients": ["bread", "egg"],
        "image": recipe_image("French Toast.jpeg"),
        "description": "Sweet, golden French toast.",
        "ingredients_full": [
            "4 bread slices", "2 eggs", "1/4 cup milk",
            "1 tbsp sugar", "1/2 tsp cinnamon"
        ],
        "steps_full": [
            "Whisk eggs, milk, sugar, cinnamon.",
            "Dip bread slices.",
            "Pan-fry until golden."
        ],
        "nutrition": {"Calories": "340 kcal", "Protein": "12g", "Carbs": "38g", "Fat": "16g"},
        "time": "15 min",
        "servings": "2"
    },
    {
        "name": "Grilled Cheese Sandwich",
        "ingredients": ["bread", "cheese"],
        "image": recipe_image("Grilled Cheese Sandwich.jpeg"),
        "description": "Classic grilled cheese sandwich.",
        "ingredients_full": [
            "2 slices bread", "2 slices cheese", "1 tbsp butter"
        ],
        "steps_full": [
            "Butter bread slices.",
            "Place cheese in between.",
            "Grill until golden."
        ],
        "nutrition": {"Calories": "350 kcal", "Protein": "13g", "Carbs": "30g", "Fat": "19g"},
        "time": "10 min",
        "servings": "1"
    },
    {
        "name": "Onion Rice Pilaf",
        "ingredients": ["rice", "onion"],
        "image": recipe_image("Onion Rice Pilaf.jpeg"),
        "description": "Fluffy rice with sautéed onions.",
        "ingredients_full": [
            "1 cup rice", "1 onion", "2 cups broth",
            "1 tbsp butter", "Salt and pepper"
        ],
        "steps_full": [
            "Sauté onions.",
            "Toast rice.",
            "Add broth and cook."
        ],
        "nutrition": {"Calories": "210 kcal", "Protein": "4g", "Carbs": "40g", "Fat": "4g"},
        "time": "30 min",
        "servings": "2"
    },
    {
        "name": "Tomato Bread Soup",
        "ingredients": ["bread", "tomato", "onion"],
        "image": recipe_image("Tomato Bread Soup.jpeg"),
        "description": "Comforting tomato and bread soup.",
        "ingredients_full": [
            "6 tomatoes", "1 onion", "4 cups broth",
            "2 cups bread cubes", "Olive oil"
        ],
        "steps_full": [
            "Sauté onions.",
            "Add tomatoes and cook down.",
            "Add broth and bread.",
            "Simmer and serve."
        ],
        "nutrition": {"Calories": "220 kcal", "Protein": "6g", "Carbs": "35g", "Fat": "7g"},
        "time": "35 min",
        "servings": "6"
    },
    {
        "name": "Tomato Cheese Toast",
        "ingredients": ["bread", "cheese", "tomato"],
        "image": recipe_image("Tomato Cheese Toast.jpeg"),
        "description": "Open toast with cheese and tomatoes.",
        "ingredients_full": [
            "4 slices bread", "2 tomatoes", "1 cup cheese"
        ],
        "steps_full": [
            "Add tomatoes on bread.",
            "Sprinkle cheese.",
            "Toast until melted."
        ],
        "nutrition": {"Calories": "250 kcal", "Protein": "10g", "Carbs": "20g", "Fat": "15g"},
        "time": "10 min",
        "servings": "4"
    },
    {
        "name": "Tomato Omelette",
        "ingredients": ["egg", "tomato", "onion"],
        "image": recipe_image("Tomato Omelette.jpeg"),
        "description": "A fluffy tomato omelette.",
        "ingredients_full": [
            "2 eggs", "1 tomato", "1/4 onion"
        ],
        "steps_full": [
            "Beat eggs.",
            "Add chopped tomato & onion.",
            "Cook both sides."
        ],
        "nutrition": {"Calories": "210 kcal", "Protein": "12g", "Carbs": "4g", "Fat": "17g"},
        "time": "10 min",
        "servings": "1"
    },
    {
        "name": "Tomato Rice Soup",
        "ingredients": ["rice", "tomato"],
        "image": recipe_image("Tomato Rice Soup.jpeg"),
        "description": "Warm tomato soup with rice.",
        "ingredients_full": [
            "1 cup rice", "4 tomatoes", "4 cups broth"
        ],
        "steps_full": [
            "Sauté onion and garlic.",
            "Add tomatoes.",
            "Add broth and rice.",
            "Simmer 20 minutes."
        ],
        "nutrition": {"Calories": "210 kcal", "Protein": "4g", "Carbs": "40g", "Fat": "5g"},
        "time": "35 min",
        "servings": "4"
    },
    {
        "name": "Tomato Rice",
        "ingredients": ["rice", "tomato", "onion"],
        "image": recipe_image("Tomato Rice.jpeg"),
        "description": "Comforting tomato rice.",
        "ingredients_full": [
            "1 cup rice", "2 tomatoes", "1 onion"
        ],
        "steps_full": [
            "Cook tomatoes and onions.",
            "Mix with cooked rice."
        ],
        "nutrition": {"Calories": "220 kcal", "Protein": "4g", "Carbs": "42g", "Fat": "5g"},
        "time": "25 min",
        "servings": "2"
    }
]


# -----------------------------------------
# FORMAT RECIPE CARD (HTML)
# -----------------------------------------
def format_recipe(recipe):
    try:
        with open(recipe['image'], "rb") as img_file:
            img_data = base64.b64encode(img_file.read()).decode('utf-8')

        ext = recipe['image'].split(".")[-1].lower()
        img_type = "jpeg" if ext in ["jpg", "jpeg"] else ext

        img_src = f"data:image/{img_type};base64,{img_data}"

    except Exception:
        img_src = "https://via.placeholder.com/320x200?text=Image+Unavailable"

    html = f"""
    <div style="font-family: Arial; padding: 10px; border:1px solid #ddd; border-radius:10px; margin-bottom:25px;">
        <h2 style="color:#d35400;">{recipe['name']}</h2>
        <img src="{img_src}" style="width: 320px; border-radius: 10px; margin-bottom: 10px;">
        <h3>Description</h3>
        <p>{recipe['description']}</p>
        <h3>Ingredients</h3>
        <ul>{''.join([f'<li>{i}</li>' for i in recipe['ingredients_full']])}</ul>
        <h3>Steps</h3>
        <ol>{''.join([f'<li>{s}</li>' for s in recipe['steps_full']])}</ol>
        <h3>Nutrition</h3>
        <ul>{''.join([f'<li>{k}: {v}</li>' for k,v in recipe['nutrition'].items()])}</ul>
        <p><b>Prep Time:</b> {recipe['time']}</p>
        <p><b>Servings:</b> {recipe['servings']}</p>
    </div>
    """
    return html


# -----------------------------------------
# MATCH RECIPES
# -----------------------------------------
def match_recipes(ingredients):
    best = []
    for recipe in RECIPE_DB:
        score = len(set(recipe["ingredients"]) & set(ingredients))
        if score > 0:
            best.append((score, recipe))

    best.sort(key=lambda x: x[0], reverse=True)
    return [r for _, r in best]


# -----------------------------------------
# PROCESS UPLOADED IMAGES
# -----------------------------------------
def process_images(files):
    if not files:
        return "<h3>Please upload ingredient images.</h3>"

    detected = []
    html_images = "<div style='display:flex; flex-wrap:wrap; gap:10px;'>"

    for file_path in files:
        img = image.load_img(file_path, target_size=IMG_SIZE)
        ingredient, conf = predict_ingredient(img)

        # Convert to Base64 for UI display
        with open(file_path, "rb") as f:
            img_data = base64.b64encode(f.read()).decode("utf-8")

        ext = file_path.split(".")[-1].lower()
        img_type = "jpeg" if ext in ["jpg", "jpeg"] else ext

        color = "green" if ingredient != "unknown" else "red"

        html_images += f"""
        <div style='border:1px solid #ddd; border-radius:8px; padding:8px; text-align:center;'>
            <img src='data:image/{img_type};base64,{img_data}'
                 style='width:150px; height:150px; object-fit:cover; border-radius:4px;'>
            <p style='color:{color}; margin-top:5px;'>{ingredient} ({conf:.2f})</p>
        </div>
        """

        if ingredient != "unknown":
            detected.append(ingredient)

    html_images += "</div>"

    if not detected:
        return "<h3>No valid ingredients detected.</h3>" + html_images

    recommendations = match_recipes(list(set(detected)))

    final_html = f"<h2>Detected Ingredients: {', '.join(detected)}</h2>" + html_images
    final_html += "<h2>Recommended Recipes:</h2>"

    for r in recommendations:
        final_html += format_recipe(r)

    return final_html


# -----------------------------------------
# USER FEEDBACK METRICS (FIXED)
# -----------------------------------------
def collect_feedback(predicted, feedback_type, comment_text):
    # Generate a unique feedback ID using timestamp
    feedback_id = str(int(time.time() * 1000))  # Millisecond timestamp as unique ID
    
    # Record good/bad feedback
    feedback_counter.labels(
        feedback_type=feedback_type,
        predicted_ingredient=predicted
    ).inc()

    # Record user comment with unique feedback_id
    feedback_comment_counter.labels(
        predicted_ingredient=predicted,
        feedback_type=feedback_type,
        comment=comment_text.strip(),
        feedback_id=feedback_id  # This makes each feedback entry unique
    ).inc()

    return "Thank you for your feedback!"



# -----------------------------------------
# GRADIO UI
# -----------------------------------------
with gr.Blocks() as main_ui:
    gr.Markdown("# 🥕 WasteNot Ingredient App")
    gr.Markdown("Upload your ingredient images to get recipe suggestions.")

    upload = gr.File(type="filepath", file_count="multiple", label="Upload Ingredient Images")
    output_html = gr.HTML()

    btn = gr.Button("Get Recipes")
    btn.click(process_images, inputs=upload, outputs=output_html)

feedback_ui = gr.Interface(
    fn=collect_feedback,
    inputs=[gr.Textbox("Predicted Ingredient"),
            gr.Radio(["Good", "Bad"], label="Feedback Type"),
            gr.Textbox("Additional Feedback")],
    outputs="text",
    title="Feedback Collector"
)

gr.TabbedInterface(
    [main_ui, feedback_ui],
    ["Ingredient Detector", "Feedback"]
).launch(server_name="0.0.0.0", server_port=7860)
