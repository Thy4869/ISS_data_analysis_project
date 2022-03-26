from app import get_data, get_position, appInfo
from flask import Flask
import pytest, json

def test_get_data():
    assert get_data() == 'Download Completed\n'

def test_get_position():
    assert isinstance(get_position('Epochs'), dict) == True

def test_appInfo():
    assert isinstance(appInfo(), str) == True 
    
