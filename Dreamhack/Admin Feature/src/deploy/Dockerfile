FROM maven:3.8.5-openjdk-17-slim as builder

WORKDIR /app

COPY ./ctf .
RUN apt-get update && apt-get install -y openssl && \
    rm -rf /var/lib/apt/lists/* && \
    sed -i "s/'[0-9a-f]\{64\}'[[:space:]]*,[[:space:]]*'ADMIN'/\'$(openssl rand -hex 32)\', 'ADMIN'/" src/main/resources/data.sql

# Package the application
RUN mvn clean package -DskipTests

FROM openjdk:17-jdk-alpine

WORKDIR /app
COPY --from=builder /app/target/*.jar app.jar
COPY ./flag /flag
RUN chmod 755 /flag

EXPOSE 8003
CMD ["java", "-jar", "app.jar"]