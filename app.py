import gradio as gr
import json
import os
import subprocess
import re
from pathlib import Path
from datetime import datetime
import anthropic
from openai import OpenAI

# ==============================
# 🔧 Internal Config (Hidden)
# ==============================
YOLO_WEIGHTS_PATH = "YOLOV7_version_3.pt"
YOLO_DETECT_SCRIPT = "detect.py"
CONFIDENCE_THRESHOLD = 0.5
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")  # Secret key from environment (safe for hosting)
# ==============================

DATABASE_FILE = "recipe_database.json"

# Initial recipe database
INITIAL_RECIPES = [
    {
        "id": 1,
        "name": "Classic Margherita Pizza",
        "ingredients": ["flour", "yeast", "tomato", "mozzarella", "basil", "olive oil"],
        "instructions": ["Mix flour and yeast with water", "Let dough rise for 1 hour", "Roll out dough", "Add tomato sauce and cheese", "Bake at 450°F for 12-15 minutes", "Garnish with fresh basil"],
        "cookTime": 30,
        "difficulty": "medium",
        "servings": 4,
        "calories": 266,
        "protein": 11,
        "cuisine": "Italian",
        "dietary": ["vegetarian"],
        "rating": 4.5
    },
    {
        "id": 2,
        "name": "Chicken Stir Fry",
        "ingredients": ["chicken", "soy sauce", "ginger", "garlic", "bell pepper", "onion", "rice"],
        "instructions": ["Cut chicken into strips", "Heat oil in wok", "Cook chicken until golden", "Add vegetables", "Add soy sauce and ginger", "Serve over rice"],
        "cookTime": 20,
        "difficulty": "easy",
        "servings": 4,
        "calories": 320,
        "protein": 28,
        "cuisine": "Asian",
        "dietary": ["gluten-free"],
        "rating": 4.7
    },
    {
        "id": 3,
        "name": "Vegetable Curry",
        "ingredients": ["potato", "carrot", "peas", "coconut milk", "curry powder", "onion", "garlic", "ginger"],
        "instructions": ["Sauté onions and garlic", "Add curry powder and ginger", "Add vegetables and cook", "Pour coconut milk", "Simmer for 20 minutes", "Serve with rice"],
        "cookTime": 35,
        "difficulty": "easy",
        "servings": 6,
        "calories": 180,
        "protein": 5,
        "cuisine": "Indian",
        "dietary": ["vegetarian", "vegan", "gluten-free"],
        "rating": 4.6
    },
    {
        "id": 4,
        "name": "Caesar Salad",
        "ingredients": ["romaine lettuce", "parmesan", "croutons", "egg", "lemon", "garlic", "olive oil"],
        "instructions": ["Wash and chop lettuce", "Make dressing with egg, lemon, garlic", "Toss lettuce with dressing", "Add parmesan and croutons", "Serve immediately"],
        "cookTime": 15,
        "difficulty": "easy",
        "servings": 4,
        "calories": 184,
        "protein": 7,
        "cuisine": "American",
        "dietary": ["vegetarian"],
        "rating": 4.3
    },
    {
        "id": 5,
        "name": "Spaghetti Carbonara",
        "ingredients": ["spaghetti", "bacon", "egg", "parmesan", "black pepper", "garlic"],
        "instructions": ["Cook spaghetti", "Fry bacon until crispy", "Mix eggs and parmesan", "Combine hot pasta with egg mixture", "Add bacon and pepper", "Serve immediately"],
        "cookTime": 25,
        "difficulty": "medium",
        "servings": 4,
        "calories": 420,
        "protein": 18,
        "cuisine": "Italian",
        "dietary": [],
        "rating": 4.8
    },
    {
        "id": 6,
        "name": "Lentil Soup",
        "ingredients": ["lentils", "carrot", "celery", "onion", "garlic", "tomato", "vegetable broth"],
        "instructions": ["Sauté vegetables", "Add lentils and broth", "Simmer for 30 minutes", "Season to taste", "Serve hot"],
        "cookTime": 45,
        "difficulty": "easy",
        "servings": 6,
        "calories": 165,
        "protein": 12,
        "cuisine": "Mediterranean",
        "dietary": ["vegetarian", "vegan", "gluten-free"],
        "rating": 4.4
    },
    {
        "id": 7,
        "name": "Beef Tacos",
        "ingredients": ["ground beef", "taco seasoning", "tortilla", "lettuce", "tomato", "cheese", "sour cream"],
        "instructions": ["Brown ground beef", "Add taco seasoning", "Warm tortillas", "Assemble tacos with toppings", "Serve with lime"],
        "cookTime": 20,
        "difficulty": "easy",
        "servings": 4,
        "calories": 340,
        "protein": 22,
        "cuisine": "Mexican",
        "dietary": [],
        "rating": 4.6
    },
    {
        "id": 8,
        "name": "Greek Salad",
        "ingredients": ["cucumber", "tomato", "feta", "olive", "red onion", "olive oil", "lemon"],
        "instructions": ["Chop vegetables", "Crumble feta", "Mix all ingredients", "Dress with olive oil and lemon", "Serve chilled"],
        "cookTime": 10,
        "difficulty": "easy",
        "servings": 4,
        "calories": 145,
        "protein": 5,
        "cuisine": "Greek",
        "dietary": ["vegetarian", "gluten-free"],
        "rating": 4.5
    },
    {
        "id": 9,
        "name": "Pad Thai",
        "ingredients": ["rice noodles", "shrimp", "egg", "peanuts", "bean sprouts", "lime", "fish sauce", "tamarind"],
        "instructions": ["Soak noodles", "Scramble eggs", "Cook shrimp", "Stir fry noodles with sauce", "Add peanuts and sprouts", "Serve with lime"],
        "cookTime": 25,
        "difficulty": "medium",
        "servings": 4,
        "calories": 375,
        "protein": 20,
        "cuisine": "Thai",
        "dietary": ["gluten-free"],
        "rating": 4.7
    },
    {
        "id": 10,
        "name": "Mushroom Risotto",
        "ingredients": ["arborio rice", "mushroom", "onion", "white wine", "parmesan", "butter", "vegetable broth"],
        "instructions": ["Sauté mushrooms", "Toast rice", "Add wine", "Gradually add broth, stirring", "Finish with butter and parmesan", "Serve immediately"],
        "cookTime": 40,
        "difficulty": "hard",
        "servings": 4,
        "calories": 310,
        "protein": 9,
        "cuisine": "Italian",
        "dietary": ["vegetarian"],
        "rating": 4.6
    }
]

