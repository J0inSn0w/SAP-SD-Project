CREATE SCHEMA IF NOT EXISTS sap_raw;

-- ===== Master data =====
CREATE TABLE sap_raw.kna1 (            -- Customer: general data
    kunnr  char(10) NOT NULL,
    name1  varchar(35),
    land1  char(3),
    ort01  varchar(35),
    adrnr  char(10),
    PRIMARY KEY (kunnr)
);

CREATE TABLE sap_raw.tvko (            -- Sales organization
    vkorg  char(4) NOT NULL,
    bukrs  char(4),
    PRIMARY KEY (vkorg)
);

CREATE TABLE sap_raw.knvv (            -- Customer: sales data per sales area
    kunnr  char(10) NOT NULL,
    vkorg  char(4)  NOT NULL,
    vtweg  char(2)  NOT NULL,
    spart  char(2)  NOT NULL,
    kdgrp  char(2),
    kalks  char(1),
    PRIMARY KEY (kunnr, vkorg, vtweg, spart),
    FOREIGN KEY (kunnr) REFERENCES sap_raw.kna1 (kunnr),
    FOREIGN KEY (vkorg) REFERENCES sap_raw.tvko (vkorg)
);

CREATE TABLE sap_raw.mara (            -- Material: general data
    matnr  char(40) NOT NULL,
    PRIMARY KEY (matnr)
);

CREATE TABLE sap_raw.makt (            -- Material: description by language
    matnr  char(40) NOT NULL,
    spras  char(1)  NOT NULL,
    maktx  varchar(40),
    PRIMARY KEY (matnr, spras),
    FOREIGN KEY (matnr) REFERENCES sap_raw.mara (matnr)
);

-- ===== Billing =====
CREATE TABLE sap_raw.vbrk (            -- Billing document: header
    vbeln  char(10) NOT NULL,
    fkart  char(4),
    vbtyp  char(1),                    -- M invoice, O credit memo, N cancellation
    fkdat  date,
    kunag  char(10),
    vkorg  char(4),
    vtweg  char(2),
    spart  char(2),
    waerk  char(5),                    -- MXN, USD...
    knumv  char(10),
    fksto  char(1),                    -- 'X' = cancelled
    PRIMARY KEY (vbeln),
    FOREIGN KEY (kunag) REFERENCES sap_raw.kna1 (kunnr),
    FOREIGN KEY (vkorg) REFERENCES sap_raw.tvko (vkorg),
    FOREIGN KEY (kunag, vkorg, vtweg, spart)
        REFERENCES sap_raw.knvv (kunnr, vkorg, vtweg, spart)
);

CREATE TABLE sap_raw.vbrp (            -- Billing document: items
    vbeln  char(10) NOT NULL,
    posnr  char(6)  NOT NULL,          -- '000010' (NUMC: text with leading zeros)
    matnr  char(40),
    fkimg  numeric(13,3),
    vrkme  char(3),                    -- sales unit
    netwr  numeric(15,2),
    PRIMARY KEY (vbeln, posnr),
    FOREIGN KEY (vbeln) REFERENCES sap_raw.vbrk (vbeln),
    FOREIGN KEY (matnr) REFERENCES sap_raw.mara (matnr)
);
