FROM python:3.11

# 建立工作目錄
WORKDIR /app

# 安裝 Poetry
RUN pip install poetry

# 複製 Poetry 設定檔並安裝依賴（不安裝自己專案）
COPY pyproject.toml poetry.lock* ./
RUN poetry config virtualenvs.create false && poetry install

# 複製整個程式碼（task、config 等）
COPY . .

# 開啟 Django 使用的 port
EXPOSE 8000

# 啟動指令可寫在 docker-compose.yml 裡