# Initialize database
def initialize_database():
    if not os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, 'w') as f:
            json.dump(INITIAL_RECIPES, f, indent=2)

def load_database():
    with open(DATABASE_FILE, 'r') as f:
        return json.load(f)

def save_to_database(recipe):
    recipes = load_database()
    recipe['id'] = max([r['id'] for r in recipes], default=0) + 1
    recipe['timestamp'] = datetime.now().isoformat()
    recipes.append(recipe)
    with open(DATABASE_FILE, 'w') as f:
        json.dump(recipes, f, indent=2)
    return recipe

# YOLOv7 Detection
# YOLOv7 Detection - FIXED VERSION
def detect_ingredients_from_image(image_path, yolo_weights_path, yolo_detect_script, confidence=0.5):
    """
    Run YOLOv7 detection on an image and extract detected ingredients
    """
    try:
        # Create temp directory for results
        output_dir = "yolo_temp_output"
        os.makedirs(output_dir, exist_ok=True)
        
        # Run YOLOv7 detection
        cmd = [
            "python",
            yolo_detect_script,
            
            "--weights", yolo_weights_path,
            "--source", image_path,
            "--conf", str(confidence),
            "--project", output_dir,
            "--name", "detection",
            "--exist-ok",
            "--nosave"  # Don't save images to speed up
        ]
        
        # Run the command and capture output
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        # Combine stdout and stderr
        output_text = result.stdout + result.stderr
        
        # Parse the detection output
        # Looking for pattern like: "1 apple, 1 avocado, 1 banana, Done."
        detected_ingredients = []
        
        # Split by lines and look for the detection line
        lines = output_text.split('\n')
        for line in lines:
            # The detection line contains "Done." at the end
            if 'Done.' in line and any(char.isalpha() for char in line):
                # Extract the part before "Done."
                detection_part = line.split('Done.')[0].strip()
                
                # Remove timing information in parentheses
                detection_part = re.sub(r'\([^)]*\)', '', detection_part).strip()
                
                # Split by comma to get individual items
                items = detection_part.split(',')
                
                for item in items:
                    item = item.strip()
                    if item:
                        # Extract ingredient name (remove count like "1 apple" -> "apple")
                        # Pattern: number followed by ingredient name
                        match = re.search(r'\d+\s+(\w+)', item)
                        if match:
                            ingredient = match.group(1)
                            detected_ingredients.append(ingredient)
                        else:
                            # If no number, just use the word
                            words = item.split()
                            if words:
                                detected_ingredients.append(words[-1])
                break
        
        # Remove duplicates and return
        detected_ingredients = list(set(detected_ingredients))
        
        # If nothing detected, return message
        if not detected_ingredients:
            return ["Unable to detect ingredients. Please try manual entry."]
        
        return detected_ingredients
    
    except subprocess.TimeoutExpired:
        return ["Error: Detection timed out"]
    except Exception as e:
        return [f"Error detecting ingredients: {str(e)}"]
