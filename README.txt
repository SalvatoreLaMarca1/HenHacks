# The Data Bard

## Overview
The Data Bard is a **medieval-inspired** data visualization and analysis platform that allows users to report, analyze, and seek insights on incidents such as **fires, disease outbreaks, and crimes**. It integrates **Google's Gemini AI** to provide intelligent interpretations of data, all while maintaining an engaging 1300s storytelling theme.

## Features
### 🏰 **Incident Reporting & Visualization**
- Users can **report events** (fires, diseases, crimes) with a single click.
- Interactive **map visualization** of incidents based on live data.
- Dynamic filtering to display **only relevant** event types.

### 🔥 **Real-Time Data Insights**
- Data from user reports is processed and displayed instantly.
- Different event sizes (Small, Medium, Large) dynamically adjust map visuals.

### 🧙 **Gemini AI-Powered Analysis**
- Integrated **LLM chatbot** provides insights into incident data.
- AI interprets the data **as if in the 1300s**, avoiding modern terminology.
- Provides **landmark-based** locations instead of raw coordinates.

## Installation & Setup
### Prerequisites
Ensure you have **Python 3.8+** installed. Install required dependencies:

```sh
pip install streamlit pandas numpy google-generativeai python-dotenv
```

### API Key Setup
1. Obtain an **API Key** for Gemini AI.
2. Create a `.env` file in the project directory and add:
   ```sh
   API_KEY=your_gemini_api_key_here
   ```

### Running the Application
```sh
streamlit run main.py
```

## Code Structure
- `main.py`: Core logic of the application.
- `utils.py`: Helper functions.
- `db.py`: Database interactions for storing and retrieving reports.
- `styling.py`: Custom styles and theming.
- `data.csv`: Stores reported incidents.

## How It Works
1. **User selects an event type (Fire, Disease, Crime).**
2. **User reports an event**, which is stored in a database.
3. **Data is displayed on an interactive map.**
4. **User can ask the AI chatbot** for insights on the reported data.
5. **AI provides historical-style responses**, using modern-day landmarks instead of coordinates.

## Future Enhancements 🚀
- **Government Data Validation:** Cross-check reports with official sources.
- **Predictive Analytics:** Forecast future incidents based on historical data.
- **Emergency Alerts:** Integrate with real-time notification systems.

## Acknowledgments
Special thanks to **Streamlit, Google Gemini AI, and Open Data APIs** for enabling this project!

---
🛡️ "The Data Bard: Seek wisdom in the data’s tale." 📜

