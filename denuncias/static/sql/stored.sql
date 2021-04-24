CREATE PROCEDURE `spXmapa`()
SELECT denuncias_departamentos.id, denuncias_departamentos.mapa as mapa, COUNT(denuncias_quejas.id) as totales
from denuncias_quejas
join denuncias_sucursales on denuncias_sucursales.id = denuncias_quejas.sucursal_id
join denuncias_municipios on denuncias_municipios.id = denuncias_sucursales.municipio_id
join denuncias_departamentos on denuncias_departamentos.id = denuncias_municipios.departamento_id
WHERE denuncias_quejas.estado = TRUE
GROUP BY denuncias_departamentos.mapa


CREATE PROCEDURE `getAllNeg`()
SELECT * FROM denuncias_negocios ORDER BY nombre ASC;

CREATE PROCEDURE `getDepartamentos`()
SELECT * from denuncias_departamentos;

CREATE PROCEDURE `getNegocio`(IN `id_municipio` INT)
SELECT DISTINCT denuncias_negocios.id, denuncias_negocios.nombre
FROM denuncias_negocios
JOIN denuncias_sucursales ON denuncias_sucursales.negocio_id = denuncias_negocios.id
JOIN denuncias_municipios ON denuncias_sucursales.municipio_id = denuncias_municipios.id
WHERE denuncias_municipios.id = id_municipio
ORDER BY denuncias_negocios.nombre ASC;


CREATE PROCEDURE `getSucursales`(`id_municipio` INT, `id_negocio` INT)
SELECT denuncias_sucursales.id, denuncias_sucursales.ubicacion
FROM denuncias_sucursales
JOIN denuncias_municipios ON denuncias_sucursales.municipio_id = denuncias_municipios.id
JOIN denuncias_negocios ON denuncias_sucursales.negocio_id = denuncias_negocios.id
WHERE denuncias_municipios.id = id_municipio
AND denuncias_negocios.id = id_negocio
ORDER BY denuncias_sucursales.ubicacion ASC;


CREATE PROCEDURE `spInsertNegocio`(`in_negocio` VARCHAR(100))
INSERT INTO denuncias_negocios (nombre) VALUES (in_negocio);


CREATE PROCEDURE `spInsertQueja`(in_queja text, in_date datetime, in_sucursal int)
INSERT INTO denuncias_quejas (queja, estado, creacion, sucursal_id) VALUES (in_queja, TRUE, in_date, in_sucursal);


CREATE PROCEDURE `spInsertSucursal`(IN `in_ubicacion` VARCHAR(100), IN `in_municipio` INT, IN `in_negocio` INT)
INSERT INTO denuncias_sucursales (ubicacion, municipio_id, negocio_id) VALUES (in_ubicacion, in_municipio, in_negocio);


CREATE PROCEDURE `spUpdateQueja`(`in_id` int)
UPDATE denuncias_quejas SET estado = FALSE WHERE id = in_id;


CREATE PROCEDURE `spXdeptos`()
SELECT denuncias_departamentos.id, denuncias_departamentos.nombre_dep as deptos, COUNT(denuncias_quejas.id) as totales from denuncias_quejas
join denuncias_sucursales on denuncias_sucursales.id = denuncias_quejas.sucursal_id
join denuncias_municipios on denuncias_municipios.id = denuncias_sucursales.municipio_id
join denuncias_departamentos on denuncias_departamentos.id = denuncias_municipios.departamento_id
WHERE denuncias_quejas.estado = TRUE
GROUP BY denuncias_departamentos.nombre_dep;


CREATE PROCEDURE `spXfechas`()
SELECT NOW() as id, DATE_FORMAT(denuncias_quejas.creacion, '%d-%m-%y') AS creado, 
COUNT(denuncias_quejas.id) AS totales
FROM denuncias_quejas
WHERE denuncias_quejas.estado = TRUE
GROUP BY creado;


CREATE PROCEDURE `spXnegocios`()
SELECT denuncias_negocios.id, denuncias_negocios.nombre as negocios, COUNT(denuncias_quejas.id) as totales from denuncias_quejas
join denuncias_sucursales on denuncias_sucursales.id = denuncias_quejas.sucursal_id
join denuncias_negocios on denuncias_negocios.id = denuncias_sucursales.negocio_id
WHERE denuncias_quejas.estado = TRUE
GROUP BY denuncias_negocios.nombre;


CREATE PROCEDURE `spXregiones`()
SELECT denuncias_regiones.id, denuncias_regiones.nombre_reg as regiones, COUNT(denuncias_quejas.id) as totales from denuncias_quejas
join denuncias_sucursales on denuncias_sucursales.id = denuncias_quejas.sucursal_id
join denuncias_municipios on denuncias_municipios.id = denuncias_sucursales.municipio_id
join denuncias_departamentos on denuncias_departamentos.id = denuncias_municipios.departamento_id
join denuncias_regiones on denuncias_regiones.id = denuncias_departamentos.region_id
WHERE denuncias_quejas.estado = TRUE
GROUP BY denuncias_regiones.nombre_reg;