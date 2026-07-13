#This file is the main entry of the project
#This file imports all the routers from app/routers
#This file also imports all other files needed to run the project like database connection


from fastapi import FastAPI, Router, HTTPException


app = FastAPI()

