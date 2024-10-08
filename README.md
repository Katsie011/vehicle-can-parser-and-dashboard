# Vehicle CAN utils  (🚧 a work in progress 🚧) 
smol lil repo with a set of utils to extract info from a mf4 file after recording can messages.  

There is also a dashboard for viewing plots of the extracted data in the browser using Panel.

## Usage
### Setup
If you don't have `conda` installed, you can get it via the instructions [here](https://docs.anaconda.com/miniconda/).

Create a new conda environment and install the requirements using:
```python
pip install -r requirements.txt
```

Next, add all the DBC files you would like to use to decode the CAN messages into the folder `DBCs`.  
These will be used to identify messages and convert their content from raw bytes into human readable formats.


*Note: If you have access to the internal files at 4QT gmbh, you can run the following to get the internal code.*

```bash
git submodule update --init --recursive
```


### Extracting .mf4 to csv
This tool will do a bulk extraction of any messages that it can decode with the given DBC files.  

Simply run:
```python
python mf4_to_csv.py
```

The tool will prompt you to give the path to the `.mf4` file you would like to decode and will output the results to `./processed_files/`

### Visualising with the dashboard
A draft dashboard is currently availible in the `webapp.py`.  
It will take in a `.csv` file and allow you to choose which messages to display. 

To serve it, just run the following code and follow the link in your browser:
```python
panel serve src/webapp.py
```

Here is a preview of what you would see at [http://localhost:5006/webapp?theme=dark ](http://localhost:5006/webapp?theme=dark)
<img width="1170" alt="image" src="https://github.com/user-attachments/assets/f5cd65bf-815f-4611-9185-afcfc6308789">


If you would like to make any changes while developing, this command will let you see the results live:
```python
panel serve src/webapp.py --autoreload
```
There is doccumentation for Panel availible [here](https://panel.holoviz.org) on the home page of this awesome project. 


