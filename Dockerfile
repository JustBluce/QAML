
FROM node:lts-alpine as build-stage
COPY /Vue /Vue
WORKDIR /Vue

LABEL org.opencontainers.image.authors="damianrene@cs.umd.edu"


RUN npm install vue
RUN npm install -g serve
RUN npm install
RUN npm run build

EXPOSE 5000



# production stage
EXPOSE 80
CMD ["npm", "run", "dev"]