-- Poblar tabla empleados
INSERT INTO empleados (nombre, puesto, salario, fecha_contratacion, turno) VALUES
  ('Alejandro Daniel Pérez Gómez',    'Bodeguero',               7500.00, '2022-05-15', 'Matutino'),
  ('María Fernanda Castillo Ramírez',  'Gerente de Ventas',       8500.00, '2023-07-10', 'Vespertino'),
  ('Carlos Alberto Rivera Mendoza',    'Personal de Limpieza',    7200.00, '2024-11-01', 'Nocturno'),
  ('Ana Sofía Morales Herrera',        'Auxiliar de Ventas',       7800.00, '2025-02-28', 'Matutino'),
  ('Sergio Alejandro Torres Díaz',     'Supervisor de Stock',      8300.00, '2022-12-01', 'Vespertino'),
  ('Patricia Isabel Gómez Sánchez',    'Atención al Cliente',      8000.00, '2023-03-20', 'Matutino'),
  ('Roberto Manuel Díaz López',        'Encargado de Almacén',     8200.00, '2024-06-30', 'Vespertino'),
  ('Verónica Elizabeth Solís Cruz',    'Asistente Administrativo', 7100.00, '2025-04-10', 'Nocturno'),
  ('Lucía Valentina Gómez Moreno',     'Cajera',                   7000.00, '2024-01-10', 'Matutino'),
  ('Raúl Eduardo Medina García',       'Cajero',                   7000.00, '2023-08-15', 'Vespertino');

-- Poblar tabla clientes
INSERT INTO clientes (telefono, nombre, correo, direccion) VALUES
  ('9613456780','Miguel Ángel Torres López',       'miguel.torres@gmail.com',       'Calle Olivo No. 202'),
  ('9614567890','Sofía Isabel Hernández Vargas',  'sofia.hernandez@outlook.com',   'Av. Insurgentes 345'),
  ('9615678901','Diego Andrés Martínez Rivera',   'diego.martinez@gmail.com',      'Calle Lago No. 78'),
  ('9616789012','Lucía Fernanda Ramos Ortiz',     'lucia.ramos@outlook.com',       'Av. Reforma 100'),
  ('9617890123','Fernando José Cruz Sánchez',     'fernando.cruz@gmail.com',       'Calle Juárez 50'),
  ('9618901234','Karina Sofía López Martínez',    'karina.lopez@outlook.com',      'Av. Universidad 120'),
  ('9619012345','Javier Alejandro Sánchez Pérez', 'javier.sanchez@gmail.com',      'Calle Hidalgo 215'),
  ('9610123456','María Fernanda Ruiz González',   'maria.fernanda@outlook.com',    'Av. Central 89'),
  ('9617898524','Carlos Manuel Díaz Hernández',   'carlos@outlook.com',            'Av Central No° 123'),
  ('9612463791','Ana Patricia Ruiz López',        'anita_ruiz@gmail.com',          'Calle Central No° 456');

-- Poblar tabla proveedores
INSERT INTO proveedores (nombre, telefono, contacto, rfc) VALUES
  ('Proveedor Bebidas Energéticas',    '5551234003', 'contacto_energeticas@gmail.com', 'BEBE780101ABC'),
  ('Proveedor Jugos Jumex',            '5551234004', 'jumex.contacto@outlook.com',       'JUMX810202DEF'),
  ('Proveedor Pan Bimbo',              '5551234005', 'bimbo_info@gmail.com',             'PABI830303GHI'),
  ('Proveedor Cervezas Modelo',        '5551234006', 'modelo.cervezas@outlook.com',     'CEMO850404JKL'),
  ('Proveedor Cigarrera',              '5551234007', 'cigarrera_contacto@gmail.com',     'CIGA860505MNO'),
  ('Proveedor Embutidos El Rey',       '5551234008', 'embutidos.rey@outlook.com',        'EMRE870606PQR'),
  ('Proveedor Lácteos Alpura',         '5551234009', 'alpura.sales@gmail.com',           'LALA880707STU'),
  ('Proveedor Snacks del Valle',       '5551234010', 'snacks.valle@outlook.com',         'SVAL890808VWX'),
  ('Proveedor Sabritas',               '5551234001', 'sabritas@gmail.com',               'SABR900909YZA'),
  ('Proveedor Refrescos',              '5551234002', 'variedades_refrescos@gmail.com',   'REFR911010BCD');

-- Poblar tabla categorias
INSERT INTO categorias (nombre, id_proveedor) VALUES
  ('Sabritas', 9),
  ('jugos',    2),
  ('refrescos',10);

-- Poblar tabla articulos
INSERT INTO articulos (
  nombre, codigo_barras, descripcion, precio_venta, stock,
  precio_unitario_proveedor, id_categoria, fecha_caducidad
) VALUES
  ('sabritones',                '7501011149205', 'sabritones sabor chile y limon',                   15, 1, 12, 1, '2025-12-08'),
  ('Coca-Cola',                 '7501055310227', 'Coca-Cola de 2.5 litros',                          42, 1, 38, 3, '2025-10-03'),
  ('Bida Fresa',                '7501013191219', 'Jugar sabor a fresa',                              15, 1, 12, 2, '2025-06-24'),
  ('Jugo de manzana',           '7501013122190', 'Jugo jumex sabor manzana',                         25, 1, 21, 2, '2025-07-16'),
  ('Boing de mango',            '7501017351284', 'Boing sabor mango, el mejor de todos',             17, 1, 15, 2, '2025-05-29'),
  ('Rancheritos',               '7500478001620', 'Rancheritos muy good con salsa',                   15, 1, 12, 1, '2025-09-03'),
  ('Sabrita Crujiente Jalapeño','7501011145719', 'Aque no puedes comer sola una',                     17, 1, 14, 1, '2025-09-03'),
  ('pepsi',                     '7501047826493', 'Refresco de 2 litros',                             32, 1, 29, 3, '2025-05-27'),
  ('Big-Cola',                  '7501025487632', 'Refresco de 3 litros superior a la Coca-Cola',     29, 1, 25, 3, '2025-07-07');
