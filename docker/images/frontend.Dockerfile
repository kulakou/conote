FROM node:21.5.0

WORKDIR service/

COPY ./services/frontend/package*.json .

RUN npm install

COPY ./services/frontend .

EXPOSE 3000
CMD ["npm", "run", "dev"]