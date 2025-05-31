-- Poblar tabla empleados
INSERT INTO empleados (nombre, puesto, salario, fecha_contratacion, turno) VALUES
  ('Alejandro Daniel Perez Gomez',    'Bodeguero',               7500.00, '2022-05-15', 'Matutino'),
  ('Maria Fernanda Castillo Ramirez',  'Gerente de Ventas',       8500.00, '2023-07-10', 'Vespertino'),
  ('Carlos Alberto Rivera Mendoza',    'Personal de Limpieza',    7200.00, '2024-11-01', 'Nocturno'),
  ('Ana Sofia Morales Herrera',        'Auxiliar de Ventas',       7800.00, '2025-02-28', 'Matutino'),
  ('Sergio Alejandro Torres Diaz',     'Supervisor de Stock',      8300.00, '2022-12-01', 'Vespertino'),
  ('Patricia Isabel Gómez Sanchez',    'Atención al Cliente',      8000.00, '2023-03-20', 'Matutino'),
  ('Roberto Manuel Diaz Lopez',        'Encargado de Almacén',     8200.00, '2024-06-30', 'Vespertino'),
  ('Veronica Elizabeth Solis Cruz',    'Asistente Administrativo', 7100.00, '2025-04-10', 'Nocturno'),
  ('Lucia Valentina Gomez Moreno',     'Cajera',                   7000.00, '2024-01-10', 'Matutino'),
  ('Raul Eduardo Medina Garcia',       'Cajero',                   7000.00, '2023-08-15', 'Vespertino');

-- Poblar tabla clientes
INSERT INTO clientes (telefono, nombre, correo, direccion) VALUES
  ('9613456780','Miguel Angel Torres Lopez'     , 'miguel.torres@gmail.com',       'Calle Olivo No. 202'),
  ('9614567890','Sofia Isabel Hernandez Vargas' , 'sofia.hernandez@outlook.com',   'Av. Insurgentes 345'),
  ('9615678901','Diego Andres Martinez Rivera'  , 'diego.martinez@gmail.com',      'Calle Lago No. 78'),
  ('9616789012','Lucia Fernanda Ramos Ortiz'    , 'lucia.ramos@outlook.com',       'Av. Reforma 100'),
  ('9617890123','Fernando Jose Cruz Sanchez'    , 'fernando.cruz@gmail.com',       'Calle Juárez 50'),
  ('9618901234','Karina Sofia Lopez Martinez'   , 'karina.lopez@outlook.com',      'Av. Universidad 120'),
  ('9619012345','Javier Alejandro Sanchez Perez', 'javier.sanchez@gmail.com',      'Calle Hidalgo 215'),
  ('9610123456','Maria Fernanda Ruiz Gonzalez'  , 'maria.fernanda@outlook.com',    'Av. Central 89'),
  ('9617898524','Carlos Manuel Diaz Hernandez'  , 'carlos@outlook.com',            'Av Central No° 123'),
  ('9612463791','Ana Patricia Ruiz Lopez'       , 'anita_ruiz@gmail.com',          'Calle Central No° 456'),
  ('999'       ,'Cliente General'               , 'general_client15@gmail.com',    'Calle tamarindos No° 325');

-- Poblar tabla proveedores
INSERT INTO proveedores (nombre, telefono, contacto, rfc) VALUES
  ('Proveedor Bebidas Energeticas',    '5551234003', 'contacto_energeticas@gmail.com', 'BEBE780101ABC'),
  ('Proveedor Jugos Jumex',            '5551234004', 'jumex.contacto@outlook.com',       'JUMX810202DEF'),
  ('Proveedor Pan Bimbo',              '5551234005', 'bimbo_info@gmail.com',             'PABI830303GHI'),
  ('Proveedor Cervezas Modelo',        '5551234006', 'modelo.cervezas@outlook.com',     'CEMO850404JKL'),
  ('Proveedor Cigarrera',              '5551234007', 'cigarrera_contacto@gmail.com',     'CIGA860505MNO'),
  ('Proveedor Embutidos El Rey',       '5551234008', 'embutidos.rey@outlook.com',        'EMRE870606PQR'),
  ('Proveedor Lacteos Alpura',         '5551234009', 'alpura.sales@gmail.com',           'LALA880707STU'),
  ('Proveedor Snacks del Valle',       '5551234010', 'snacks.valle@outlook.com',         'SVAL890808VWX'),
  ('Proveedor Sabritas',               '5551234001', 'sabritas@gmail.com',               'SABR900909YZA'),
  ('Proveedor Refrescos',              '5551234002', 'variedades_refrescos@gmail.com',   'REFR911010BCD');

