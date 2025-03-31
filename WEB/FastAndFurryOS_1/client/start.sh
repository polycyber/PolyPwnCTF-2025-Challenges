# ./build.sh && docker run -it -p 5173:5173 --rm -v "/${PWD}":/app --name furryos_frontend_container furryos_frontend
./build.sh && docker run -it -p 8080:8080 --rm --name furryos_frontend_container furryos_frontend
