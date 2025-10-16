# 🍳 Smart Recipe Generator: Hybrid AI Approach with Cost Optimization

### 🔗 Live App
👉 [Try it on Hugging Face Spaces](https://huggingface.co/spaces/Aaron-David-Don12/RECIPES)

### 🧠 Trained YOLO Model for Ingredients Detection
📁 [Download RecipeYOLOv7 Model (Google Drive)](https://drive.google.com/file/d/1s3_35hrIFEM_5glYB6HM6SMobfz9kQ40/view?usp=sharing)

---

## 🚀 Overview

**Smart Recipe Generator** is an AI-powered application that intelligently generates recipes based on user-provided ingredients — either through **text input** or **image upload**.  
It combines the strengths of **Computer Vision**, **Database Retrieval**, and **Large Language Models (LLMs)** to deliver accurate, creative, and cost-efficient recipe suggestions.

---

## 🏗️ Architecture

### 🧩 1. Input Layer
- Built with **Gradio** for a simple and intuitive web interface  
- Accepts **text input** or **image uploads** of ingredients  

### 👁️ 2. Vision Module
- Utilizes a **custom-trained YOLOv7 model (.pt)** for ingredient detection  
- Accurately identifies multiple food items from uploaded images  

### 📚 3. Retrieval System
- Matches detected or typed ingredients against a **JSON-based recipe database**  
- Implements **fuzzy matching algorithms** for flexible ingredient comparison  

### 💡 4. LLM Fallback
- If no suitable recipe exists, the **Claude Sonnet LLM** dynamically generates one  
- Takes into account:
  - Dietary preferences (vegetarian, vegan, gluten-free)
  - Difficulty level
  - Cooking time
  - User rating expectations  

### 💾 5. Database Persistence
- All **AI-generated recipes** are automatically stored in the database  
- Ensures that future requests with similar ingredients retrieve cached results  
- Significantly reduces **API costs** while maintaining **high response quality**

---

## 🌟 Key Features

✅ **Multi-modal input** — supports both text and image-based ingredient inputs  
✅ **Smart dietary filtering** — choose between vegetarian, vegan, or gluten-free  
✅ **Advanced search filters** — difficulty, preparation time, and ratings  
✅ **Comprehensive recipe output** — includes nutrition, servings, and step-by-step instructions  
✅ **Cost-efficient design** — minimizes unnecessary LLM usage via intelligent caching  

---

## 💰 Cost Optimization Strategy

This project employs a **token-efficient hybrid architecture**:
- Recipes generated once by the LLM are **cached locally** in the recipe database  
- Subsequent similar ingredient queries retrieve existing data instead of invoking the LLM  
- This **reduces redundant API calls** and ensures **sustainable scalability**  

---

## 🌐 Deployment

- Hosted on **Hugging Face Spaces**
- Frontend built with **Gradio** for a user-friendly experience  
- Fully accessible through web browsers without additional setup  

---

## 🧩 Tech Stack

| Component | Technology Used |
|------------|------------------|
| Object Detection | YOLOv7 (custom-trained) |
| Language Model | Claude Sonnet |
| Interface | Gradio |
| Hosting | Hugging Face Spaces |
| Database | JSON (local persistence) |
| Matching Algorithm | Fuzzy Matching |

---

## 🏁 Conclusion

The **Smart Recipe Generator** demonstrates how hybrid AI systems can combine **computer vision, retrieval mechanisms, and generative AI** to create intelligent and cost-optimized solutions.  
By caching generated results and using LLMs only when necessary, the system ensures **both efficiency and creativity** — a practical model for real-world AI deployment.

---
