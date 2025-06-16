# 💊 Pharmore: Inventory Management System for Pharmacy Stores

Pharmore is a robust and user-friendly Django-based inventory management system built specifically for pharmacy stores. It helps pharmacy owners and staff track medicine stock, manage suppliers, handle purchases and sales, and generate professional reports—all from a modern web interface.

### Live Demo [Here](https://curiousbud.pythonanywhere.com/).
## 📦 Features

- ✅ Real-time inventory tracking
- 🧾 Purchase & sales records with invoice generation
- 🧪 Medicine batch & expiry management
- 🧍 Supplier management
- 📄 Professional PDF reports using ReportLab
- 🎨 Clean & responsive UI with Crispy Forms

## 🚀 Tech Stack

- **Backend:** Django 5.0.6
- **Frontend:** HTML, CSS, Bootstrap (via Django templates)
- **Database:** SQLite (default), easily switch to PostgreSQL or MySQL
- **PDF Generation:** ReportLab
- **Forms:** django-crispy-forms

## 📁 Project Structure (Simplified)

```
Pharmore/
├── inventory/        # Core inventory logic (models, views, forms)
├── templates/        # HTML templates
├── static/           # CSS, JS, image files
├── media/            # Uploaded files
├── manage.py
└── requirements.txt
```

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/curiousbud/Pharmore.git
cd Pharmore
```

### 2. Set up a virtual environment

```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply migrations

```bash
python manage.py migrate
```

### 5. Run the development server

```bash
python manage.py runserver
```

### 6. Create a superuser (admin)

```bash
python manage.py createsuperuser
```

### 7. Access the app

Visit: [http://localhost:8000](http://localhost:8000)

## 🛠️ Requirements

```
asgiref==3.8.1
chardet==5.2.0
Django==5.0.6
django-crispy-forms==2.1
pillow==11.1.0
reportlab==4.3.1
sqlparse==0.5.3
tzdata==2025.2
```

## ✅ Roadmap (Suggestions)

- 📷 Barcode scanning for medicines
- 📩 SMS or email alerts for low stock or expiry
- 📊 Export reports to Excel or CSV
- 🔐 Role-based access control
- 🌐 REST API for integration with POS systems



## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/xyz`)
3. Commit your changes
4. Open a Pull Request

## 📄 License
MIT License. See [LICENSE](LICENSE) for more details.

## 👨‍⚕️ Made with ❤️ for pharmacies
Have questions? Suggestions? Drop an issue or start a discussion on the GitHub repo!
