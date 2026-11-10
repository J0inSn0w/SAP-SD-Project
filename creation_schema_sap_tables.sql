CREATE SCHEMA IF NOT EXISTS sap_raw;

-- ===== Maestros =====
CREATE TABLE sap_raw.kna1 (            -- Cliente: datos generales
    kunnr  char(10) NOT NULL,
    name1  varchar(35),
    land1  char(3),
    ort01  varchar(35),
    adrnr  char(10),
    PRIMARY KEY (kunnr)
);

CREATE TABLE sap_raw.tvko (            -- Organización de ventas
    vkorg  char(4) NOT NULL,
    bukrs  char(4),
    PRIMARY KEY (vkorg)
);

CREATE TABLE sap_raw.knvv (            -- Cliente: datos de ventas por área
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

CREATE TABLE sap_raw.mara (            -- Material: datos generales
    matnr  char(40) NOT NULL,
    PRIMARY KEY (matnr)
);

CREATE TABLE sap_raw.makt (            -- Material: descripción por idioma
    matnr  char(40) NOT NULL,
    spras  char(1)  NOT NULL,
    maktx  varchar(40),
    PRIMARY KEY (matnr, spras),
    FOREIGN KEY (matnr) REFERENCES sap_raw.mara (matnr)
);

-- ===== Facturación =====
CREATE TABLE sap_raw.vbrk (            -- Factura: encabezado
    vbeln  char(10) NOT NULL,
    fkart  char(4),
    vbtyp  char(1),                    -- M factura, O nota de crédito, N cancelación
    fkdat  date,
    kunag  char(10),
    vkorg  char(4),
    vtweg  char(2),
    spart  char(2),
    waerk  char(5),                    -- MXN, USD...
    knumv  char(10),
    fksto  char(1),                    -- 'X' = cancelada
    PRIMARY KEY (vbeln),
    FOREIGN KEY (kunag) REFERENCES sap_raw.kna1 (kunnr),
    FOREIGN KEY (vkorg) REFERENCES sap_raw.tvko (vkorg),
    FOREIGN KEY (kunag, vkorg, vtweg, spart)
        REFERENCES sap_raw.knvv (kunnr, vkorg, vtweg, spart)
);

CREATE TABLE sap_raw.vbrp (            -- Factura: renglones
    vbeln  char(10) NOT NULL,
    posnr  char(6)  NOT NULL,          -- '000010' (NUMC: texto con ceros)
    matnr  char(40),
    fkimg  numeric(13,3),
    vrkme  char(3),                    -- unidad de venta
    netwr  numeric(15,2),
    PRIMARY KEY (vbeln, posnr),
    FOREIGN KEY (vbeln) REFERENCES sap_raw.vbrk (vbeln),
    FOREIGN KEY (matnr) REFERENCES sap_raw.mara (matnr)
);