# Recipe matching logic
def match_recipes(user_ingredients, dietary_prefs=None, difficulty='all', max_time=999, min_rating=0):
    recipes = load_database()
    ingredient_list = [ing.strip().lower() for ing in user_ingredients.split(',') if ing.strip()]
    
    matches = []
    for recipe in recipes:
        # Count matching ingredients
        match_count = sum(
            1 for ing in ingredient_list
            if any(
                ing in recipe_ing.lower() or recipe_ing.lower() in ing
                for recipe_ing in recipe['ingredients']
            )
        )
        
        # Check dietary preferences
        dietary_match = True
        if dietary_prefs:
            dietary_list = [d.lower() for d in dietary_prefs if d]
            if dietary_list:
                dietary_match = all(
                    diet in [d.lower() for d in recipe.get('dietary', [])]
                    for diet in dietary_list
                )
        
        # Apply filters
        difficulty_match = difficulty == 'all' or recipe['difficulty'] == difficulty
        time_match = recipe['cookTime'] <= max_time
        rating_match = recipe['rating'] >= min_rating
        
        # Require at least 2 matching ingredients
        if match_count >= 2 and dietary_match and difficulty_match and time_match and rating_match:
            recipe['match_score'] = match_count
            matches.append(recipe)
    
    # Sort by match score
    matches.sort(key=lambda x: x['match_score'], reverse=True)
    return matches

# LLM Recipe Generation
import json
from openai import OpenAI

def generate_recipe_with_llm(ingredients, dietary_prefs=None, api_key=None):
    if not api_key:
        return None, "Please provide your OpenAI API key to generate custom recipes"
    
    try:
        client = OpenAI(api_key=api_key)
        
        # Format dietary preferences
        dietary_text = ""
        if dietary_prefs:
            dietary_list = [d for d in dietary_prefs if d]
            if dietary_list:
                dietary_text = f"Dietary restrictions: {', '.join(dietary_list)}"
        
        # Prompt for GPT
        prompt = f"""
        You are a chef AI. Create a recipe using these ingredients: {ingredients}. {dietary_text}

        Return ONLY a valid JSON object in this exact format (no other text):
        {{
          "name": "Recipe Name",
          "ingredients": ["ingredient1", "ingredient2"],
          "instructions": ["step1", "step2"],
          "cookTime": 30,
          "difficulty": "easy",
          "servings": 4,
          "calories": 300,
          "protein": 15,
          "cuisine": "cuisine type",
          "dietary": ["vegetarian"],
          "rating": 4.5
        }}

        IMPORTANT: Return ONLY the JSON object, no markdown, no backticks, no extra text.
        """

        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4-turbo",  # You can change this to gpt-4o-mini or gpt-3.5-turbo if preferred
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000,
            temperature=0.7
        )

        recipe_text = response.choices[0].message.content.strip()
        recipe_text = recipe_text.replace("```json", "").replace("```", "").strip()

        # Parse recipe JSON
        new_recipe = json.loads(recipe_text)
        new_recipe['fromLLM'] = True

        # Save to database
        saved_recipe = save_to_database(new_recipe)
        
        return saved_recipe, "✨ AI-generated recipe created and saved to database!"

    except Exception as e:
        return None, f"Error generating recipe: {str(e)}"

# Format recipe for display
def format_recipe_card(recipe):
    dietary_badges = " ".join([f"🏷️ {d.title()}" for d in recipe.get('dietary', [])])
    llm_badge = "✨ AI Generated" if recipe.get('fromLLM') else ""
    
    return f"""
## 🍽️ {recipe['name']}

{llm_badge} {dietary_badges}

**⏱️ Cook Time:** {recipe['cookTime']} min | **👥 Servings:** {recipe['servings']} | **⭐ Rating:** {recipe['rating']}/5  
**📊 Difficulty:** {recipe['difficulty'].title()} | **🌍 Cuisine:** {recipe['cuisine']}

### 📋 Nutrition (per serving)
- Calories: {recipe['calories']} kcal
- Protein: {recipe['protein']}g

### 🛒 Ingredients
{chr(10).join([f"• {ing.title()}" for ing in recipe['ingredients']])}

### 👨‍🍳 Instructions
{chr(10).join([f"{i+1}. {step}" for i, step in enumerate(recipe['instructions'])])}

---
"""
# (Keep your INITIAL_RECIPES, initialize_database, load_database, save_to_database, 
# detect_ingredients_from_image, match_recipes, generate_recipe_with_llm, format_recipe_card as-is)

