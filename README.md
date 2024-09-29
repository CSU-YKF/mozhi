# 🌟 Mozhi - Intelligent Calligraphy Education Evaluation System 🖋️🎨

Welcome to **Mozhi**, the future of calligraphy education! 🎉 This project revolutionizes traditional Chinese calligraphy teaching with cutting-edge AI and a sleek, user-friendly interface. If you think mastering calligraphy takes years, think again—Mozhi brings that learning curve way down! 🚀

## 🚀 About the Project

Calligraphy, a treasured gem in Chinese culture, faces a modern challenge—**lack of resources, objective scoring, and personalized feedback**. But we’ve got this covered. 💡 With Mozhi, learners get instant feedback on their strokes, structures, and even aesthetics!

### What Makes Mozhi Special?

- **🖥️ Frontend (Vue):** A smooth and dynamic user experience, bringing calligraphy practice to your screen with real-time feedback.
- **⚙️ Backend (FastAPI):** The backbone of Mozhi, handling user data, evaluations, and recommendations at lightning speed.
- **🧠 Algorithms (Torch, GNN, RL):** We've incorporated deep learning with a **Siamese Regression Network (SRN)** for structure scoring, and **Stroke-Seg** for detailed stroke analysis. Plus, there's **personalized learning routes** powered by **DQN** and knowledge graph-enhanced **ChatGPT** guidance!

### Core Features 🔑

1. **Charm Framework**: A robust scoring system that evaluates the overall shape and individual stroke details of calligraphy.
   - **Vision Module**: Handles large-scale aesthetic features like balance and symmetry.
   - **Rule Module**: Provides detailed stroke analysis with the help of a cutting-edge **Unet-Transformer** hybrid model.
2. **Knowledge Graph & ChatGPT**: Fine-tuned AI to give learners helpful feedback and direction, ensuring continual improvement.
3. **Reinforcement Learning**: Adaptive learning paths based on individual progress, giving each user a unique experience tailored to their skills.

> Mozhi has been rigorously tested with **99.6% stroke segmentation accuracy** and delivers superior performance over previous methods in aesthetic evaluations. It’s fast, reliable, and, most importantly, easy to use! 🚀

## 🎨 How to Get Started

1. **Clone the repo**:
   ```bash
   git clone https://github.com/CSU-YKF/mozhi.git
   ```
2. **Install dependencies**:
   ```bash
   cd mozhi
   pip install -r requirements.txt
   ```
3. **Run the backend**:
   ```bash
   uvicorn main:app --reload
   ```
4. **Run the frontend**:
   ```bash
   cd web
   npm install
   npm run serve
   ```
5. **Start practicing your calligraphy skills and receive instant AI feedback!** 🖌️

## 🏆 Achievements

Mozhi proudly secured **First Place** 🥇 in the National Finals of the "Chinese Robotics and Artificial Intelligence Competition - AI Innovation Track"! 💻✨

Our system was praised for:
- Precision in stroke segmentation
- Aesthetic scoring accuracy
- Personalized learning paths
- Seamless integration of AI into traditional art 🎉

## 🙌 Acknowledgements

This project wouldn’t have been possible without the dedication of our amazing team:
- @Rvosuke (白泽阳) - Project Lead & AI Specialist 💻
- @LambertRao (饶逸石) - Backend Engineer 🔧
- @August-snoopy (丁御峰) - Frontend Developer 🎨
- @kyliancc (朱若朴) - Optimization and Future Enhancements 🌱
- @wosida (李东阳) - Algorithm Contributor 🧠

A huge thanks to everyone for their hard work and support! 🚀

## 📅 Future Plans

The journey doesn’t stop here! Next steps for Mozhi include:
- Further optimization of the **personalized recommendation engine**.
- Expanding the **knowledge graph** for more detailed feedback.
- Enhancing the **user interface** for a more engaging learning experience.

Stay tuned for updates and new features! 👀
