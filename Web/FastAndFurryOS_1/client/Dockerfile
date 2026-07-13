FROM node:22.2.0


# # install simple http server for serving static content

# make the 'app' folder the current working directory
WORKDIR /app

# copy both 'package.json' and 'package-lock.json' (if available)
COPY package*.json ./

# install project dependencies
# RUN npm ci
RUN npm install
# RUN npm install -g vite

RUN npm install -g http-server
COPY . .

# RUN npm install -g @vue/cli
# RUN npm install -g @vue/cli-service
# RUN npm install -g @vue/cli-plugin-babel
# RUN npm install -g tailwindcss postcss autoprefixer


# copy project files and folders to the current working directory (i.e. 'app' folder),
# ONLY if not using workind directory as volume
# COPY . .

# build app for production with minification
# CMD ["npm", "run", "dev"]

RUN npm run build

EXPOSE 8080
CMD [ "http-server", "dist" ]

# Note des docs: If you are running your container behind a TLS Termination Proxy (load balancer) like Nginx or Traefik, 
# add the option --proxy-headers, this will tell Uvicorn (through the FastAPI CLI) to trust the headers sent by that proxy 
# telling it that the application is running behind HTTPS, etc.
