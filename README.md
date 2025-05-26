## Project Layout

```

├── requirements.txt
├── README.md             
└── app/
    ├── main.py           # FastAPI instance & router wiring
    ├── core/             # config & security helpers
    ├── db/               # SQLAlchemy base / session
    ├── models/           # ORM table classes
    ├── schemas/          # Pydantic models
    ├── repositories/     # DB-access wrappers
    ├── services/         # business logic
    ├── api/              # routers and shared deps
    └── middleware/       # request-size limit
    ├── .env.example      # local environment variables example file

````

---

## Requirements

* Python 3.11 +
* **MySQL**
* Packages in `requirements.txt`

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
````

---

## ▶️ Run the server

```bash
uvicorn app.main:app --reload
```

Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for Swagger UI.

---

## 🌐 HTTP API

| Method & Path        | Auth? | Body (example)                          | Description                    |
| -------------------- | ----- | --------------------------------------- | ------------------------------ |
| `POST  /signup`      | –     | `{ "email": "a@b.com", "password":"…"}` | Register + receive JWT         |
| `POST  /login`       | –     | same as above                           | Obtain a fresh JWT             |
| `POST  /posts`       | ✅     | `{ "text": "Hello" }`                   | Create post (≤ 1 MB)           |
| `GET   /posts`       | ✅     | –                                       | List your posts (cached 5 min) |
| `DELETE /posts/{id}` | ✅     | –                                       | Delete **your** post           |

**Auth header**

```http
Authorization: Bearer <token>
```

---

### Payload size

Any request body larger than **1 048 576 bytes** returns a **413 Payload Too Large** with JSON:

```json
{
  "error": "payload_too_large",
  "max_bytes": 1048576,
  "detail": "Payload exceeds 1048576 bytes limit"
}
```

---
