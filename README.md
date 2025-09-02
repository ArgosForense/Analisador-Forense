# Analisador-Forense

## Autores

| [<img src="https://avatars.githubusercontent.com/u/128331199?v=4" width=115><br><sub>Kennedy Torres</sub>](https://github.com/Kennedy-Torres) |[<img src="https://avatars.githubusercontent.com/u/111468952?v=4" width=115><br><sub>Nathalia GS</sub>](https://github.com/nathi-gs) |[<img src="https://avatars.githubusercontent.com/u/116228124?v=4" width=115><br><sub>Pedro Marques</sub>](https://github.com/phxdablio) |[<img src="https://avatars.githubusercontent.com/u/101297032?v=4" width=115><br><sub>Gustavo Horeste</sub>](https://github.com/GustavoHoreste) |[<img src="https://avatars.githubusercontent.com/u/71994927?v=4" width=115><br><sub>Matheus Vinycius</sub>](https://github.com/matheus58) |
| :---: | :---: | :---: | :---: | :---: |

# Argos - Forensic Analyzer

This project is a forensic analysis system that collects and manages machine activity logs to improve network security.  
It uses **MongoDB** for scalable log storage and an **ER Model** to define entities like Users, Profiles, and Permissions.  

## Main Collections (ArgosDB)
- **EMPRESA** – Company data  
- **GESTOR** – Manager data  
- **USUARIOS** – Users (analysts/employees)  
- **PERFIL** – Access profiles  
- **PERMISSAO** – Permissions list  
- **PERFIL_PERMISSAO** – Links profiles ↔ permissions  
- **LOG** – Activity logs  

Scripts for database setup are in `scripts/` and can be executed with **mongosh**.  

An agent collects logs from machines and sends them to MongoDB (cloud), while managers use a control panel to analyze and manage data.

