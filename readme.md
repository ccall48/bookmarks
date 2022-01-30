# Create and run project (linux)
Recommended python v3.9 or higher. 
```bash
python3 -m venv app
cd app
source bin/activate
git clone https://github.com/ccall48/bookmarks
cd bookmarks
pip install -r requirements.txt
python app.py
```

## Project Documentation
When project is running documentation can be found at.  
http://localhost:1111/docs  
http://localhost:1111/redoc

## todo
1. Create db and or tables if not exists on project startup.
2. Add tags db to handle link tags
3. Add user db for api-key authorization
