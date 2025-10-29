# ☁️ Dockerized Weather Reporting Pipeline

[![Docker Compose](https://img.shields.io/badge/Stack-Docker%20Compose-blue)](https://docs.docker.com/compose/)
[![ELK Stack](https://img.shields.io/badge/Data%20Pipeline-RabbitMQ%20%7C%20Logstash%20%7C%20ElasticSearch-orange)](https://www.elastic.co/elk-stack)
[![Visualization](https://img.shields.io/badge/Visualization-Grafana-9cf)](https://grafana.com/)

This project provides a complete **Dockerized data pipeline** to fetch, process, and visualize real-time weather information.

---

## 💡 Overview

The core of this solution is a **Python application** that automatically retrieves **Jerusalem weather data** from **OpenWeatherMap.org**.

The data then moves through a robust processing and storage pipeline:

$$
\text{Python App (Source)} \rightarrow \text{RabbitMQ} \rightarrow \text{Logstash} \rightarrow \text{ElasticSearch (Storage)}
$$

Finally, the results are visualized on a dedicated **"Weather Report" dashboard** in **Grafana**, which uses ElasticSearch as its primary data source.

---

## 🚀 Getting Started

Follow these steps to quickly build and run the entire stack on your local machine.

### 1. Build and Run the Containers

Use `docker compose` to build the necessary images and launch all services simultaneously.

```bash
docker compose up --build
