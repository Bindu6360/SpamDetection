# ⚡ QUICK START GUIDE

Get your Spam Detection System running in **5 minutes**!

## 🚀 Quick Setup

### 1. Open Terminal in VS Code
```
Ctrl + ` (backtick)
```

### 2. Create & Activate Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Train the Model
```bash
cd ml_model
python train_model.py
cd ..
```

### 5. Run the Application
```bash
python app.py
```

### 6. Open in Browser
```
http://localhost:5000
```

---

## ✅ Verify Everything Works

1. ✓ Flask server running? Check terminal for "Server running at http://localhost:5000"
2. ✓ Website loaded? Check browser shows SpamGuard homepage
3. ✓ Try a test message: "Click here to claim your free prize!!!"
4. ✓ See result? Should show "Spam" with high confidence

---

## 🎯 What to Do Next

### For Demonstration
1. Enter different messages to test
2. Check prediction history
3. View statistics

### For Viva Explanation
1. Show website working
2. Show prediction results
3. Explain the code (see README.md)
4. Discuss ML model and accuracy

### For Modifications
- Edit `sample_data.csv` to add more training data
- Modify `style.css` to change colors/design
- Add new fields in `index.html`
- Extend database schema in `app.py`

---

## 📁 Key Files to Know

| File | What it does |
|------|-------------|
| `train_model.py` | Creates the AI model |
| `app.py` | Backend server |
| `index.html` | Website interface |
| `style.css` | Website styling |
| `script.js` | Website interaction |

---

## ❌ Common Issues

| Problem | Solution |
|---------|----------|
| "No module named 'flask'" | Run: `pip install -r requirements.txt` |
| "Port 5000 already in use" | Run: `netstat -ano \| findstr :5000` then `taskkill /PID <id> /F` |
| "Model files not found" | Run: `cd ml_model && python train_model.py && cd ..` |
| "Can't connect to backend" | Check Flask server is running |

---

## 📞 Need Help?

1. Check **README.md** for detailed documentation
2. Read code comments for explanations
3. Check browser console (F12) for errors
4. Check terminal for Flask errors

---

## 🎓 For College Viva

**Key Points to Remember:**

1. **Purpose:** Spam detection using Machine Learning
2. **Algorithm:** Multinomial Naive Bayes classifier
3. **Features:** TF-IDF vectorization with 1000 features
4. **Accuracy:** ~90% on test data
5. **Database:** Stores all predictions for history
6. **Frontend:** Modern, responsive UI with animations
7. **Backend:** Flask REST API with error handling
8. **Scalability:** Can handle longer messages and more data

---

**Happy Learning! 🚀**
