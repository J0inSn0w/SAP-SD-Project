BEGIN; 
-- ============================================
-- transform_dw.sql
-- Llena el schema dw a partir de sap_raw
-- Orden: dimensiones primero, fact al final
-- ============================================

-- --dim_calendar--
INSERT INTO dw.dim_calendar(date,year,quarter,month,month_name,day,day_of_week,day_name,week_of_year,is_weekend,is_holiday)
SELECT 
	calendar::date as date,
	EXTRACT(YEAR FROM calendar) AS year,
	EXTRACT(QUARTER FROM calendar) AS quarter,
	EXTRACT(MONTH FROM calendar) AS month,
	TRIM(TO_CHAR(calendar,'TMMonth')) as month_name,
	EXTRACT(DAY FROM calendar) AS day,
	EXTRACT(ISODOW FROM calendar) AS day_of_week,
	TRIM(TO_CHAR(calendar,'TMDay')) as day_name,
	EXTRACT(WEEK FROM calendar) AS week_of_year,
	CASE
		WHEN EXTRACT(ISODOW FROM calendar) IN (6,7) THEN TRUE ELSE FALSE
	END AS is_weekend,
	CASE
		WHEN calendar::date IN ('2025-01-01', '2025-02-03', '2025-03-17', '2025-05-01', '2025-09-16', '2025-11-17', '2025-12-25', '2026-01-01', '2026-02-02', '2026-03-16', '2026-05-01', '2026-09-16', '2026-11-16', '2026-12-25') THEN TRUE ELSE FALSE
	END AS is_holiday
FROM generate_series('2025-01-01', '2026-12-31', INTERVAL '1 day') AS calendar
ON CONFLICT(date) DO NOTHING;

-- --dim_material--
INSERT INTO dw.dim_material(matnr,description)
SELECT matnr, 
	   maktx AS description
FROM sap_raw.makt
WHERE spras = 'S'
ON CONFLICT(matnr) DO NOTHING;

-- --dim_org_sales--
INSERT INTO dw.dim_org_sales(vkorg,company_code)
SELECT vkorg, 
	   bukrs AS company_code
FROM sap_raw.tvko
ON CONFLICT(vkorg) DO NOTHING;

-- --dim_client--
INSERT INTO dw.dim_client(kunnr,name,land,city,vkorg,vtweg,spart,customer_group)
SELECT a.kunnr::char(10),             -- 👈 Forzamos tipo char(10)
	   b.name1 AS name,
	   b.land1 AS land,
	   b.ort01 AS city,
	   a.vkorg::char(4),              -- 👈 Forzamos tipo char(4)
	   a.vtweg::char(2),              -- 👈 Forzamos tipo char(2)
	   a.spart::char(2),              -- 👈 Forzamos tipo char(2)
	   a.kdgrp AS customer_group
FROM sap_raw.knvv AS a 
LEFT JOIN sap_raw.kna1 AS b ON a.kunnr = b.kunnr
ON CONFLICT(kunnr, vkorg, vtweg, spart) DO NOTHING;

COMMIT;