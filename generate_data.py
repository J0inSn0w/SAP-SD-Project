import random 
import pandas as pd
from sqlalchemy import create_engine,text
from faker import Faker
from datetime import date

random.seed(42)
Faker.seed(42)

fake = Faker("es_MX")

engine = create_engine("postgresql+psycopg2://USER:PASSWORD@localhost:5432/postgres")

# CONS --KNVV--

canales  = ["10", "20"]            # 10 mayoreo, 20 minoreo
sectores = ["00"]                  # sector general
grupos   = ["01", "02", "03"]      # grupos de clientes

# CONS --MAKT--

materiales = [
    ("Tornillo hexagonal M8", "M8 Hex Bolt"),
    ("Tuerca hexagonal M8", "M8 Hex Nut"),
    ("Arandela plana M8", "M8 Flat Washer"),
    ("Remache de aluminio", "Aluminum Rivet"),
    ("Rodamiento de bolas 6204", "6204 Ball Bearing"),
    ("Banda de transmisión en V", "V-Belt"),
    ("Cadena de transmisión industrial", "Industrial Drive Chain"),
    ("Motor eléctrico de 2 HP", "2 HP Electric Motor"),
    ("Reductor de velocidad", "Speed Reducer"),
    ("Acoplamiento de eje", "Shaft Coupling"),
    ("Sensor inductivo M12", "M12 Inductive Sensor"),
    ("Sensor fotoeléctrico", "Photoelectric Sensor"),
    ("Interruptor de límite", "Limit Switch"),
    ("Controlador lógico programable (PLC)", "Programmable Logic Controller (PLC)"),
    ("Contactor eléctrico de 24 V", "24 V Electrical Contactor"),
    ("Relevador de control", "Control Relay"),
    ("Fusible de 10 A", "10 A Fuse"),
    ("Cable eléctrico de cobre", "Copper Electrical Cable"),
    ("Conector eléctrico industrial", "Industrial Electrical Connector"),
    ("Fuente de alimentación de 24 V CC", "24 V DC Power Supply"),
    ("Válvula solenoide neumática", "Pneumatic Solenoid Valve"),
    ("Cilindro neumático", "Pneumatic Cylinder"),
    ("Manguera neumática", "Pneumatic Hose"),
    ("Filtro de aire comprimido", "Compressed Air Filter"),
    ("Manómetro de presión", "Pressure Gauge"),
    ("Tubería de acero inoxidable", "Stainless Steel Pipe"),
    ("Lámina de acero al carbono", "Carbon Steel Sheet"),
    ("Barra de aluminio", "Aluminum Bar"),
    ("Grasa lubricante industrial", "Industrial Lubricating Grease"),
    ("Aceite hidráulico", "Hydraulic Oil")
]

# CONS --VBRK--

n_facturas = 500

# vbtyp -> fkart, para que siempre coincidan
tipos_doc = {"M": "F2", "O": "G2"}

moneda_por_org = {"MX01": "MXN", "US01": "USD"}

# --TVKO--

tvko = pd.DataFrame([
    {"vkorg":"MX01","bukrs":"1000"},
    {"vkorg":"US01","bukrs":"2000"}
])

sql_tvko = text("""
    INSERT INTO sap_raw.tvko (vkorg, bukrs)
    VALUES (:vkorg, :bukrs)
    ON CONFLICT (vkorg) DO NOTHING;
""")

datos_tvko = tvko.to_dict(orient="records")

# --KNA1--
n_clientes = 10
num = random.sample(range(1,100000000),k=n_clientes)

kna1 = pd.DataFrame(
    {
     "kunnr":[str(n).zfill(10) for n in num],
     "name1":[fake.name() for i in range(n_clientes)],
     "land1":[random.choice(["MEX","USA"]) for i in range(n_clientes)],
     "ort01":[fake.city() for i in range(n_clientes)],
     "adrnr":[str(random.randint(1,100000000)) for i in range(n_clientes)]
     }
)

sql_kna1 = text("""
    INSERT INTO sap_raw.kna1
        (kunnr, name1, land1, ort01, adrnr)
    VALUES
        (:kunnr, :name1, :land1, :ort01, :adrnr)
    ON CONFLICT (kunnr) DO NOTHING;
""")

datos_kna1 = kna1.to_dict(orient="records")

# --KNVV--

filas_knvv = []
vkorgs = tvko["vkorg"].to_list()

for kunnr in kna1["kunnr"]:
    # ¿En cuántas organizaciones de ventas vende este cliente? (1 o 2)
    n_orgs = random.randint(1,len(vkorgs))
    orgs = random.sample(vkorgs,k=n_orgs)

    for vkorg in orgs:
        filas_knvv.append({
            "kunnr":kunnr,
            "vkorg":vkorg,
            "vtweg":random.choice(canales),
            "spart":random.choice(sectores),
            "kdgrp":random.choice(grupos),
            "kalks":1
        })

knvv = pd.DataFrame(filas_knvv)  

sql_knvv = text("""
    INSERT INTO sap_raw.knvv
        (kunnr, vkorg, vtweg, spart, kdgrp,kalks)
    VALUES
        (:kunnr, :vkorg, :vtweg, :spart, :kdgrp, :kalks)
    ON CONFLICT (kunnr, vkorg, vtweg, spart) DO NOTHING;
""")

datos_knvv = knvv.to_dict(orient="records")

# --MARA--

n_materiales = 30
num = random.sample(range(1,10000000000000),k=n_materiales)

mara = pd.DataFrame({

    "matnr":[str(n).zfill(40) for n in num]
    
})

