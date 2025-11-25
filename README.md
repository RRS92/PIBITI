# PIBITI

# Sobre o projeto

Este trabalho apresenta o desenvolvimento de um sistema inteligente de alerta precoce para hiperlactatemia pós-operatória em cirurgias cardíacas, utilizando técnicas de aprendizado de máquina aplicadas a dados clínicos. O objetivo principal foi prever antecipadamente o risco dessa complicação, permitindo intervenções clínicas mais ágeis e personalizadas. O conjunto de dados inicial, passou por rigoroso processo de preparação, incluindo padronização de variáveis, codificação de categorias, criação de variáveis derivadas, tratamento de outliers por winsorização e exclusão de registros incompletos, Foram testados diversos algoritmos de aprendizado supervisionado, como Regressão Logística, Random Forest, Gradient Boosting, Support Vector Machine, K-Nearest Neighbors, Naive Bayes e Decision Tree, avaliados por métricas como acurácia, precisão, recall, F1-score e AUC-ROC, com ênfase no recall devido à importância clínica de minimizar falsos negativos. A Regressão Logística apresentou o melhor equilíbrio entre desempenho preditivo e interpretabilidade clínica, sendo selecionada como modelo final. 

# Sobre o Sistema

O sistema foi implementado em arquitetura cliente-servidor, com backend em Python (Flask) para execução do pipeline e geração da predição, e frontend em HTML, CSS e JavaScript para inserção de dados e visualização do risco calculado. O protótipo mostrou-se funcional, demonstrando a viabilidade técnica da solução e seu potencial para apoiar a tomada de decisão clínica e intervenções precoces.

# Como rodar o sistema

1º passo:

Use o comando a seguir para rodar a API do backend:

poetry run python main.py

2º passo:

No cmd/terminal vá até a pasta do ngrok e dê o comando para iniciar o sistema:

cd C:\Program Files\ngrok

ngrok.exe http 5000

3º passo:

Pegue a URL disponibilizada pelo ngrok e substitua o URL da variavel "API_BASE_URL" no arquivo config.js no frontend

# Link de demonstração do sistema

https://youtu.be/VUTIafYTOEs?si=eKF1Oo2moTPZG9wk


