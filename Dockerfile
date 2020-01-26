FROM node:12-alpine AS frontend-build
WORKDIR /app/
ADD frontend/ /app/
RUN npm --registry https://registry.npm.taobao.org install 
RUN npm run build 

# production stage
FROM nginx:stable-alpine as production-stage
COPY --from=frontend-build /app/dist /usr/share/nginx/html
# copy the server config to direct the dynamic reponse to 
# python backend 
COPY nginx.conf /etc/nginx/conf.d/default.conf 

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]