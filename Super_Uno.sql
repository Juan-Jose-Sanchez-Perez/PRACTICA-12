-- Crear la base de datos
CREATE DATABASE Super_Uno;
USE Super_Uno;

-- Tabla de proveedores
CREATE TABLE Proveedores (
    id_proveedor INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    telefono VARCHAR(20) UNIQUE NOT NULL,
    contacto VARCHAR(100)
);

-- Tabla de categorías con referencia al proveedor
CREATE TABLE Categorias (
    id_categoria INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    id_proveedor INT NOT NULL,
    FOREIGN KEY (id_proveedor) REFERENCES Proveedores(id_proveedor) ON DELETE CASCADE
);

-- Tabla de artículos con referencia a la categoría
CREATE TABLE Articulos (
    id_articulo INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    precio DECIMAL(10,2) NOT NULL CHECK (precio >= 0),
    stock INT NOT NULL CHECK (stock >= 0),
    id_categoria INT NOT NULL,
    fecha_caducidad DATE,
    FOREIGN KEY (id_categoria) REFERENCES Categorias(id_categoria) ON DELETE CASCADE
);

-- Tabla de clientes (Usando teléfono como clave primaria)
CREATE TABLE Clientes (
    telefono VARCHAR(15) PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(100) UNIQUE,
    direccion TEXT,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de empleados
CREATE TABLE Empleados (
    id_empleado INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    puesto VARCHAR(50) NOT NULL,
    salario DECIMAL(10,2) NOT NULL CHECK (salario >= 0),
    fecha_contratacion DATE NOT NULL,
    turno ENUM('Matutino', 'Vespertino', 'Nocturno') NOT NULL
);

-- Tabla de ventas
CREATE TABLE Ventas (
    id_venta INT AUTO_INCREMENT PRIMARY KEY,
    telefono_cliente VARCHAR(15),
    id_empleado INT,
    fecha_venta TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total DECIMAL(10,2) NOT NULL CHECK (total >= 0),
    FOREIGN KEY (telefono_cliente) REFERENCES Clientes(telefono) ON DELETE SET NULL,
    FOREIGN KEY (id_empleado) REFERENCES Empleados(id_empleado) ON DELETE SET NULL
);

-- Tabla de detalles de ventas
CREATE TABLE Detalles_Venta (
    id_detalle INT AUTO_INCREMENT PRIMARY KEY,
    id_venta INT NOT NULL,
    id_articulo INT NOT NULL,
    cantidad INT NOT NULL CHECK (cantidad > 0),
    subtotal DECIMAL(10,2) NOT NULL CHECK (subtotal >= 0),
    FOREIGN KEY (id_venta) REFERENCES Ventas(id_venta) ON DELETE CASCADE,
    FOREIGN KEY (id_articulo) REFERENCES Articulos(id_articulo) ON DELETE CASCADE
);

-- Tabla de compras (reabastecimiento de inventario)
CREATE TABLE Compras (
    id_compra INT AUTO_INCREMENT PRIMARY KEY,
    id_proveedor INT NOT NULL,
    id_empleado INT,
    fecha_compra TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total DECIMAL(10,2) NOT NULL CHECK (total >= 0),
    FOREIGN KEY (id_proveedor) REFERENCES Proveedores(id_proveedor),
    FOREIGN KEY (id_empleado) REFERENCES Empleados(id_empleado)
);

-- Detalles de cada compra
CREATE TABLE Detalles_Compra (
    id_detalle_compra INT AUTO_INCREMENT PRIMARY KEY,
    id_compra INT NOT NULL,
    id_articulo INT NOT NULL,
    cantidad INT NOT NULL CHECK (cantidad > 0),
    costo_unitario DECIMAL(10,2) NOT NULL CHECK (costo_unitario >= 0),
    subtotal DECIMAL(10,2) NOT NULL CHECK (subtotal >= 0),
    FOREIGN KEY (id_compra) REFERENCES Compras(id_compra) ON DELETE CASCADE,
    FOREIGN KEY (id_articulo) REFERENCES Articulos(id_articulo) ON DELETE CASCADE
);

-- TRIGGERS PARA MANEJAR STOCK AUTOMÁTICAMENTE

-- Aumentar stock al hacer una compra
DELIMITER //
CREATE TRIGGER trg_aumentar_stock AFTER INSERT ON Detalles_Compra
FOR EACH ROW
BEGIN
    UPDATE Articulos
    SET stock = stock + NEW.cantidad
    WHERE id_articulo = NEW.id_articulo;
END;
//
DELIMITER ;

-- Disminuir stock al hacer una venta
DELIMITER //
CREATE TRIGGER trg_disminuir_stock AFTER INSERT ON Detalles_Venta
FOR EACH ROW
BEGIN
    UPDATE Articulos
    SET stock = stock - NEW.cantidad
    WHERE id_articulo = NEW.id_articulo;
END;
//
DELIMITER ;
