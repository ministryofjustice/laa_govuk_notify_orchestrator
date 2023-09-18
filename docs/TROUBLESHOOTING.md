# Troubleshooting

#### 1) Check you are using a Python virtual environment

```
python3.11 -m venv env --prompt=\(notify_api\)

source env/bin/activate
```

#### 2) Check you are using the correct Python/ Pip version (3.11)

```
python --version

pip --version
```

#### 3) Check you have installed all required python dependancies

```
pip install -U pip

pip install -r requirements.txt
```
