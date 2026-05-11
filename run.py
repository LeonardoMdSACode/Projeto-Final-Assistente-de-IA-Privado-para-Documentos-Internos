# run.py
# serve apenas como launcher para evitar uvicor app.app:app --reload

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app.app:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
