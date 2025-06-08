# Build stage
FROM node:18 AS builder
WORKDIR /app

# Add ARG for env var
ARG VITE_CHAT_API_URL

# Set env var so Vite can read it
ENV VITE_CHAT_API_URL=$VITE_CHAT_API_URL

COPY . .
COPY .env .env

RUN npm install
RUN npm run build

# Production stage
FROM node:18-slim
WORKDIR /app
RUN npm install -g serve
COPY --from=builder /app/dist /app/dist
EXPOSE 3000
CMD ["serve", "-s", "dist", "-l", "3000"]