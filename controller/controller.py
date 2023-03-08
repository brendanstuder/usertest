"""
Fast API controller to query the module

author: Brendan Studer
date: 2022-12-07

"""
from typing import Union
from fastapi import FastAPI
from src.wallet import Wallet
import json

app = FastAPI()

@app.get("/")
async def get_module():
    """
    Query module
    """
    return {
        "module": {
            "name": "TP2",
            "description": "Un exercice sur le CI/CD",
            "version": "1.0"
        }
    }

@app.get("/wallet-with-100")
async def get_wallet():
    """
    Query module
    """
    wallet = Wallet(100)
    return {
        "balance": wallet.balance
    }
