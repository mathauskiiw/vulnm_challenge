
# Vulnm (Vulnerability Mapper)
Greetings, this repository holds the code for a Django REST API for storing/retrieving info about  assets and their vulnerabilities 
##  API
This repository features a fully *containerized* environment consisting of the following images:
  - Django (version 3.1.2)
  - PostgreSQL (latest)
  - Nginx (mainline-alpine)

#### Other information
 - OS
 -- [Manjaro (Kernel 5.8.16-2)](https://manjaro.org/get-manjaro/)
 - Language
 -- [Python 3.8.5](https://hub.docker.com/_/python/)
	 --- Libraries used: 
			 djangorestframework=3.12.1
			 psycopg2-binary=2.8.6
			 gunicorn=20.0.4
			 django-extensions=3.0.9
			 

# Setup 
1. Requisites
*  clone the repository localy
 

> $ git clone git@github.com:mathauskiiw/vulnm_challenge.git

* Then, paste a project.ENV at the project's root 
 

> $ cp ~/<project.ENV file path> ./vulnm_challenge

* Place a .csv file into the *commands* folder  *(optional)*
 

> $ cp ~/<assets.csv file path> ./djangobackend/api/management/commands/

 * Install docker & docker-compose

2. Instalation & Docker
* To run the application, simply run the docker-compose file from projects' root 

> $ docker-compose run --build

* Docker will automatically download and build the images, after that the service is gonna be available at 


> localhost:1337/

3. Postman
To ease the operation, there's a postman collection that contains the API endpoints for the application located at : 
[/vulnm_challenge/postman/djangoapi.postman_collection.json]()
 Only need to import it into postman and send requests while the server is running.
# Structure

## Models
 The following models where implemented to attain the desired behavior, those where:
### Asset
 1. Summary:
- Asset model represents the machines imported from the file.
 2. Attributes:
 - Asset.pk -> Primary Key field
 - Asset.hostname -> String field
 - Asset.ip_address -> String field with IPV4 mask validation
 - Asset.vulns -> Foreign Key field ( to Vulnerability model as Many to Many)
 3. Properties (Dynamically updated): 
  
 - Asset.risk
 #=> returns the ratio of the **risk** of vulns not solved by the **count** vulns not solved 
  
 - Asset.vuln_count
 #=> returns the count of vulnerabilities linked to this asset that weren't solved

### Vulnerability
 1. Summary:
- Vulnerability model represents the vulnerabilities imported with the assets
 2. Attributes:
 - Vulnerability.pk -> Primary Key field
 - Vulnerability.title -> String field
 - Vulnerability.severity -> String field
 - Vulnerability.cvss -> Float field (0 to 10 validation)
 - Vulnerability.pub_date -> Date field
 - Vulnerability.hosts -> Foreign Key field( to Assets model)
 
 3. Properties:
 - Vulnerabity.affected_count
 #=> returns the count of hosts currently affected by this vulnerability (Solved = False)

  
### VulnStatus
1. Summary:
- Through model to represent the Asset<->Vulnerability relation and store the vulnerability status (solved or not).
- Each VulnStatus is unique for a (Asset, Vulnerability) pair
2. Attributes:
- VulnStatus.solved-> Boolean field

## Endpoints
### Assets
- [GET]   ->  /assets/?page=1 
-- Asset list *(pagination parameter optional)*
- [GET]  -> /assets/?vuln=20
-- Asset list filtering by vulnerabilty_pk
- [GET] ->  /assets/<asset_pk>
-- Asset detail view
- [PUT] -> /assets/<asset_pk>/vuln/<vuln_pk>
-- Update the solved status for the specified asset's vulnerability (has a toggle behavior) 

### Vulnerability
- [GET]   ->  /vulnerabilities/?page=1 
-- Vulnerabilities list *(pagination parameter optional)*
- [GET]  -> /vulnerability/?asset=1&severity=baixo
-- Vulnerabilities list fltering by asset or/and severity 



## Author
- Mathaus Eugênio - Maintainer // [Gitlab](https://gitlab.com/hideonsouls) - [LinkedIn](https://www.linkedin.com/in/mathaus-eug%C3%AAnio-01b065b7/)
## License
This project is licensed under the MIT license, see LICENSE.md file for more details