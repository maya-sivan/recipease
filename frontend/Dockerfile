# Stage 1: Build the React/Vite app
FROM node:22.17.0 AS builder
WORKDIR /app

# Declare the build argument that will be passed from docker-compose.yml
ARG VITE_BACKEND_PREFIX

# Set it as an environment variable so the 'npm run build' command can access it
ENV VITE_BACKEND_PREFIX=${VITE_BACKEND_PREFIX}

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

FROM nginx:stable-alpine
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy the custom nginx.conf
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]