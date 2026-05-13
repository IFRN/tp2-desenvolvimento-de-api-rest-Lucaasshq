[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/KEr3YAoF)
[![Open in Codespaces](https://classroom.github.com/assets/launch-codespace-2972f46106e565e64193e422d61a12cf1da4916b45550586e14ef0a7c637dd04.svg)](https://classroom.github.com/open-in-codespaces?assignment_repo_id=23907016)

#Gerenciamento de Eleições 






## Instruções de Instalação

1. **Clone o repositório:**
   ```bash
   git clone [URL_DO_SEU_REPOSITORIO]
   cd eleicoes_api



1. **Criar ambiente**
   ```bash
   python -m venv venv



1. **Instalar dependencias**
   ```bash
   pip install django djangorestframework django-filter drf-yasg qrcode pillow django-cors-headers

1. **Migração**
   ```bash
   python manage.py makemigrations
   python manage.py migrate

1. **Criar super usuario**  
python manage.py createsuperuser

1. **Inicar**  
python manage.py runserver

Documentação da API  
A documentação está disponível nos endpoints:

Swagger UI: http://127.0.0.1:8000/swagger/

ReDoc: http://127.0.0.1:8000/redoc/
