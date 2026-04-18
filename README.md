# 💰 FINNY - Student Finance App

A simple full-stack finance application built with Python Flask and vanilla JavaScript. FINNY helps students track their purchases and manage their expenses in real-time.

## Features

✨ **Simple & Beginner-Friendly**: Easy to understand and extend
📱 **Real-time Updates**: Add purchases and see them instantly
💾 **In-Memory Storage**: No database setup needed
🎨 **Beautiful UI**: Modern, responsive design
🔄 **CORS Enabled**: Frontend and backend communication works smoothly

## Project Structure

```
FINNY/
├── backend/
│   └── app.py              # Flask server with REST API
├── frontend/
│   ├── index.html          # Main HTML page with form and display
│   └── app.js              # JavaScript to handle frontend logic
├── transversal/
│   └── constants.py        # Shared constants (categories)
└── requirements.txt        # Python dependencies
```

## Prerequisites

- Python 3.7+
- A modern web browser
- Basic knowledge of Python and JavaScript

## Installation & Setup

### 1. Install Python Dependencies

```bash
# Navigate to the project directory
cd /workspaces/FINNY

# Install required packages
pip install -r requirements.txt
```

### 2. Start the Backend Server

```bash
# From the project root directory
python backend/app.py
```

You should see:
```
Starting FINNY Finance App Backend...
Server running on http://localhost:5000
```

### 3. Open the Frontend

Open your browser and navigate to:
```
file:///workspaces/FINNY/frontend/index.html
```

Or simply open the `index.html` file directly in your browser.

## How to Use

1. **Fill the Form**: Enter a purchase name and amount
2. **Select Category** (optional): Choose from Food, Transport, Study, or Other
3. **Click "Add Purchase"**: The purchase will be sent to the backend and displayed
4. **View Total**: See your total spending at the bottom

## API Endpoints

### GET /compras
Retrieve all purchases

**Response:**
```json
{
  "purchases": [
    {
      "id": 1,
      "name": "Coffee",
      "amount": 5.50,
      "category": "Food"
    }
  ],
  "total": 5.50,
  "count": 1,
  "categories": ["Food", "Transport", "Study"]
}
```

### POST /compras
Add a new purchase

**Request Body:**
```json
{
  "name": "Bus Ticket",
  "amount": 2.50,
  "category": "Transport"
}
```

**Response:**
```json
{
  "message": "Purchase added successfully",
  "purchase": {
    "id": 2,
    "name": "Bus Ticket",
    "amount": 2.50,
    "category": "Transport"
  },
  "total_purchases": 2
}
```

## Code Overview

### Backend (Flask)

- **CORS Support**: Enables communication between frontend and backend
- **In-Memory Storage**: Purchases stored in a Python list
- **Error Handling**: Validates input and returns appropriate error messages
- **RESTful API**: Clean endpoints following REST conventions

### Frontend (HTML/JavaScript)

- **Fetch API**: Makes HTTP requests to the backend
- **DOM Manipulation**: Dynamically updates the purchase list
- **Form Validation**: Checks inputs before sending to server
- **Error Handling**: Shows user-friendly error and success messages

### Transversal

- **Constants**: Centralized list of purchase categories

## Extending FINNY

Here are some ideas to expand this project:

1. **Add Edit/Delete**: Modify or remove purchases
2. **Categories Filter**: Filter purchases by category
3. **Date Tracking**: Add dates to purchases
4. **Export Data**: Download purchases as CSV
5. **Local Storage**: Save data in browser (IndexedDB or localStorage)
6. **Database**: Replace in-memory storage with a real database (SQLite, PostgreSQL)
7. **Authentication**: Add user accounts and login
8. **Statistics**: Show spending trends and charts

## Troubleshooting

### "Cannot connect to server"
- Make sure the backend is running on port 5000
- Check that you're no blocking port 5000 with another application
- Look at the backend console for error messages

### "CORS Error"
- Ensure Flask-CORS is installed (`pip install Flask-CORS`)
- Make sure the backend is running

### Form not submitting
- Open browser developer tools (F12) and check the Console tab
- Verify the backend URL in `app.js` is correct

## License

This is a beginner-friendly educational project. Feel free to use and modify it!

## Author

Created as an MVP for student finance tracking.

---

Happy tracking with FINNY! 💰