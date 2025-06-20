FROM node:22.0-alpine

WORKDIR service/

COPY ./services/frontend/package*.json ./

RUN npm install

COPY ./services/frontend .

EXPOSE 3000

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "3000"]