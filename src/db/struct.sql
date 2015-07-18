-- FORCE FOREIGN KEY USE
-- view: https://www.sqlite.org/pragma.html#pragma_foreign_keys
PRAGMA foreign_keys = ON;

-- TABLES

CREATE TABLE file ( 			       -- registers analyzed files
  id_file INTEGER PRIMARY KEY,	 -- file unique id
  fname TEXT,					           -- file name
  fpath TEXT					           -- file path
);

CREATE TABLE symbol_type (		   -- describes the type of each symbol
  id_type INTEGER PRIMARY KEY,	 -- type unique id
  type TEXT 					           -- type description
);

CREATE TABLE symbol (            -- describes common symbol attributes
  id_symbol INTEGER PRIMARY KEY, -- symbol unique id
  id_file INTEGER,				       -- file id in which symbol is defined
  id_type INTEGER,				       -- type id of the symbol
  ini_line INTEGER,				       -- initialization line
  end_line INTEGER,				       -- last line of symbol definition
  use_line TEXT, 				         -- lines where symbol is used
  -- symbol existence bound with file existence:
  FOREIGN KEY (id_file) REFERENCES file(id_file) ON DELETE CASCADE
);

CREATE TABLE import (             -- describes import specific attributes
  id_symbol INTEGER PRIMARY KEY,  -- symbol unique id
  module TEXT,                    -- import module
  element TEXT,                   -- import elements (can be express as an array using '|' as delimiters)
  alias TEXT,                     -- alias name use to describe a module
  -- import existence bound with symbol existence:
  FOREIGN KEY (id_symbol) REFERENCES symbol(id_symbol) ON DELETE CASCADE
);

CREATE TABLE variable (           -- describes global variable specific attributes
  id_symbol INTEGER PRIMARY KEY,  -- symbol unique id
  name TEXT,                      -- variable name
  -- variable existence bound with symbol existence:
  FOREIGN KEY (id_symbol) REFERENCES symbol(id_symbol) ON DELETE CASCADE
);

CREATE TABLE function (           -- describes function specific attributes
  id_symbol INTEGER PRIMARY KEY,  -- symbol unique id
  name TEXT,                      -- function name
  args TEXT,                      -- function arguments (can be express as an array using '|' as delimiters)
  -- function existence bound with symbol existence:
  FOREIGN KEY (id_symbol) REFERENCES symbol(id_symbol) ON DELETE CASCADE
);

CREATE TABLE class (              -- describes class specific attributes
  id_symbol INTEGER PRIMARY KEY,  -- symbol unique id
  name TEXT,                      -- class name
  legacy TEXT,                    -- legacy (can be express as an array using '|' as delimiters)
  -- import class bound with symbol existence:
  FOREIGN KEY (id_symbol) REFERENCES symbol(id_symbol) ON DELETE CASCADE
);

CREATE TABLE docstring (          -- describes docstring specific attributes
  id_symbol INTEGER PRIMARY KEY,  -- symbol unique id
  context TEXT,                   -- symbol in which the docstring is defined
  -- import docstring bound with symbol existence:
  FOREIGN KEY (id_symbol) REFERENCES symbol(id_symbol) ON DELETE CASCADE
);

CREATE TABLE method (             -- describes method specific attributes
  id_symbol INTEGER PRIMARY KEY,  -- symbol unique id
  id_class INTEGER,               -- class in which the method is defined
  name TEXT,                      -- method name
  args TEXT,                      -- method arguments
  -- method existence bound with symbol existence:
  FOREIGN KEY (id_symbol) REFERENCES symbol(id_symbol) ON DELETE CASCADE
  -- method existence bound with class existence:
  FOREIGN KEY (id_class) REFERENCES class(id_symbol) ON DELETE CASCADE
);

