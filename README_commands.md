# Setting

1. Frontend

``` shell
    cd frontend/
    npm run dev
```

2. Backend

``` shell
    cd backend/
    python -m venv .venv
    source venv/bin/activate
    pip install -r requirements.txt
    uvicorn main:app --reload
```

3. Set Admin

``` shell
    curl -X POST 'https://slideai.onrender.com/api/admin/set-admin?email=your-email@example.com'
```