# 🏏 IPL 2026 Playoff Predictor

An interactive, web-based dashboard built with **Streamlit** and **Pandas** to track and predict the playoff scenarios for the IPL 2026 season. This tool allows fans and analysts to input upcoming match results sequentially and see how the standings, qualification status, and elimination risks change in real-time.

## 🚀 Features

* **Sequential Match Predictor:** Automatically guides you through upcoming fixtures from May 1st to the final league game.
* **Live Points Table:** A dynamic table that re-sorts itself instantly based on points and Net Run Rate (NRR).
* **Mathematical Qualification (Q):** Automatically marks teams with a `(Q)` when they are guaranteed a top 4 spot.
* **Mathematical Elimination (E):** Identifies teams that can no longer reach the top 4 based on their maximum possible points.
* **Interactive UI:** Clean, centered data display with bolded headers and color-coded status highlights (Green for Top 4, Red for Eliminated).

## 🛠️ Tech Stack

* **Python 3.11+**
* **Streamlit:** For the web interface and interactivity.
* **Pandas:** For data manipulation and NRR logic.
* **Docker:** For containerization and easy deployment.

## 📦 Installation & Setup

### Local Setup
1. **Clone the repository:**
   ```bash
   git clone [https://github.com/Dheeraj1225/ipl-playoffs.git](https://github.com/Dheeraj1225/ipl-playoffs.git)
   cd ipl-playoffs

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run predict.py