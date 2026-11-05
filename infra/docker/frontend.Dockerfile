# infra/docker/frontend.Dockerfile
FROM node:20-alpine

WORKDIR /app

# Install dependencies
COPY frontend/package.json frontend/package-lock.json* ./
RUN npm install

# Copy source code
COPY frontend/ .

EXPOSE 5173

# Run Vite in host-accessible mode
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]