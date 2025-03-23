# Sistema de Transportadora

Este projeto é um sistema para calcular o custo de transporte de cargas com base no peso e na distância, utilizando Python, Django e princípios de Clean Architecture. O sistema considera diferentes veículos, cada um com uma capacidade máxima e um custo por km rodado, e permite identificar a melhor opção ou combinação de veículos para transportar a carga.

## Funcionalidades

- **Cálculo do Custo de Transporte:**  
  Realiza o cálculo do custo com base no peso da carga e em uma distância fixa (600 km).

- **Gerenciamento de Veículos:**  
  Permite visualizar a lista de veículos cadastrados, cada um com capacidade máxima e custo por km.

- **Seleção de Veículo(s):**  
  Identifica o veículo ou a combinação de veículos ideal para transportar a carga de acordo com as faixas de peso definidas (100 kg a 200.000 kg, com incrementos de 500 kg).

## Tecnologias Utilizadas

- Python 3.x
- Django 3.x ou superior
- Bootstrap 4 (para a interface)

## Pré-requisitos

- Python 3.x instalado
- Pip (gerenciador de pacotes Python)
- Virtualenv (opcional, mas recomendado para isolar o ambiente)

## Instalação e Configuração

### 1. Clonando o Repositório

```bash
git clone https://github.com/rodrigoFerreir/project-carrier.git
cd project-carrier
```


## 2. Criando o Ambiente Virtual

```
python3 -m venv env
source env/bin/activate   # No Windows, utilize: env\Scripts\activate
```

## 3. Instalando as Dependências
```pip install -r requirements.txt```


## 4. Configurando o Banco de Dados
``` 
python manage.py makemigrations
python manage.py migrate
```

## 5. Carregando os Dados Iniciais (Fixture)
```
python manage.py loaddata core/fixtures/vehicles.json
```

## 6. Executando o Servidor de Desenvolvimento

``` python manage.py runserver ```
