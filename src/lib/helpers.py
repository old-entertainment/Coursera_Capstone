#!/usr/bin/python3
"""Outsiders"""
import os

PROJECT_DIR = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))
DATASETS_DIR = PROJECT_DIR + '/datasets/'
MEDIA_DIR = PROJECT_DIR + '/media/'

def prepare_query(query):
    """Strip all except words"""
    return ''.join(e for e in query if e.isalnum())
