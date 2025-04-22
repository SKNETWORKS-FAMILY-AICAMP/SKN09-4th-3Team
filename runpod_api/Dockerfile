FROM python:3.12

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
  && apt-get update && apt-get install -y git \
  && git init \
  && git remote add origin https://github.com/SKNETWORKS-FAMILY-AICAMP/SKN09-4th-3Team.git \
  && git config core.sparseCheckout true \
  && echo "runpod_api/" >> .git/info/sparse-checkout \
  && git pull origin main


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
