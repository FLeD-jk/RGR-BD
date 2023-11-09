import psycopg2


class Model:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname='RGR',
            user='postgres',
            password='1111',
            host='localhost',
            port=5432
        )
        self.create_table_Category()
        self.create_table_SubCategory()
        self.create_table_Brand()
        self.create_table_Product()
        self.create_table_SubCategory_Brand()

    def create_table_Category(self):
        c = self.conn.cursor()
        c.execute('''
             CREATE TABLE IF NOT EXISTS "Category" (
            "Category_id" integer NOT NULL,
            "Name" character varying(30) NOT NULL,
            CONSTRAINT "Category_pkey" PRIMARY KEY ("Category_id"),
            CONSTRAINT name_un UNIQUE ("Name")
        )
        ''')

        # Check if the table exists
        c.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'Category')")
        table_exists = c.fetchone()[0]

        if not table_exists:
            # Table does not exist, so create it
            c.execute('''
                 CREATE TABLE  "Category" (
            "Category_id" integer NOT NULL,
            "Name" character varying(30) NOT NULL,
            CONSTRAINT "Category_pkey" PRIMARY KEY ("Category_id"),
            CONSTRAINT name_un UNIQUE ("Name")
        )
            ''')

        self.conn.commit()

    def create_table_SubCategory(self):
        c = self.conn.cursor()
        c.execute('''
             CREATE TABLE IF NOT EXISTS "SubCategory" (
            "SubCategory_id" integer NOT NULL,
            "Name" character varying(30) NOT NULL,
            "Category_id" integer NOT NULL,
            CONSTRAINT "SubCategory_pkey" PRIMARY KEY ("SubCategory_id"),
            CONSTRAINT name_un2 UNIQUE ("Name"),
            CONSTRAINT "Category_FK" FOREIGN KEY ("Category_id") REFERENCES public."Category" ("Category_id") MATCH SIMPLE
        )
        ''')

        # Check if the table exists
        c.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'SubCategory')")
        table_exists = c.fetchone()[0]

        if not table_exists:
            # Table does not exist, so create it
            c.execute('''
                 CREATE TABLE "SubCategory" (
            "SubCategory_id" integer NOT NULL,
            "Name" character varying(30) NOT NULL,
            "Category_id" integer NOT NULL,
            CONSTRAINT "SubCategory_pkey" PRIMARY KEY ("SubCategory_id"),
            CONSTRAINT name_un2 UNIQUE ("Name"),
            CONSTRAINT "Category_FK" FOREIGN KEY ("Category_id") REFERENCES public."Category" ("Category_id") MATCH SIMPLE
        )
        ''')

        self.conn.commit()

    def create_table_Brand(self):
        c = self.conn.cursor()
        c.execute('''
             CREATE TABLE IF NOT EXISTS "Brand" (
            "Brand_id" integer NOT NULL,
            "Name" character varying(30)  NOT NULL,
            CONSTRAINT "Brand_pkey" PRIMARY KEY ("Brand_id"),
            CONSTRAINT name_un3 UNIQUE ("Name")
        )
        ''')

        # Check if the table exists
        c.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'Brand')")
        table_exists = c.fetchone()[0]

        if not table_exists:
            # Table does not exist, so create it
            c.execute('''
                 CREATE TABLE "Brand" (
            "Brand_id" integer NOT NULL,
            "Name" character varying(30)  NOT NULL,
            CONSTRAINT "Brand_pkey" PRIMARY KEY ("Brand_id"),
            CONSTRAINT name_un3 UNIQUE ("Name")
        )
        ''')

        self.conn.commit()

    def create_table_Product(self):
        c = self.conn.cursor()
        c.execute('''
             CREATE TABLE IF NOT EXISTS "Product" (
            "Product_id" integer NOT NULL,
            "Name" character varying(30) NOT NULL,
            "Color" character varying(30)  NOT NULL,
            "Width" integer NOT NULL,
            "Height" integer NOT NULL,
            "Deepth" integer NOT NULL,
            "Weight" integer NOT NULL,
            "Energy consumption" integer NOT NULL,
            "Brand_id" integer NOT NULL,
            CONSTRAINT "Product_pkey" PRIMARY KEY ("Product_id"),
            CONSTRAINT "Brand_FK" FOREIGN KEY ("Brand_id") REFERENCES public."Brand" ("Brand_id") MATCH SIMPLE
        )
        ''')

        # Check if the table exists
        c.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'Product')")
        table_exists = c.fetchone()[0]

        if not table_exists:
            # Table does not exist, so create it
            c.execute('''
                 CREATE TABLE  "Product" (
            "Product_id" integer NOT NULL,
            "Name" character varying(30) NOT NULL,
            "Color" character varying(30)  NOT NULL,
            "Width" integer NOT NULL,
            "Height" integer NOT NULL,
            "Deepth" integer NOT NULL,
            "Weight" integer NOT NULL,
            "Energy consumption" integer NOT NULL,
            "Brand_id" integer NOT NULL,
            CONSTRAINT "Product_pkey" PRIMARY KEY ("Product_id"),
            CONSTRAINT "Brand_FK" FOREIGN KEY ("Brand_id") REFERENCES public."Brand" ("Brand_id") MATCH SIMPLE
        )
        ''')

        self.conn.commit()

    def create_table_SubCategory_Brand(self):
        c = self.conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS "SubCategory_Brand" (
            "SubCategory_id" integer NOT NULL,
            "Brand_id" integer NOT NULL,
            CONSTRAINT "SubCategory_Brand_pkey" PRIMARY KEY ("SubCategory_id", "Brand_id"),
            CONSTRAINT "Brand_FK" FOREIGN KEY ("Brand_id") REFERENCES public."Brand" ("Brand_id") MATCH SIMPLE,
            CONSTRAINT "SubCategory_FK" FOREIGN KEY ("SubCategory_id") REFERENCES public."SubCategory" ("SubCategory_id") MATCH SIMPLE
        )
        ''')

        # Check if the table exists
        c.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'SubCategory_Brand')")
        table_exists = c.fetchone()[0]

        if not table_exists:
            # Table does not exist, so create it
            c.execute('''
                 CREATE TABLE "SubCategory_Brand" (
            "SubCategory_id" integer NOT NULL,
            "Brand_id" integer NOT NULL,
            CONSTRAINT "SubCategory_Brand_pkey" PRIMARY KEY ("SubCategory_id", "Brand_id"),
            CONSTRAINT "Brand_FK" FOREIGN KEY ("Brand_id") REFERENCES public."Brand" ("Brand_id") MATCH SIMPLE,
            CONSTRAINT "SubCategory_FK" FOREIGN KEY ("SubCategory_id") REFERENCES public."SubCategory" ("SubCategory_id") MATCH SIMPLE
        )
        ''')

        self.conn.commit()
    def add_Category(self, Category_id, Name):
        c = self.conn.cursor()
        try:
            c.execute('INSERT INTO "Category" ("Category_id", "Name") VALUES (%s, %s)', (Category_id, Name))
            self.conn.commit()
            return "Category added successfully!"
        except psycopg2.IntegrityError as e:
            self.conn.rollback()
            error_message = str(e)
            return "Error: " + error_message
        finally:
            c.close()

    def get_all_Category(self):
        c = self.conn.cursor()
        c.execute('SELECT * FROM "Category"')
        return c.fetchall()

    def update_Category(self, Category_id, Name):
        c = self.conn.cursor()
        try:
            c.execute('UPDATE "Category" SET "Name"=%s WHERE "Category_id"=%s', (Name, Category_id))
            self.conn.commit()
            return "Category update successfully!"
        except psycopg2.IntegrityError as e:
            self.conn.rollback()
            error_message = str(e)
            return "Error: " + error_message
        finally:
            c.close()

    def delete_Category(self, Category_id):
        c = self.conn.cursor()
        try:
            c.execute('DELETE FROM "Category" WHERE "Category_id"=%s', (Category_id,))
            self.conn.commit()
            return "Category delete successfully!"
        except psycopg2.IntegrityError as e:
            self.conn.rollback()
            error_message = str(e)
            return "Error: " + error_message
        finally:
            c.close()

    def add_SubCategory(self, SubCategory_id, Name,Category_id):
        c = self.conn.cursor()
        try:
            c.execute('INSERT INTO "SubCategory" ("SubCategory_id", "Name","Category_id") VALUES (%s, %s,%s)', ( SubCategory_id, Name,Category_id))
            self.conn.commit()
            return "SubCategory added successfully!"
        except psycopg2.IntegrityError as e:
            self.conn.rollback()
            error_message = str(e)
            return "Error: " + error_message
        finally:
            c.close()


    def get_all_SubCategory(self):
        c = self.conn.cursor()
        c.execute('SELECT * FROM "SubCategory"')
        return c.fetchall()

    def update_SubCategory(self,  SubCategory_id, Name,Category_id):
        c = self.conn.cursor()
        try:
            c.execute('UPDATE "SubCategory" SET "Name"=%s, "Category_id"=%s WHERE "SubCategory_id"=%s', (Name, Category_id, SubCategory_id))
            self.conn.commit()
            return "SubCategory update successfully!"
        except psycopg2.IntegrityError as e:
            self.conn.rollback()
            error_message = str(e)
            return "Error: " + error_message
        finally:
            c.close()

    def delete_SubCategory(self, SubCategory_id):
        c = self.conn.cursor()
        try:
            c.execute('DELETE FROM "SubCategory" WHERE "SubCategory_id"=%s', (SubCategory_id,))
            self.conn.commit()
            return "SubCategory delete successfully!"
        except psycopg2.IntegrityError as e:
            self.conn.rollback()
            error_message = str(e)
            return "Error: " + error_message
        finally:
            c.close()

    def add_Brand(self, Brand_id, Name):
        c = self.conn.cursor()
        try:
            c.execute('INSERT INTO "Brand" ("Brand_id", "Name") VALUES (%s, %s)', (Brand_id, Name))
            self.conn.commit()
            return "Product added successfully!"
        except psycopg2.IntegrityError as e:
            self.conn.rollback()
            error_message = str(e)
            return "Error: " + error_message
        finally:
            c.close()

    def get_all_Brand(self):
        c = self.conn.cursor()
        c.execute('SELECT * FROM "Brand"')
        return c.fetchall()

    def update_Brand(self, Brand_id, Name):
        c = self.conn.cursor()
        try:
            c.execute('UPDATE "Brand" SET "Name"=%s WHERE "Brand_id"=%s', (Name, Brand_id))
            self.conn.commit()
            return "Brand update successfully!"
        except psycopg2.IntegrityError as e:
            self.conn.rollback()
            error_message = str(e)
            return "Error: " + error_message
        finally:
            c.close()

    def delete_Brand(self, Brand_id):
        c = self.conn.cursor()
        try:
            c.execute('DELETE FROM "Brand" WHERE "Brand_id"=%s', (Brand_id,))
            self.conn.commit()
            return "Brand delete successfully!"
        except psycopg2.IntegrityError as e:
            self.conn.rollback()
            error_message = str(e)
            return "Error: " + error_message
        finally:
            c.close()

    def add_Product(self, Product_id, Name, Color, Width, Height, Deepth,  Weight, Energy_consumption, Brand_id):
        c = self.conn.cursor()
        try:
            c.execute('INSERT INTO "Product" ("Product_id", "Name", "Color", "Width", "Height", "Deepth",  "Weight", "Energy consumption", "Brand_id") VALUES (%s, %s,%s, %s,%s, %s,%s, %s,%s)', (Product_id, Name, Color, Width, Height, Deepth,  Weight, Energy_consumption, Brand_id))
            self.conn.commit()
            return "Product added successfully!"
        except psycopg2.IntegrityError as e:
            self.conn.rollback()
            error_message = str(e)
            return "Error: " + error_message
        finally:
            c.close()

    def get_all_Product(self):
        c = self.conn.cursor()
        c.execute('SELECT * FROM "Product"')
        return c.fetchall()

    def update_Product(self, Product_id, Name, Color, Width, Height, Deepth,  Weight, Energy_consumption, Brand_id):
        c = self.conn.cursor()
        try:
            c.execute('UPDATE "Product" SET "Name"=%s, "Color"=%s, "Width"=%s, "Height"=%s, "Deepth"=%s,  "Weight"=%s, "Energy consumption"=%s, "Brand_id"=%s WHERE "Product_id"=%s', ( Name, Color, Width, Height, Deepth,  Weight, Energy_consumption, Brand_id,Product_id))
            self.conn.commit()
            return "Product update successfully!"
        except psycopg2.IntegrityError as e:
            self.conn.rollback()
            error_message = str(e)
            return "Error: " + error_message
        finally:
            c.close()

    def delete_Product(self, Product_id):
        c = self.conn.cursor()
        try:
            c.execute('DELETE FROM "Product" WHERE "Product_id"=%s', (Product_id,))
            self.conn.commit()
            return "Product delete successfully!"
        except psycopg2.IntegrityError as e:
            self.conn.rollback()
            error_message = str(e)
            return "Error: " + error_message
        finally:
            c.close()
    def generate_category(self, number):
        c = self.conn.cursor()
        c.execute(
            '''
            DO $$
            DECLARE
                subcategory_id  INT;
            BEGIN
                FOR subcategory_id  IN 1..%s
                LOOP
                    INSERT INTO public."Category" ("Category_id", "Name") 
                    VALUES (
                          nextval('public.category_id'),
                          'Category' || currval('public.category_id')
                     )
                     ON CONFLICT ("Name") DO NOTHING;
                END LOOP;
            END $$;
            ''',
            (number,)
        )
        self.conn.commit()

    def generate_subcategory(self, number):
        c = self.conn.cursor()
        c.execute(
            '''
            DO $$
            DECLARE
                subcategory_id INT;
            BEGIN
                FOR subcategory_id IN 1..%s
                LOOP
                    INSERT INTO public."SubCategory" ("SubCategory_id", "Name", "Category_id")
                    VALUES (
                        nextval('public.subcategory_id'), 
                        'SubCategory' || currval('public.subcategory_id'), 
                        (SELECT "Category_id" FROM public."Category" ORDER BY random() LIMIT 1)
                    );
                END LOOP;
            END $$;
            ''',
            (number,)
        )

        self.conn.commit()

    def generate_brand(self, number):
        c = self.conn.cursor()
        c.execute(
            '''
            DO $$
            DECLARE
                brand_id  INT;
            BEGIN
                FOR brand_id  IN 1..%s
                LOOP
                    INSERT INTO public."Brand" ("Brand_id", "Name") 
                    VALUES (
                          nextval('public.brand_id'),
                          'Brand' || currval('public.brand_id')
                     )
                     ON CONFLICT ("Name") DO NOTHING;
                END LOOP;
            END $$;
            ''',
            (number,)
        )
        self.conn.commit()

    def generate_product(self, number):
        c = self.conn.cursor()
        c.execute(
            '''
            DO $$
            DECLARE
                product_id INT;
            BEGIN
                FOR product_id IN 1..%s
                LOOP
                    INSERT INTO public."Product" ("Product_id", "Name", "Color", "Width", "Height", "Deepth", "Weight", "Energy consumption", "Brand_id")
                    VALUES (
                      nextval('public.product_id'),  
                      'Product' || currval('public.product_id'), 
                        CASE WHEN random() < 0.2 THEN 'Red'
                             WHEN random() < 0.4 THEN 'Blue'
                             WHEN random() < 0.6 THEN 'Green'
                             WHEN random() < 0.8 THEN 'Yellow'
                             ELSE 'Purple' END,
                        (random() * 100 + 1)::integer,
                        (random() * 100 + 1)::integer,
                        (random() * 100 + 1)::integer,
                        (random() * 100 + 1)::integer,
                        (random() * 100 + 1)::integer,
                        (SELECT "Brand_id" FROM public."Brand" ORDER BY random() LIMIT 1)
                    );
                END LOOP;
            END $$;
            ''',
            (number,)
        )
        self.conn.commit()

    def generate_subcategory_brand(self, number):
        c = self.conn.cursor()
        c.execute(
            'INSERT INTO public."SubCategory_Brand" ("SubCategory_id", "Brand_id") SELECT sc."SubCategory_id", b."Brand_id" FROM public."SubCategory" sc CROSS JOIN public."Brand" b LIMIT %s;',
            (number,))

        self.conn.commit()

    def reset(self):
        c = self.conn.cursor()
        c.execute('DELETE FROM public."SubCategory_Brand"; DELETE FROM public."Product"; DELETE FROM public."Brand";   DELETE FROM public."SubCategory"; DELETE FROM public."Category";SELECT setval(\'category_id\', 0); SELECT setval(\'subcategory_id\', 0);SELECT setval(\'brand_id\', 0);SELECT setval(\'product_id\', 0);')
        self.conn.commit()

    def search_request1(self):
        c = self.conn.cursor()
        c.execute('SELECT b."Name" AS "Brand", p."Name" AS "Product", p."Energy consumption", p."Weight" FROM "public"."Product" p JOIN "public"."Brand" b ON p."Brand_id" = b."Brand_id" WHERE p."Energy consumption" < 20 AND p."Weight" < 30 ORDER BY b."Name";')
        self.conn.commit()

        return c.fetchall(), c.description

    def search_request2(self):
        c = self.conn.cursor()
        c.execute('SELECT s."Name" AS "SubCategoryName", b."Name" AS "BrandName", p."Name" AS "ProductName",p."Width" AS "ProductWidth",p."Height" AS "ProductHeight" FROM "public"."SubCategory" s JOIN "public"."SubCategory_Brand" sb ON s."SubCategory_id" = sb."SubCategory_id" JOIN "public"."Brand" b ON sb."Brand_id" = b."Brand_id" JOIN "public"."Product" p ON b."Brand_id" = p."Brand_id" WHERE p."Width" = (SELECT MAX("Width") FROM "public"."Product") AND p."Height" = (SELECT MAX("Height") FROM "public"."Product");')
        self.conn.commit()

        return c.fetchall(), c.description

    def search_request3(self):
        c = self.conn.cursor()
        c.execute('SELECT c."Name" AS "Category_Name", sc."Name" AS "SubCategory_Name", b."Name" AS "Brand_Name", p."Name" AS "Product_Name" FROM "public"."Category" AS c INNER JOIN "public"."SubCategory" AS sc ON c."Category_id" = sc."Category_id" INNER JOIN "public"."SubCategory_Brand" AS scb ON SC."SubCategory_id" = scb."SubCategory_id" INNER JOIN "public"."Brand" AS b ON scb."Brand_id" = b."Brand_id" INNER JOIN "public"."Product" AS p ON b."Brand_id" = p."Brand_id" WHERE p."Color" = \'Yellow\';')
        self.conn.commit()

        return c.fetchall(), c.description