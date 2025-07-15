# Stage 1: Build the React/Vite app
FROM node:18 as build
WORKDIR /app

# --- Required Change ---
# Declare the build argument that will be passed from docker-compose.yml
ARG VITE_BACKEND_API_URL

# Set it as an environment variable so the 'npm run build' command can access it
ENV VITE_BACKEND_API_URL=${VITE_BACKEND_API_URL}

COPY . .
RUN npm install

# This command will now use the VITE_BACKEND_API_URL variable
RUN npm run build
# Stage 2: Serve the static files with Nginx
FROM nginx:stable-alpine

# Copy the custom nginx.conf
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy build frontend
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]