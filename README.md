# Watson

## Istruzioni per il setup (Linux)

 - Clonare la repo: 
     - `git clone git clone https://github.com/ZanSara/watson`
     - `cd watson`
 - Se non lo avete (dovreste averlo) installare pip3: 
     - http://stackoverflow.com/questions/6587507/how-to-install-pip-with-python-3
 - Installare virtualenv: 
     - `sudo pip3 install virtualenv`
 - Creare un ambiente virtuale:
     - `virtualenv env` (`env` sarà il nome dell'ambiente virtuale creato)
 - Attivare l'ambiente virtuale:
     - `. env/bin/activate`
     - Per disattivarlo, `deactivate`
 - Una volta attivato l'ambiente virtuale, installarci Flask:
     - `pip3 install flask`
 - Rendere eseguibile il launcher:
     - `chmod a+x run.py`
 - Avviare il server:
     - `./run.py`
 - Il server gira su `http://127.0.0.1:5000`
 
## Istruzioni per avviare il server (Linux)
 - Attivare l'ambiente virtuale:
     - `. env/bin/activate`
     - Per disattivarlo, `deactivate`
 - Avviare il server:
     - `./run.py`
