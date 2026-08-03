<h1 align="center">🎵 Moodify</h1>

<p align="center">
  <b>AI-Powered Emotion Recognition & Mood-Based Music Recommendation System</b>
</p>

<p align="center">
  Detect emotions from images using OpenAI's CLIP model and instantly receive personalized YouTube music recommendations.
</p>

---

## 📌 Overview

Moodify is an AI-powered application that analyzes a user's facial image using **OpenAI CLIP**, predicts the underlying emotion without task-specific training (Zero-Shot Learning), and recommends songs that match the detected mood using the **YouTube Data API v3**.

The project demonstrates the practical integration of **Computer Vision**, **Natural Language Processing**, **Zero-Shot Learning**, **REST APIs**, and **Interactive AI Deployment** into a single end-to-end application.

---

## ✨ Features

- 🎭 Zero-shot emotion recognition using OpenAI CLIP
- 🧠 Supports **18 emotion categories**
- 🎵 Real-time mood-based YouTube song recommendations
- 📊 Confidence score visualization
- 🖼️ Upload any image for instant emotion prediction
- ⚡ Fast inference using PyTorch
- 🌐 Interactive web interface built with Gradio

---

## 🛠️ Tech Stack

### Programming Language
- Python

### AI / Machine Learning
- OpenAI CLIP
- PyTorch
- Transformers (Hugging Face)

### Computer Vision
- PIL (Pillow)

### API
- YouTube Data API v3

### Frontend
- Gradio

### Others
- Requests
- Google Colab

---

## 🧠 How It Works

```text
             User Uploads Image
                      │
                      ▼
           Image Preprocessing (PIL)
                      │
                      ▼
        OpenAI CLIP Vision-Language Model
                      │
                      ▼
      Zero-Shot Emotion Classification
                      │
                      ▼
        Highest Confidence Emotion
                      │
                      ▼
     YouTube Data API Song Search
                      │
                      ▼
     Personalized Music Recommendations
```

---

## 🎯 Supported Emotion Categories

- Happy 😊
- Sad 😢
- Angry 😠
- Excited 🤩
- Calm 😌
- Fear 😨
- Surprise 😲
- Love ❤️
- Confident 💪
- Lonely 🌙
- Hopeful 🌅
- Relaxed 🌿
- Tired 😴
- Motivated 🚀
- Nostalgic 📸
- Bored 😐
- Anxious 😟
- Romantic 💖

---

## 📂 Project Structure

```
Moodify/
│
├── moodify.ipynb
├── README.md
├── requirements.txt
└── assets/
```

---

## 🚀 Installation

### Clone the Repository

```bash
git clone https://github.com/yourusername/Moodify.git
```

```bash
cd Moodify
```

---

### Install Dependencies

```bash
pip install -r requirements.txt
```

or

```bash
pip install torch transformers pillow requests gradio
```

---

### Configure YouTube API

Create your API key from the Google Cloud Console.

Replace

```python
YOUTUBE_API_KEY = "YOUR_API_KEY"
```

with your own key.

---

### Run the Project

```bash
python app.py
```

or open the notebook in

- Google Colab
- Jupyter Notebook

---

## 📸 Demo

### Input

Upload an image.

### AI Prediction

```
Emotion:
Happy 😊

Confidence:
91.3%
```

### Output

```
🎵 Top YouTube Recommendations

1. Song A
2. Song B
3. Song C
```

---

## 💡 Future Improvements

- 🎤 Voice emotion detection
- 😊 Live webcam support
- 🎶 Spotify API integration
- 🤖 Personalized recommendation engine
- 📱 Mobile application
- ☁️ Cloud deployment
- 🧠 Fine-tuned emotion classification model

---

## 📚 Learning Outcomes

This project helped me gain practical experience with:

- Machine Learning
- Deep Learning
- Computer Vision
- Vision-Language Models
- Zero-Shot Learning
- REST APIs
- AI Deployment
- Interactive UI Development
- Model Inference
- Prompt Engineering

---

## 🤝 Contributing

Contributions are welcome!

If you'd like to improve Moodify:

1. Fork the repository
2. Create a new branch
3. Commit your changes
4. Open a Pull Request

---

## ⭐ If You Like This Project

Please consider giving this repository a ⭐.

It helps others discover the project and motivates future development.

---

## 👨‍💻 Author

**Bhuwan Yogi**

🎓 B.Tech Computer Science Engineering (AI/ML)

💻 AI • Machine Learning • Computer Vision • NLP • Data Science

📧 yogibhuwan2004@gmail.com

🔗 LinkedIn: https://linkedin.com/in/bhuwanyogi

🔗 GitHub: https://github.com/Bhuwanyogii

---

## 📄 License

This project is licensed under the MIT License.