# Only update the Gradio app section below 👇

# Main search function (unchanged)
def search_recipes(ingredients_text, image, dietary_prefs, difficulty, max_time, min_rating):
    """
    Main function to search recipes based on text or image input
    """
    detected_text = ""
    
    # If image is provided, run YOLOv7 detection
    if image is not None:
        temp_image_path = "temp_upload.jpg"
        image.save(temp_image_path)
        
        detected_ingredients = detect_ingredients_from_image(
            temp_image_path, YOLO_WEIGHTS_PATH, YOLO_DETECT_SCRIPT, CONFIDENCE_THRESHOLD
        )
        
        detected_text = f"🔍 **Detected Ingredients:** {', '.join(detected_ingredients)}\n\n"
        ingredients_text = ', '.join(detected_ingredients)
    
    if not ingredients_text or not ingredients_text.strip():
        return "⚠️ Please provide ingredients (text or image)", "", ""
    
    # Search in database
    matches = match_recipes(ingredients_text, dietary_prefs, difficulty, max_time, min_rating)
    
    if matches:
        results = detected_text + f"✅ **Found {len(matches)} matching recipe(s):**\n\n"
        recipe_details = "\n\n".join([format_recipe_card(recipe) for recipe in matches[:5]])
        return results, recipe_details, ingredients_text
    else:
        # No matches found, try LLM generation
        recipe, message = generate_recipe_with_llm(ingredients_text, dietary_prefs, ANTHROPIC_API_KEY)
        if recipe:
            return detected_text + message, format_recipe_card(recipe), ingredients_text
        else:
            return detected_text + message, "", ingredients_text


# Initialize database on startup
initialize_database()

# ==============================
# 🎨 Gradio Interface (Simplified)
# ==============================
with gr.Blocks(theme=gr.themes.Soft(), title="Smart Recipe Generator") as app:
    gr.Markdown("""
    # 🍳 Smart Recipe Generator with AI Vision
    ### Discover recipes from your ingredients - Type them in or upload a photo!
    """)
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### 📝 Input Methods")
            
            ingredients_input = gr.Textbox(
                label="🥗 Type Ingredients (comma-separated)",
                placeholder="e.g., chicken, tomato, basil, garlic",
                lines=3
            )
            
            image_input = gr.Image(
                label="📸 Or Upload Image of Ingredients",
                type="pil"
            )
            
            gr.Markdown("### 🎛️ Preferences")
            
            dietary_checkboxes = gr.CheckboxGroup(
                choices=["Vegetarian", "Vegan", "Gluten-Free"],
                label="🥬 Dietary Preferences"
            )
            
            difficulty_dropdown = gr.Dropdown(
                choices=["all", "easy", "medium", "hard"],
                value="all",
                label="📊 Difficulty Level"
            )
            
            max_time_slider = gr.Slider(
                minimum=10,
                maximum=180,
                value=150,  # ✅ changed from 999 → 150
                step=5,
                label="⏱️ Max Cooking Time (minutes)"
            )
            
            min_rating_slider = gr.Slider(
                minimum=0,
                maximum=5,
                value=0,
                step=0.5,
                label="⭐ Minimum Rating"
            )
            
            search_btn = gr.Button("🔍 Search Recipes", variant="primary", size="lg")
        
        with gr.Column(scale=2):
            gr.Markdown("### 🎯 Results")
            
            status_output = gr.Markdown()
            detected_ingredients_output = gr.Textbox(
                label="Detected/Used Ingredients",
                interactive=False
            )
            recipe_output = gr.Markdown()
    
    # Event handler
    search_btn.click(
        fn=search_recipes,
        inputs=[
            ingredients_input,
            image_input,
            dietary_checkboxes,
            difficulty_dropdown,
            max_time_slider,
            min_rating_slider
        ],
        outputs=[status_output, recipe_output, detected_ingredients_output]
    )
    
    gr.Markdown("""
    ---
    ### 📖 How to Use:
    1. **Type ingredients** OR **upload an image** of your ingredients  
    2. Set your dietary preferences and filters  
    3. Click "Search Recipes"  
    4. The app detects ingredients using YOLOv7 and searches your recipe database  
    5. If no matches are found, it automatically uses AI to generate a new recipe!
    """)

if __name__ == "__main__":
    app.launch(share=False, server_name="0.0.0.0", server_port=7860)
