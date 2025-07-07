# Heurística NEH para o Problema de Flow Shop Permutacional

Este repositório contém a implementação da heurística NEH (Nawaz, Enscore e Ham) para o problema de sequenciamento da produção em ambiente Flow Shop Permutacional, com objetivo de minimizar o makespan ($C_{max}$). O trabalho foi desenvolvido como parte da disciplina **Tópicos Especiais em Engenharia de Produção I**, na Universidade Federal do Ceará (UFC), 2025.

## Sobre o Problema

Dado um conjunto de tarefas que devem ser processadas por várias máquinas em sequência, o objetivo é encontrar a ordem ótima das tarefas que minimize o tempo total de processamento (makespan). O problema é classificado como NP-difícil.

## Funcionalidades

- Implementação da heurística NEH em Python
- Leitura de instâncias benchmark de Taillard
- Cálculo do makespan e do desvio percentual relativo (DPR)
- Geração de gráficos de Gantt

## Requisitos e Ambiente

Este projeto foi desenvolvido e testado em:

- **Python 3.11**
- **Visual Studio Code (VSCode)** como ambiente de desenvolvimento
- Bibliotecas utilizadas:
  - `numpy`
  - `matplotlib`
