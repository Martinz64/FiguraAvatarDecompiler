# Figura Avatar decompiler

## Supported Figura version: 0.1.0-rc14

## WARNING
This code is so janky that attempting to understand it may give you brian cancer

## Basic usage instructions

Make a directory to extract the Avatar contents into:
```
mkdir extracted
cd extracted
```

Run nbt1.py on the .moon file
```
python3 ../nbt1.py <avatar>.moon
```

Run convert_to_bbmodel.py
```
python3 ../convert_to_bbmodel.py
```
Your avatar files should appear in the current directory 