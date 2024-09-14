import os


class Config:

	SQLALCHEMY_DATABASE_URI ='sqlite:///mydatabasedb'
	SQLALCHEMY__TRACK__MODIFICATIONS = False
	LOGGING_FILE = 'error.log'
	TIMEZONE = 'Asia/Kolkata'  
