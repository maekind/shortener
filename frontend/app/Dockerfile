# Use an official Node.js runtime as the base image
FROM node:20 AS build-stage

# Set the working directory inside the container
WORKDIR /app

# Copy the package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the entire application source code
COPY . .

# Build the application for production
RUN npm run build

# Use Nginx for serving the production build
FROM nginx:stable-alpine AS production-stage

# Copy the built files from the build stage to the Nginx directory
COPY --from=build-stage /app/dist /usr/share/nginx/html

# Expose port 80 for serving the application
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]