CREATE TABLE class_attr (         -- describes class attribute specific attributes
  id_symbol INTEGER PRIMARY KEY,  -- symbol unique id
  id_class INTEGER,               -- id of class bound to the attribute
  name TEXT,                      -- attribute name
  -- class attribute existence bound with symbol existence:
  FOREIGN KEY (id_symbol) REFERENCES symbol(id_symbol) ON DELETE CASCADE
  -- class attribute existence bound with class existence:
  FOREIGN KEY (id_class) REFERENCES class(id_symbol) ON DELETE CASCADE
);

CREATE TABLE tmp_index (  -- temporary table used to register the current process symbol
  id_symbol INTEGER       -- symbol unique id
);

-- INSERT
-- FILLS xxx_type table with constant value --

INSERT INTO symbol_type VALUES(10, 'import');
INSERT INTO symbol_type VALUES(11, 'global variable');
INSERT INTO symbol_type VALUES(12, 'oneline function');
INSERT INTO symbol_type VALUES(13, 'multiline function');
INSERT INTO symbol_type VALUES(14, 'class declaration');

INSERT INTO symbol_type VALUES(20, 'oneline public method');
INSERT INTO symbol_type VALUES(21, 'oneline private method');
INSERT INTO symbol_type VALUES(22, 'oneline constructor method');
INSERT INTO symbol_type VALUES(23, 'multiline public method');
INSERT INTO symbol_type VALUES(24, 'multiline private method');
INSERT INTO symbol_type VALUES(25, 'multiline constructor method');

INSERT INTO symbol_type VALUES(30, 'class attribute');

INSERT INTO symbol_type VALUES(40, 'oneline docstring');
INSERT INTO symbol_type VALUES(41, 'multiline docstring');


-- TRIGGER --
-- Triggers are used for preserving the data integretity and automate
--  process like linking mechanisme beetween the symbol table and
--  each sub-symbol table.

CREATE TRIGGER trg_insert_symbol_import AFTER INSERT ON symbol
WHEN new.id_type = 10
BEGIN
  INSERT INTO import (id_symbol) VALUES (new.id_symbol);
  INSERT INTO tmp_index (id_symbol) VALUES (new.id_symbol);
END;

CREATE TRIGGER trg_insert_symbol_variable AFTER INSERT ON symbol
WHEN new.id_type = 11
BEGIN
  INSERT INTO variable (id_symbol) VALUES (new.id_symbol);
  INSERT INTO tmp_index (id_symbol) VALUES (new.id_symbol);
END;

CREATE TRIGGER trg_insert_symbol_function AFTER INSERT ON symbol
WHEN new.id_type = 12 OR new.id_type = 13
BEGIN
  INSERT INTO function (id_symbol) VALUES (new.id_symbol);
  INSERT INTO tmp_index (id_symbol) VALUES (new.id_symbol);
END;

CREATE TRIGGER trg_insert_symbol_class AFTER INSERT ON symbol
WHEN new.id_type = 14
BEGIN
  INSERT INTO class (id_symbol) VALUES (new.id_symbol);
  INSERT INTO tmp_index (id_symbol) VALUES (new.id_symbol);
END;

CREATE TRIGGER trg_insert_symbol_docstring AFTER INSERT ON symbol
WHEN new.id_type = 40 OR new.id_type = 41
BEGIN
  INSERT INTO docstring (id_symbol) VALUES (new.id_symbol);
  INSERT INTO tmp_index (id_symbol) VALUES (new.id_symbol);
END;

CREATE TRIGGER trg_insert_symbol_class_attr AFTER INSERT ON symbol
WHEN new.id_type = 30
BEGIN
  INSERT INTO class_attr (id_symbol) VALUES (new.id_symbol);
  INSERT INTO tmp_index (id_symbol) VALUES (new.id_symbol);
END;

CREATE TRIGGER trg_insert_symbol_method AFTER INSERT ON symbol
WHEN new.id_type >= 20 AND new.id_type < 30
BEGIN
  INSERT INTO method (id_symbol) VALUES (new.id_symbol);
  INSERT INTO tmp_index (id_symbol) VALUES (new.id_symbol);
END;

CREATE TRIGGER trg_insert_tmp_index BEFORE INSERT ON tmp_index
BEGIN
  DELETE FROM tmp_index;
END;
