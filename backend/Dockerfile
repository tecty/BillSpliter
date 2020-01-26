FROM tiangolo/meinheld-gunicorn:python3.7-alpine3.8

WORKDIR /app/
ADD . /app/
RUN echo  http://mirrors.aliyun.com/alpine/v3.7/main/ > /etc/apk/repositories
RUN echo  http://mirrors.aliyun.com/alpine/v3.7/community/ >> /etc/apk/repositories
RUN apk add --no-cache postgresql-libs
RUN apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev 
RUN pip install --no-cache-dir \
    -i https://pypi.tuna.tsinghua.edu.cn/simple \
    -r requirements.txt
RUN apk --purge del .build-deps
# Add any custom, static environment variables needed by Django or your settings file here:
ENV DJANGO_SETTINGS_MODULE=BillSpliter.deploy

ENV APP_MODULE="BillSpliter.wsgi"
ENV GUNICORN_CONF="/app/BillSpliter/gunsetting.py"

# # copying the fronend static code to server 
# COPY --from=frontend-build /app/dist/ /app/static/
