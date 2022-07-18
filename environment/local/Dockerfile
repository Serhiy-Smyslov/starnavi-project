FROM python:3.9

WORKDIR /starnavi_project
COPY environment/requirements/ /starnavi_project/requirements/

RUN apt-get update && apt-get install gettext -y
RUN pip install --upgrade pip
RUN pip install -r ./requirements/local.txt
RUN pip freeze


EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000" , "--reload"]

