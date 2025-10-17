FROM node:22-alpine AS build
WORKDIR /app
COPY ./trajectopy-react /app
RUN npm ci && npm run build

FROM python:3.13-slim AS runtime
WORKDIR /app

COPY ./trajectopy-api/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY ./trajectopy-api /app
COPY --from=build /app/build ./frontend/build

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
