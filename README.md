# NeuralNetworkManager
A save button and manager for running neural networks.

# Jupyter Notebook Integration
To configure Jupyter notebook to run on a server

- jupyter notebook --generate-config

Open up your generated jupyter_notebook_config.py file and add

c.NotebookApp.tornado_settings = {
	'headers': {
        'Content-Security-Policy': "frame-ancestors 'https://localhost:80' * 'self' "
    }
}

# Generate SSL keys
- openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout privatekey.key -out certificate.crt
