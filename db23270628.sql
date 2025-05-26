CREATE DATABASE IF NOT EXISTS super_uno
  /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */
  /*!80016 DEFAULT ENCRYPTION='N' */;
USE super_uno;

-- Proveedores
DROP TABLE IF EXISTS proveedores;
CREATE TABLE proveedores (
  id_proveedor INT NOT NULL AUTO_INCREMENT,
  nombre VARCHAR(100) NOT NULL,
  rfc VARCHAR(13) NOT NULL,
  telefono VARCHAR(20) NOT NULL,
  contacto VARCHAR(100),
  PRIMARY KEY (id_proveedor),
  UNIQUE KEY telefono_unico (telefono),
  UNIQUE KEY rfc_unico (rfc)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Categorias
DROP TABLE IF EXISTS categorias;
CREATE TABLE categorias (
  id_categoria INT NOT NULL AUTO_INCREMENT,
  nombre VARCHAR(100) NOT NULL,
  id_proveedor INT NOT NULL,
  PRIMARY KEY (id_categoria),
  KEY fk_categorias_proveedores (id_proveedor),
  CONSTRAINT fk_categorias_proveedores FOREIGN KEY (id_proveedor)
    REFERENCES proveedores(id_proveedor) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Articulos
DROP TABLE IF EXISTS articulos;
CREATE TABLE articulos (
  id_articulo INT NOT NULL AUTO_INCREMENT,
  nombre VARCHAR(100) NOT NULL,
  codigo_barras VARCHAR(14) NOT NULL,
  descripcion TEXT,
  precio_venta DECIMAL(10,2) NOT NULL,
  stock INT NOT NULL,
  precio_unitario_proveedor DECIMAL(10,2) NOT NULL DEFAULT '0.00',
  id_categoria INT NOT NULL,
  fecha_caducidad DATE,
  PRIMARY KEY (id_articulo),
  UNIQUE KEY idx_codigo_barras (codigo_barras),
  KEY fk_articulos_categorias (id_categoria),
  CONSTRAINT fk_articulos_categorias FOREIGN KEY (id_categoria)
    REFERENCES categorias(id_categoria) ON DELETE CASCADE,
  CONSTRAINT chk_stock_nonneg CHECK (stock >= 0),
  CONSTRAINT chk_precio_venta_nonneg CHECK (precio_venta >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Clientes
DROP TABLE IF EXISTS clientes;
CREATE TABLE clientes (
  telefono VARCHAR(15) NOT NULL,
  nombre VARCHAR(100) NOT NULL,
  correo VARCHAR(100),
  direccion TEXT,
  fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (telefono),
  UNIQUE KEY correo_unico (correo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Empleados
DROP TABLE IF EXISTS empleados;
CREATE TABLE empleados (
  id_empleado INT NOT NULL AUTO_INCREMENT,
  nombre VARCHAR(100) NOT NULL,
  puesto VARCHAR(50) NOT NULL,
  salario DECIMAL(10,2) NOT NULL,
  fecha_contratacion DATE NOT NULL,
  turno ENUM('Matutino','Vespertino','Nocturno') NOT NULL,
  PRIMARY KEY (id_empleado),
  CONSTRAINT chk_salario_nonneg CHECK (salario >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Ventas
DROP TABLE IF EXISTS ventas;
CREATE TABLE ventas (
  id_venta INT NOT NULL AUTO_INCREMENT,
  telefono_cliente VARCHAR(15),
  id_empleado INT,
  fecha_venta TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  total DECIMAL(10,2) NOT NULL,
  PRIMARY KEY (id_venta),
  KEY fk_ventas_clientes (telefono_cliente),
  KEY fk_ventas_empleados (id_empleado),
  CONSTRAINT fk_ventas_clientes FOREIGN KEY (telefono_cliente)
    REFERENCES clientes(telefono) ON DELETE SET NULL,
  CONSTRAINT fk_ventas_empleados FOREIGN KEY (id_empleado)
    REFERENCES empleados(id_empleado) ON DELETE SET NULL,
  CONSTRAINT chk_total_venta_nonneg CHECK (total >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Detalles_Venta
DROP TABLE IF EXISTS detalles_venta;
CREATE TABLE detalles_venta (
  id_detalle INT NOT NULL AUTO_INCREMENT,
  id_venta INT NOT NULL,
  id_articulo INT NOT NULL,
  cantidad INT NOT NULL,
  subtotal DECIMAL(10,2) NOT NULL,
  PRIMARY KEY (id_detalle),
  KEY fk_detallesventa_ventas (id_venta),
  KEY fk_detallesventa_articulos (id_articulo),
  CONSTRAINT fk_detallesventa_ventas FOREIGN KEY (id_venta)
    REFERENCES ventas(id_venta) ON DELETE CASCADE,
  CONSTRAINT fk_detallesventa_articulos FOREIGN KEY (id_articulo)
    REFERENCES articulos(id_articulo) ON DELETE CASCADE,
  CONSTRAINT chk_cantidad_venta CHECK (cantidad > 0),
  CONSTRAINT chk_subtotal_venta_nonneg CHECK (subtotal >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Compras
DROP TABLE IF EXISTS compras;
CREATE TABLE compras (
  id_compra INT NOT NULL AUTO_INCREMENT,
  id_proveedor INT NOT NULL,
  id_empleado INT,
  fecha_compra TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  total DECIMAL(10,2) NOT NULL,
  PRIMARY KEY (id_compra),
  KEY fk_compras_proveedores (id_proveedor),
  KEY fk_compras_empleados (id_empleado),
  CONSTRAINT fk_compras_proveedores FOREIGN KEY (id_proveedor)
    REFERENCES proveedores(id_proveedor),
  CONSTRAINT fk_compras_empleados FOREIGN KEY (id_empleado)
    REFERENCES empleados(id_empleado),
  CONSTRAINT chk_total_compra_nonneg CHECK (total >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Detalles_Compra
DROP TABLE IF EXISTS detalles_compra;
CREATE TABLE detalles_compra (
  id_detalle_compra INT NOT NULL AUTO_INCREMENT,
  id_compra INT NOT NULL,
  id_articulo INT NOT NULL,
  cantidad INT NOT NULL,
  costo_unitario DECIMAL(10,2) NOT NULL,
  subtotal DECIMAL(10,2) NOT NULL,
  PRIMARY KEY (id_detalle_compra),
  KEY fk_detallescompra_compras (id_compra),
  KEY fk_detallescompra_articulos (id_articulo),
  CONSTRAINT fk_detallescompra_compras FOREIGN KEY (id_compra)
    REFERENCES compras(id_compra) ON DELETE CASCADE,
  CONSTRAINT fk_detallescompra_articulos FOREIGN KEY (id_articulo)
    REFERENCES articulos(id_articulo) ON DELETE CASCADE,
  CONSTRAINT chk_cantidad_compra CHECK (cantidad > 0),
  CONSTRAINT chk_subtotal_compra_nonneg CHECK (subtotal >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- TRIGGERS PARA AJUSTAR STOCK
DELIMITER //
CREATE TRIGGER trg_aumentar_stock AFTER INSERT ON detalles_compra
FOR EACH ROW
BEGIN
  UPDATE articulos
  SET stock = stock + NEW.cantidad
  WHERE id_articulo = NEW.id_articulo;
END;
//
CREATE TRIGGER trg_disminuir_stock AFTER INSERT ON detalles_venta
FOR EACH ROW
BEGIN
  UPDATE articulos
  SET stock = stock - NEW.cantidad
  WHERE id_articulo = NEW.id_articulo;
END;
//
DELIMITER ;