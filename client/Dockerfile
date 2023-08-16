# Stage 1: Build the dependencies
FROM node:latest AS build

WORKDIR /app

COPY package.json ./
COPY package-lock.json ./

RUN npm install

# Stage 2: Copy only necessary files for the runtime
FROM node:latest


WORKDIR /app

COPY --from=build /app/node_modules ./node_modules
COPY . .

CMD ["npm", "run", "start"]
