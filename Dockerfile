FROM node:lts-alpine as frontend-build
WORKDIR /app
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ .
RUN npm run build

FROM tiangolo/meinheld-gunicorn:python3.7

WORKDIR /app/
ADD backend/ /app/

# uWSGI will listen on this port
EXPOSE 8000

RUN pip install --no-cache-dir -r requirements.txt
# Add any custom, static environment variables needed by Django or your settings file here:
ENV DJANGO_SETTINGS_MODULE=BillSpliter.deploy

ENV APP_MODULE="BillSpliter.wsgi"
ENV GUNICORN_CONF="/app/BillSpliter/gunsetting.py"

# copying the fronend static code to server 
COPY --from=frontend-build /app/dist/ /app/static/


# CMD ["gunicorn","-c","DReport/gunsetting.py","DReport.wsgi"]