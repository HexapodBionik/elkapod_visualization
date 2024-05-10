# Elkapod Visualization repository
![ROS2 distro](https://img.shields.io/badge/ros--version-humble-blue)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![Python Version](https://img.shields.io/badge/python-3.10-g.svg)

This repository contains ROS2 packages needed for Elkapod mobile robot vizualization.

## Installation
1. Create a workspace and clone packages into it
```bash
mkdir -p elkapod_vis/src/
git clone https://github.com/HexapodBionik/elkapod_visualization.git elkapod_vis/src/
```
2. Move into `src/` folder and download all additional packages using [vcstool](http://wiki.ros.org/vcstool)
```bash
cd elkapod_vis/src/
vcs import . < repos.yaml
```
3. Install all needed python packages 
```bash
pip install -r requirements.txt 
```