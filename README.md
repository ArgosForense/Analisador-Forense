# Analisador-Forense

## Autores

| [<img src="https://avatars.githubusercontent.com/u/128331199?v=4" width=115><br><sub>Kennedy Torres</sub>](https://github.com/Kennedy-Torres) |[<img src="https://avatars.githubusercontent.com/u/111468952?v=4" width=115><br><sub>Nathalia GS</sub>](https://github.com/nathi-gs) |[<img src="https://avatars.githubusercontent.com/u/116228124?v=4" width=115><br><sub>Pedro Marques</sub>](https://github.com/phxdablio) |[<img src="https://avatars.githubusercontent.com/u/101297032?v=4" width=115><br><sub>Gustavo Horeste</sub>](https://github.com/GustavoHoreste) |[<img src="https://avatars.githubusercontent.com/u/71994927?v=4" width=115><br><sub>Matheus Vinycius</sub>](https://github.com/matheus58) |
| :---: | :---: | :---: | :---: | :---: |
# Final Project - Forensic Analyzer

## Project Overview
This project is a forensic analysis system developed as a university assignment.  
Its main goal is to **collect and analyze machine activity logs** from a company to ensure network security.

---

## Technologies Used
- **MongoDB**: NoSQL database used to store logs in a flexible and scalable way.  
  MongoDB is ideal for this project as it efficiently handles the varied nature of log data.

- **Entity-Relationship Model (ERM)**:  
  The ER diagram was designed to logically structure the database, ensuring that all entities and their relationships (such as *Users, Profiles,* and *Permissions*) were well-defined before implementation.

---

## Database Structure
The database, named **ArgosDB**, is composed of 7 main collections:

1. **EMPRESA** – Stores company information.  
2. **GESTOR** – Contains data about the manager responsible for the system.  
3. **USUARIOS** – Stores information about users (analysts and employees).  
4. **PERFIL** – Defines types of access profiles.  
5. **PERMISSAO** – Contains the system’s permission list.  
6. **PERFIL_PERMISSAO** – Associative collection that links profiles and permissions.  
7. **LOG** – Main collection for storing activity logs.  

---

## Setup & Creation Scripts
The database creation scripts are available inside the **`scripts/`** folder.  
To run them:

1. Connect to your MongoDB instance using **mongosh**.  
2. Execute the scripts to create the database and collections.  

---

## How It Works
The system is divided into two main parts:

1. **Data Collection**:  
   An agent (script) is installed on company machines, which sends activity logs to the cloud-hosted MongoDB database.

2. **Analysis & Management**:  
   The manager accesses a control panel (system backend) to view, analyze, and manage logs, using the permissions and structure defined in the ERM.

---

## Summary
This project demonstrates the use of **forensic data analysis with MongoDB**.  
It highlights both the technical implementation (database structure and scripts) and the security management approach (log analysis and access control).  

This README serves as a professional summary of the project and the technologies used.
