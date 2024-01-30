FROM node:current-alpine
WORKDIR /app
COPY public/ /app/public/
COPY src/ /app/src/
COPY package.json /app/
COPY package-lock.json /app/
RUN npm install
RUN npm run build
RUN npm install -g serve
CMD ["serve", "-s", "build", "-l", "3000"]
