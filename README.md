# RECIPES
URL to the APP:
https://huggingface.co/spaces/Aaron-David-Don12/RECIPES

WRITE UP ABOUT my Approach:
Smart Recipe Generator: Hybrid AI Approach with Cost Optimization
This application leverages a cost-efficient hybrid architecture combining computer vision, database retrieval, and LLM generation. Users can input ingredients via text or image upload.
Architecture:

Input Layer: Gradio interface accepts text input or images of ingredients
Vision Module: YOLOv7 model (custom-trained .pt format) detects and classifies food items from uploaded images
Retrieval System: Detected/typed ingredients are matched against a JSON-based recipe database using fuzzy matching algorithms
LLM Fallback: When no suitable recipes exist, Claude Sonnet generates custom recipes matching user constraints (dietary preferences, difficulty, cooking time, ratings)
Database Persistence: AI-generated recipes are automatically saved to the database for future retrieval, minimizing API costs

Key Features:

Multi-modal input (text/image)
Dietary filtering (vegetarian, vegan, gluten-free)
Advanced filters (difficulty, time, rating)
Comprehensive recipe details (nutrition, instructions, servings)
Token-efficient design: LLM calls only when necessary

Cost Optimization Strategy: By caching LLM-generated recipes in the database, the system reduces repeated API calls for similar ingredient combinations, significantly lowering operational costs while maintaining response quality.
Deployment: Hosted on Hugging Face Spaces using Gradio for accessible web interface.
