FROM node:latest

# Expose external ports
EXPOSE 3000
EXPOSE 35729

# Define the work directory
WORKDIR /app

# Add node modules to PATH
ENV PATH=/app/node_modules/.bin:$PATH

# Copy packages files to container
COPY package.json /app/package.json
COPY package-lock.json /app/package-lock.json

# Install node packages
RUN npm install
RUN npm install react-scripts -g

# Copy all files into container
ADD . /app

# Define startup command
CMD [ "npm", "start" ]
