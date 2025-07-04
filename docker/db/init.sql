-- Creates the DB if its not made already

CREATE DATABASE IF NOT EXISTS bettertire;
USE bettertire;

-- makes all the tables 

CREATE TABLE Manufacturers (
    ManufacturerID INT AUTO_INCREMENT PRIMARY KEY,
    ManufacturerName VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE Products (
    ProductID INT AUTO_INCREMENT PRIMARY KEY,
    ProductNumber VARCHAR(50) NOT NULL UNIQUE,
    ProductName VARCHAR(255) NOT NULL,
    ManufacturerID INT,
    Size VARCHAR(20),
    Description TEXT,
    UnitPrice DECIMAL(10, 2),
    FOREIGN KEY (ManufacturerID) REFERENCES Manufacturers(ManufacturerID)
);

CREATE TABLE Customers (
    CustomerID INT AUTO_INCREMENT PRIMARY KEY,
    CustomerVendorNumber VARCHAR(255) UNIQUE,
    CustomerVendorName VARCHAR(255) NOT NULL,
    Address VARCHAR(255),
    City VARCHAR(100),
    State VARCHAR(50),
    ZipCode VARCHAR(20),
    PhoneNumber VARCHAR(20),
    Email VARCHAR(255)
);

CREATE TABLE Users (
    UserID INT AUTO_INCREMENT PRIMARY KEY,
    UserName VARCHAR(50) NOT NULL UNIQUE,
    FirstName VARCHAR(100),
    LastName VARCHAR(100)
);

CREATE TABLE Transactions (
    TransactionID INT AUTO_INCREMENT PRIMARY KEY,
    TransactionDateTime DATETIME NOT NULL,
    TransactionType ENUM('INVC', 'PMT', 'CR') NOT NULL,
    ReferenceNumber VARCHAR(255),
    CustomerID INT,
    ReceivingPONumber VARCHAR(255),
    CreatedByUserID INT,
    CreatedDateTime DATETIME,
    LastChangedByUserID INT,
    LastChangedDateTime DATETIME,
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID),
    FOREIGN KEY (CreatedByUserID) REFERENCES Users(UserID),
    FOREIGN KEY (LastChangedByUserID) REFERENCES Users(UserID)
);

CREATE TABLE Transaction_Details (
    TransactionDetailID INT AUTO_INCREMENT PRIMARY KEY,
    TransactionID INT NOT NULL,
    ProductID INT NOT NULL,
    Quantity INT NOT NULL,
    Price DECIMAL(10, 2) NOT NULL,
    Cost DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (TransactionID) REFERENCES Transactions(TransactionID),
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
);

-- ======================================================================
-- Inserting some data into the tables 
-- ======================================================================

INSERT INTO Manufacturers (ManufacturerName) VALUES
('Goodyear'), ('Michelin'), ('Bridgestone');

INSERT INTO Products (ProductNumber, ProductName, ManufacturerID, Size, UnitPrice) VALUES
('GY-G399', 'Goodyear G399 LHS Fuel Max', 1, '11R22.5', 550.00),
('GY-G572', 'Goodyear G572 LHD Fuel Max', 1, '11R22.5', 575.00),
('GY-ENDUR', 'Goodyear Endurance RSA', 1, '11R22.5', 560.00),
('MICH-XLINE', 'Michelin X Line Energy Z', 2, '11R22.5', 610.00),
('MICH-XDN2', 'Michelin XDN2', 2, '11R22.5', 630.00),
('MICH-XZA3', 'Michelin XZA3+', 2, '11R22.5', 620.00),
('BRIDGE-R284', 'Bridgestone R284 Ecopia', 3, '11R22.5', 580.00),
('BRIDGE-M726', 'Bridgestone M726 ELA', 3, '11R22.5', 595.00),
('BRIDGE-R268', 'Bridgestone R268 Ecopia', 3, '11R22.5', 585.00),
('GY-ARMOR', 'Goodyear Armor Max Pro', 1, '11R22.5', 590.00);

INSERT INTO Users (UserName, FirstName, LastName) VALUES
('U651RHY', 'Robert', 'Hyland'),
('U651JTW', 'Jessica', 'Williams'),
('U651CTW', 'Charles', 'Taylor');

INSERT INTO Customers (CustomerVendorNumber, CustomerVendorName, City, State) VALUES
('2857604', 'SOUTHERN INDIANA SCALE CO', 'New Albany', 'IN'),
('2855395', 'RIVER METALS REC LOU STL', 'Louisville', 'KY'),
('1001', 'GEORGE E. FERN COMPANY', 'Louisville', 'KY'),
('1002', 'DAVIS H. ELLIOT CO., INC.', 'Lexington', 'KY');

INSERT INTO Transactions (TransactionDateTime, TransactionType, ReferenceNumber, CustomerID, CreatedByUserID, CreatedDateTime, LastChangedByUserID, LastChangedDateTime) VALUES
('2023-04-21 13:52:33', 'INVC', '3700007001', 1, 1, '2023-04-21 13:52:33', 1, '2023-04-21 13:52:33'),
('2023-03-14 15:49:05', 'INVC', '3700007002', 2, 3, '2023-02-17 12:39:54', 3, '2023-03-14 15:49:05'),
('2023-05-10 10:15:00', 'INVC', '3700007003', 3, 2, '2023-05-10 10:15:00', 2, '2023-05-10 10:15:00');

INSERT INTO Transaction_Details (TransactionID, ProductID, Quantity, Price, Cost) VALUES
(1, 4, 4, 615.00, 520.00),
(1, 5, 4, 635.00, 540.00);


INSERT INTO Transaction_Details (TransactionID, ProductID, Quantity, Price, Cost) VALUES
(2, 1, 8, 550.00, 480.00);


INSERT INTO Transaction_Details (TransactionID, ProductID, Quantity, Price, Cost) VALUES
(3, 8, 2, 595.00, 510.00),
(3, 9, 2, 585.00, 505.00);