

--------------------------------------------------------
--  DDL for Table CONNECTING_STRING
--------------------------------------------------------

  CREATE TABLE "CONNECTING_STRING" 
   (    "ID" NUMBER(*,0), 
    "HOST_NAME" VARCHAR2(60 BYTE), 
    "DB_PORT" VARCHAR2(5 BYTE), 
    "DB_SERVICE_NAME" VARCHAR2(40 BYTE), 
    "DB_USER" VARCHAR2(40 BYTE), 
    "DB_PASSWORD" VARCHAR2(40 BYTE)
   ) SEGMENT CREATION IMMEDIATE 
  PCTFREE 10 PCTUSED 40 INITRANS 1 MAXTRANS 255 
 NOCOMPRESS LOGGING
  STORAGE(INITIAL 65536 NEXT 1048576 MINEXTENTS 1 MAXEXTENTS 2147483645
  PCTINCREASE 0 FREELISTS 1 FREELIST GROUPS 1
  BUFFER_POOL DEFAULT FLASH_CACHE DEFAULT CELL_FLASH_CACHE DEFAULT)
  TABLESPACE "ORACLECHECKER" ;


  
  
-------------------------------------------------------------------------------------------


-- database inventory
INSERT INTO connecting_string VALUES(1, 'dbhost001.domain.com', 1523, 'hr', 'dbsnmp', 'password');
INSERT INTO connecting_string VALUES(2, 'dbhost002.domain.com', 1521, 'crm', 'dbsnmp', 'password');
INSERT INTO connecting_string VALUES(3, 'dbhost003.domain.com', 1521, 'sales', 'dbsnmp', 'password');
INSERT INTO connecting_string VALUES(4, 'dbhost004.domain.com', 1521, 'db_sap', 'dbsnmp', 'password');
INSERT INTO connecting_string VALUES(5, 'dbhost005.domain.com', 1530, 'hr_tst', 'dbsnmp', 'password');
INSERT INTO connecting_string VALUES(6, 'dbhost006.domain.com', 1531, 'crm_tst', 'dbsnmp', 'password');
commit;





