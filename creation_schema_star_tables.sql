CREATE SCHEMA IF NOT EXISTS dw;

CREATE TABLE dw.dim_client (
    client_key     serial NOT NULL,
    kunnr          char(10) NOT NULL,
    name           varchar(35),
    land           char(3),
    city           varchar(35),
    vkorg          char(4) NOT NULL,
    vtweg          char(2) NOT NULL,
    spart          char(2) NOT NULL,
    customer_group char(2),
    channel_name   varchar(20),
    customer_group_name varchar (30),
    PRIMARY KEY (client_key),
    UNIQUE (kunnr, vkorg, vtweg, spart)
);

CREATE TABLE dw.dim_calendar (
    date         date NOT NULL,
    year         smallint,
    quarter      smallint,
    month        smallint,
    month_name   varchar(15),
    year_month   char(7),                -- '2025-01': monthly axis without mixing years
    day          smallint,
    day_of_week  smallint,
    day_name     varchar(15),
    week_of_year smallint,
    is_weekend   boolean,
    is_holiday   boolean,
    PRIMARY KEY (date)
);

CREATE TABLE dw.dim_material (
    matnr       char(40) NOT NULL,
    description varchar(40),
    PRIMARY KEY (matnr)
);

CREATE TABLE dw.dim_org_sales (
    vkorg        char(4) NOT NULL,
    company_code char(4),
    sales_org_name  varchar(30),
    PRIMARY KEY (vkorg)
);

CREATE TABLE dw.fact_sales (
    vbeln        char(10) NOT NULL,
    posnr        char(6) NOT NULL,
    date         date NOT NULL,
    matnr        char(40) NOT NULL,
    vkorg        char(4) NOT NULL,
    client_key   int NOT NULL,
    fkart        char(4),
    quantity     numeric(13, 3),
    vrkme        char(3),
    net_amount   numeric(15, 2),
    waerk        char(5),
    amount_mxn   numeric(15, 2),
    sign         smallint,
    is_cancelled boolean,
    PRIMARY KEY (vbeln, posnr),
    FOREIGN KEY (date)       REFERENCES dw.dim_calendar (date),
    FOREIGN KEY (client_key) REFERENCES dw.dim_client (client_key),
    FOREIGN KEY (matnr)      REFERENCES dw.dim_material (matnr),
    FOREIGN KEY (vkorg)      REFERENCES dw.dim_org_sales (vkorg)
);
