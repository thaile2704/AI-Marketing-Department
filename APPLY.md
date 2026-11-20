# Cách áp dụng (trong Codespaces, tại thư mục gốc repo)
1. git checkout -b claude/foundation
2. Giải nén zip này vào thư mục gốc repo (ghi đè config.py, model_gateway.py, page.tsx).
3. Thêm nội dung .env.patch.txt vào .env.example (và .env); sửa docker-compose.yml theo docker-compose.web-env.patch.txt.
4. cd apps/api && pip install -r requirements.txt pytest && pytest -q
5. docker compose up --build  ->  http://localhost:3000 và http://localhost:8000/docs
