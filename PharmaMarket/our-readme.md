## Introduction
In the course "Databases and Information Systems" we have been tasked to make an interactive database.
We have chosen to make an online pharmacy, where customers can buy medicine, and pharmacists can sell medicine. 

Our database consists of the following keys:

id : The ID number
name : The name of the drug
brand : The brand of the drug
price : The price of the drug
city : The city the drug is manufactured in

## How to run the project:
To run the project, you should first clone the repository, then follow the steps below.
1. Before you start
2. Downloading the requirements
3. Scripts to initalise databse
4. How to compile your web-app from source

## Before you start:
Initially you should find the .env file, it is located in the root folder of the project then a new database should be made in pgAdmin4. This database should be the same, as the one found in our .env file, it currently has the following contents, but can be changed to your liking:

        SECRET_KEY=b'\x1f\xb9_Q\xfb&\x8f\x0bD\xcf\xdbr\xac\x0f6CN\xc8\xc8\xa3\xfa)\xbem\xc9P\xd8?\xcd\xc8!0'
        DB_USERNAME=postgres
        DB_PASSWORD=parola
        DB_NAME=PharmaMarket

## Downloading the requirements:
The requirements found in requirements.txt should be downloaded and installed. This can be done by running the following command in the terminal:

`pip install -r requirements.txt`

## Scripts to initalise databse:
To run the database, start by running the "init_db.py", which is located inside the utils folder:

`cd PharmaMarket/utils/`
`python init_db.py`

When the above command is ran, it will return "Connected to the database!".

## How to compile your web-app from source:
Inside the PharmaMarket-folder, the following command should be ran in the terminal:
`flask run`

The website can now be opened in a browser like Google Chrome with the following link:
http://127.0.0.1:5000

## Problems with our implementation:
Both pharmacist and customers can see "Add drugs" and "My drugs" page, but only the pharmacist can access the page, or make add drugs. The customer will get an error that says: "".
When a customer is on the drug page, after pressing buy on it, he can either choose the go back, or buy it. When he presses buy it, it is added to his orders, but it won't tell him, unless he goes to that specific page. Therefore the customer can keep on pressing buy it, and will end up adding a lot of products to his/her orders.