-- Poblar tabla categorias
INSERT INTO categorias (nombre, id_proveedor) VALUES
  ('Sabritas', 9),
  ('jugos',    2),
  ('refrescos',10),
  ('Dulces'   ,8),  
  ('Lacteos'  ,7), 
  ('Panaderia',3), 
  ('Cafe'     ,7);

-- Poblar tabla articulos
INSERT INTO articulos (
  nombre, codigo_barras, descripcion, precio_venta, stock,
  precio_unitario_proveedor, id_categoria, fecha_caducidad
) VALUES
  ('sabritones',                    '7501011149205', 'sabritones sabor chile y limon',                           15, 150, 12, 1, '2025-12-08'),
  ('Coca-Cola',                     '7501055310227', 'Coca-Cola de 2.5 litros',                                  42, 200, 38, 3, '2025-10-03'),
  ('Bida Fresa',                    '7501013191219', 'Jugar sabor a fresa',                                      15, 259, 12, 2, '2025-06-24'),
  ('Jugo de manzana',               '7501013122190', 'Jugo jumex sabor manzana',                                 25, 142, 21, 2, '2025-07-16'),
  ('Boing de mango',                '7501039400449', 'Boing sabor mango, el mejor de todos',                     17, 200, 15, 2, '2025-05-29'),
  ('Rancheritos',                   '7500478001620', 'Rancheritos muy good con salsa',                           15, 200, 12, 1, '2025-09-03'),
  ('Sabrita Crujiente Jalapeno',    '7501011145719', 'Aque no puedes comer sola una',                            17, 254, 14, 1, '2025-09-03'),
  ('pepsi',                         '7501031311606', 'Refresco de 2 litros',                                     32, 364, 29, 3, '2025-05-27'),
  ('Fanta naranja',                 '7501055303779', 'Refresco de 600 ml superior a la Coca-Cola',               29, 500, 25, 3, '2025-07-07'),
  ('Big-Cola',                      '7507531596482', 'Refresco muy good para matar el gusto de una coquita fria',35, 554, 30, 3, '2025-06-10'),
  ('Leche Lala Entera 1L',          '7501003100597', 'Leche Lala entera en envase de 1 litro',                   28, 100, 22, 5, '2025-11-15'),
  ('Pan Bimbo Familiar',            '7500625339062', 'Pan de caja blanco Bimbo paquete familiar 680g',           35, 80,  27, 6, '2025-08-10'),
  ('Gansito Marinela',              '7501004657021', 'Pastelito Gansito Marinela con relleno de fresa',          12, 150, 9,  1, '2025-09-05'),
  ('Agua Bonafont 600 ml',          '7501055013678', 'Botella de agua purificada Bonafont 600 ml',               12, 300, 8,  2, '2026-01-20'),
  ('Cheetos Crunchy 165g',          '7501072605516', 'Cheetos sabor queso bolsa 165 gramos',                     22, 200, 16, 1, '2025-10-30'),
  ('Mentos Menta Peg bag 50g',      '7500435130105', 'Caramelos Mentos sabor menta bolsa de 50 gramos',          8,  250, 5,  4, '2026-02-28'),
  ('Cafe Instantaneo Nescafe 200g', '7500435053030', 'Café soluble Nescafé Clásico en frasco de 200g',           75, 60,  55, 7, '2026-03-15'),
  ('Jugo Del Valle Multifrutas 1L', '7501017545849', 'Jugo Del Valle multifrutas en envase de 1 litro',          30, 120, 24, 2, '2025-12-01'),
  ('Sabritas Saladas 170g',         '7501000337103', 'Papas Sabritas saladas bolsa de 170 gramos',               20, 180, 14, 1, '2025-11-25'),
  ('Yoghurt Yoplait Fresa 150g',    '7501050362013', 'Yoghurt bebible Yoplait sabor fresa 150 gramos',           14, 90,  10, 5, '2025-09-12');