sql_mara = text("""
    INSERT INTO sap_raw.mara
        (matnr)
    VALUES
        (:matnr)
    ON CONFLICT (matnr) DO NOTHING;
""")

datos_mara = mara.to_dict(orient="records")

# --MAKT--

filas_makt = []

for matnr in mara["matnr"]:
    esp,eng = random.choice(materiales)

    filas_makt.append({"matnr":matnr,"spras":"S","maktx":esp})
    filas_makt.append({"matnr":matnr,"spras":"E","maktx":eng})

makt = pd.DataFrame(filas_makt)

sql_makt = text("""
    INSERT INTO sap_raw.makt
        (matnr,spras,maktx)
    VALUES
        (:matnr,:spras,:maktx)
    ON CONFLICT (matnr,spras) DO NOTHING;
""")

datos_makt = makt.to_dict(orient="records")

# --VBRK--

filas_vbrk = []

areas = knvv.to_dict(orient="records")

for i in range(n_facturas):
    area = random.choice(areas)

    vbtyp = random.choices(["M","O"],weights=[80,20])[0]
    fkart = tipos_doc[vbtyp]

    filas_vbrk.append({
        "vbeln": str(90000001 + i).zfill(10),
        "fkart": fkart,
        "vbtyp": vbtyp,
        "fkdat": fake.date_between(start_date=date(2025, 1, 1), end_date="today"),
        "kunag": area["kunnr"],                 # ojo: en knvv se llama distinto
        "vkorg": area["vkorg"],
        "vtweg": area["vtweg"],
        "spart": area["spart"],
        "waerk": moneda_por_org[area["vkorg"]],
        "knumv": None,
        "fksto": random.choices(["X",""],weights=[3,97])[0],                       
    })

vbrk = pd.DataFrame(filas_vbrk)

sql_vbrk = text("""
    INSERT INTO sap_raw.vbrk
        (vbeln,fkart,vbtyp,fkdat,kunag,vkorg,vtweg,spart,waerk,knumv,fksto)
    VALUES
        (:vbeln,:fkart,:vbtyp,:fkdat,:kunag,:vkorg,:vtweg,:spart,:waerk,:knumv,:fksto)
    ON CONFLICT (vbeln) DO NOTHING;
""")

datos_vbrk = vbrk.to_dict(orient="records")

# --VBRP--

filas_vbrp = []

materiales_lista = mara["matnr"].to_list()

precio_por_material = {matnr: round(random.uniform(10, 2000), 2)
                       for matnr in mara["matnr"]}

for factura in vbrk.to_dict(orient="records"):
    n_renglones = random.randint(1, 5)
    mats = random.sample(materiales_lista, k=n_renglones)          # sin repetir material en la factura

    for j, matnr in enumerate(mats, start=1):
        fkimg = random.randint(1,100)
        precio = precio_por_material[matnr]

        filas_vbrp.append({
            "vbeln":factura["vbeln"],
            "posnr":str(j * 10).zfill(6),
            "matnr":matnr,
            "fkimg":fkimg,
            "vrkme":"ST",
            "netwr":round(fkimg*precio,2)
        })

vbrp = pd.DataFrame(filas_vbrp)

sql_vbrp = text("""
    INSERT INTO sap_raw.vbrp
        (vbeln,posnr,matnr,fkimg,vrkme,netwr)
    VALUES
        (:vbeln,:posnr,:matnr,:fkimg,:vrkme,:netwr)
    ON CONFLICT (vbeln, posnr) DO NOTHING;
""")

datos_vbrp = vbrp.to_dict(orient="records")

# --dim_calendar--

calendar_query = text(""" 
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
    ON CONFLICT(date) DO NOTHING """)

# --dim_material--

filas_dim_material = []

lista_makt = makt[makt["spras"] == "S"]

for material in lista_makt.to_dict(orient="records"):
    
    filas_dim_material.append({
        "matnr":material["matnr"],
        "description":material["maktx"]
    })

dim_material = pd.DataFrame(filas_dim_material)

sql_dim_material = text("""
    INSERT INTO dw.dim_material
        (matnr,description)
    VALUES
        (:matnr,:description)
    ON CONFLICT (matnr) DO NOTHING;
""")

datos_dim_material = dim_material.to_dict(orient="records")

# --dim_org_sales--

filas_dim_org_sales = []

for sales1 in tvko.to_dict(orient="records"):
    
    filas_dim_org_sales.append({
        "vkorg":sales1["vkorg"],
        "company_code":sales1["bukrs"]
    })

dim_org_sales = pd.DataFrame(filas_dim_org_sales)

sql_dim_org_sales = text("""
    INSERT INTO dw.dim_org_sales
        (vkorg,company_code)
    VALUES
        (:vkorg,:company_code)
    ON CONFLICT (vkorg) DO NOTHING;
""")

datos_dim_org_sales = dim_org_sales.to_dict(orient="records")

# --dim_client--

filas_dim_client = []




with engine.begin() as conn:
    conn.execute(sql_tvko,datos_tvko)
    conn.execute(sql_kna1,datos_kna1)
    conn.execute(sql_knvv,datos_knvv)
    conn.execute(sql_mara,datos_mara)
    conn.execute(sql_makt,datos_makt)
    conn.execute(sql_vbrk,datos_vbrk)
    conn.execute(sql_vbrp,datos_vbrp)
    conn.execute(calendar_query)
    conn.execute(sql_dim_material,datos_dim_material)
    conn.execute(sql_dim_org_sales,datos_dim_org_sales)



print("Carga finalizada sin duplicar las claves existentes.")

