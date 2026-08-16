FROM python:3.9.7

WORKDIR /usr/src/app

#./ --> means the current directory which is: /usr/src/app
COPY requirements.txt ./

#run pip install is the longest time taking line of code bc id download req
RUN pip install --no-cache-dir -r requirements.txt

#copy . . --> means to copy all of the source code, *we run pip install req first, 
#then copy all the source code even with req bc: 
#if we change anything in the source code we dont have to re-install req 
#(wich takes ALOT of time) 
#bc we changed nothing in it
COPY . .

CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000" ]
