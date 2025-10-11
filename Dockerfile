# Use official Node.js runtime as base image
FROM node:18-alpine

# Set working directory in container
WORKDIR /app

# Copy package.json and package-lock.json (if available)
COPY package*.json ./

# Install dependencies
RUN npm install --only=production

# Copy application files
COPY . .

# Create backups directory
RUN mkdir -p backups

# Expose port 3000
EXPOSE 3000

# Create non-root user for security
RUN addgroup -g 1001 -S nodejs
RUN adduser -S foosball -u 1001

# Change ownership of app directory
RUN chown -R foosball:nodejs /app
USER foosball

# Start the application
CMD ["npm", "start"]