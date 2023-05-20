#Changes to be made from testing
#1. Testing of all functions of bookmarks,reviews,orders is remaining

from typing import Optional
from typing import Callable
import pymysql
import datetime

from swagger_server.models import BookmarkRequest,Bookmarks,Categories
from swagger_server.models import Companies,CompanyRequest,ContractorRequest
from swagger_server.models import Contractors,Customers,Locations,OrderRequest
from swagger_server.models import Orders,Products, RegisterResponseInfo,RegisterResponse
from swagger_server.models import ReviewRequest,Reviews,UserLogin,UserRegister,VerifyEmail

connection = pymysql.connect(host='localhost',
                             user='newusr',
                             password='password',
                             database='tba',
                             cursorclass=pymysql.cursors.DictCursor)

def setup():

    with connection.cursor() as cursor:

        cursor.execute(""" CREATE TABLE IF NOT EXISTS `customers`(
        `cus_uid` INT(6) NOT NULL AUTO_INCREMENT,        
        `name`  VARCHAR(255) NOT NULL,      
        `email` VARCHAR(255) NOT NULL UNIQUE,
        `password` VARCHAR(255) NOT NULL,
        `phone_no` VARCHAR(255) DEFAULT NULL,
        `otp` VARCHAR(255) DEFAULT NULL,
        PRIMARY KEY (`cus_uid`)
        )""")

        cursor.execute(""" CREATE TABLE IF NOT EXISTS `companies`(
        `company_id` INT(6) NOT NULL AUTO_INCREMENT,
        `name` VARCHAR(255) NOT NULL UNIQUE,
        `company_img_url` VARCHAR(2000) DEFAULT NULL,
        `about_us` VARCHAR(5000) DEFAULT NULL,
        `website_link` VARCHAR(255) DEFAULT NULL,
        PRIMARY KEY (`company_id`)
        )""")


        cursor.execute("""CREATE TABLE IF NOT EXISTS `locations`(
        `id` INT(6) NOT NULL AUTO_INCREMENT,
        `name` VARCHAR(255) NOT NULL,
        PRIMARY KEY(`id`)
        )""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS `categories`(
        `id` INT(6) NOT NULL AUTO_INCREMENT,
        `name` VARCHAR(255) NOT NULL,
        PRIMARY KEY(`id`)
        )""")

        cursor.execute(""" CREATE TABLE IF NOT EXISTS `contractors`(
        `contractor_id` INT(6) NOT NULL AUTO_INCREMENT,
        `name` VARCHAR(255) NOT NULL,
        `email` VARCHAR(255) NOT NULL UNIQUE,
        `address` VARCHAR(5000) DEFAULT NULL,
        `phone_no` VARCHAR(255) DEFAULT NULL,
        `company_id` INT(6) NOT NULL,
        PRIMARY KEY (`contractor_id`),
        FOREIGN KEY (`company_id`) REFERENCES `companies` (`company_id`)
        )""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS `products`(
        `p_uid` INT(6) NOT NULL AUTO_INCREMENT,
        `location_id` INT(6) NOT NULL,
        `category_id` INT(6) NOT NULL,
        `product_img_url` VARCHAR(2000) DEFAULT NULL, 
        `product_description` VARCHAR(5000) DEFAULT NULL,
        `contractor_id` INT(6) NOT NULL,
        PRIMARY KEY (`p_uid`),
        FOREIGN KEY (`location_id`) REFERENCES `locations` (`id`),
        FOREIGN KEY (`category_id`) REFERENCES `categories` (`id`),
        FOREIGN KEY (`contractor_id`) REFERENCES `contractors` (`contractor_id`)        
        )""")

        cursor.execute(""" CREATE TABLE IF NOT EXISTS `orders`(
        `id` INT(6) NOT NULL AUTO_INCREMENT,
        `cus_uid` INT(6) NOT NULL,
        `p_uid` INT(6) NOT NULL,
        `order_date_time` VARCHAR(255) DEFAULT NULL,
        `message` VARCHAR(5000) DEFAULT NULL,
        PRIMARY KEY (`id`),
        FOREIGN KEY (`cus_uid`) REFERENCES `customers` (`cus_uid`),
        FOREIGN KEY (`p_uid`) REFERENCES `products` (`p_uid`)
        )""")

        cursor.execute(""" CREATE TABLE IF NOT EXISTS `bookmarks`(
        `id` INT(6) NOT NULL AUTO_INCREMENT,
        `cus_uid` INT(6) NOT NULL,
        `p_uid` INT(6) NOT NULL,
        PRIMARY KEY(`id`),
        FOREIGN KEY (`cus_uid`) REFERENCES `customers` (cus_uid),
        FOREIGN KEY (`p_uid`) REFERENCES `products` (`p_uid`)
        )""")

        cursor.execute(""" CREATE TABLE IF NOT EXISTS `reviews`(
        `id` INT(6) NOT NULL AUTO_INCREMENT,
        `cus_uid` INT(6) NOT NULL,
        `p_uid` INT(6) NOT NULL,
        `review` VARCHAR(5000) DEFAULT NULL,
        PRIMARY KEY (`id`),
        FOREIGN KEY (`cus_uid`) REFERENCES `customers` (`cus_uid`),
        FOREIGN KEY (`p_uid`) REFERENCES `products` (`p_uid`)
        )""")


#CUSTOMERS
def getpassword_fromemail(emailid : str) -> str:
    """fetch password from users database by email_id , return None if not there"""
    sql = """SELECT `password` from `customers` WHERE `email`=%s"""
    with connection.cursor() as cursor:
        cursor.execute(sql,(emailid))
        r = cursor.fetchone()
        if (r):
            password = r['password']
            return password      
        return None
    
def getcusid_fromemail(emailid : str) -> str:
    """fetch cus_id from users database by email id, return None if not there"""
    sql = """SELECT `cus_uid` from `customers` WHERE `email`=%s"""
    with connection.cursor() as cursor:
        cursor.execute(sql,(emailid))
        r = cursor.fetchone()
        if (r):
            cusid = r['cus_uid']
            return cusid
        return None
    
def getusername_fromemail(emailid:str) ->str:
    """fetch"""
    sql = """SELECT `name` from `customers` WHERE `email`=%s"""
    with connection.cursor() as cursor:
        cursor.execute(sql,(emailid))
        r = cursor.fetchone()
        if (r):
            username = r
            return username 
        return None
    
def add_customer(customer : Customers) -> None:
    with connection.cursor() as cursor:
        cusid = getcusid_fromemail(customer.emailid)
        if (cusid is not None):
           raise NameError 
        query = "INSERT INTO customers (name,email,password,phone_no) VALUES (%s, %s, %s, %s)"
        values = (customer.name,customer.emailid, customer.password, customer.phone_number)
        cursor.execute(query, values)
        connection.commit()
        customer.cus_id=str(cursor.lastrowid)


def addotp(otp:str,email : str) -> None:
    """adds otp to cutomer with given email"""
    with connection.cursor() as cursor:
        sql = """UPDATE `customers` SET `otp`=%s WHERE `email`=%s"""
        cursor.execute(sql, (otp, email))
    connection.commit()


def getotp_frommail(email : str) -> str :
    with connection.cursor() as cursor:
        sql ="""SELECT `otp` FROM `customers` WHERE `email`=%s"""
        cursor.execute(sql,(email))
        result = cursor.fetchone()
        if (not result):
            return None
        otp = result["otp"]
        return otp
    
def check_customer_exists(cusid:str)->None:
    with connection.cursor() as cursor:
        cursor.execute("""SELECT * FROM `customers` WHERE `cus_uid`=%s""",cusid)
        r=cursor.fetchone()
        if (not r):
            raise NameError


def get_customer_by_id(cusid:str) ->Optional[Customers]:
    with connection.cursor() as cursor:
        cursor.execute("""SELECT * FROM `customers` WHERE `cus_uid`=%s""",cusid)
        element=cursor.fetchone()
        if (not element):
            raise NameError
        customer=Customers(cus_id=element['cus_uid'],name=element['name'],emailid=element['email'],
                            phone_number=element['phone_no'],password=element['password'])
        return customer
        
        
def get_all_customers() -> list[Customers]:
    cm=[]
    with connection.cursor() as cursor:
        cursor.execute("""SELECT * FROM `customers`""")
        result=cursor.fetchall()
        for element in result:
            customer=Customers(cus_id=element['cus_uid'],name=element['name'],emailid=element['email'],
                               phone_number=element['phone_no'],password=element['password'])
            cm.append(customer)
    return cm
    
#COMPANIES
#company name is assumed to be unique to every company
def getcompanyid_fromcompany(company:str)->str:
    with connection.cursor() as cursor:
        cursor.execute("""SELECT `company_id` FROM `companies` WHERE `name`=%s""",company)
        r=cursor.fetchone()
        if (r):
            companyid=r['company_id']
            return companyid
        ##print("Empty string is returned from companyid_fromcompany")
        return ""
    
def getcompanyname_fromcompanyid(companyid:str)->str:
    with connection.cursor() as cursor:
        cursor.execute("""SELECT `name` FROM `companies` WHERE `company_id`=%s""",companyid)
        r=cursor.fetchone()
        if (r):
            name=r['name']
            return name
        ##print("Empty string is returned from companyname_fromcompanyid")
        return ""
        
def getcompanyimgurl_fromcompanyid(companyid:str)->str:
    with connection.cursor() as cursor:
        cursor.execute("""SELECT `company_img_url` FROM `companies` WHERE `company_id`=%s""",companyid)
        r=cursor.fetchone()
        if (r):
            company_img_url=r['company_img_url']
            return company_img_url
        ##print("Empty string is returned from companyimgurl_fromcompanyid")
        return ""
    
def check_company_exists(companyid:str)->None:
    ##print("This is debugging of check_company_exists")
    with connection.cursor() as cursor:
        cursor.execute("""SELECT * FROM `companies` WHERE `company_id` = %s""",companyid)
        ##print("query executed for check_company_exists function")
        r=cursor.fetchone()
        ##print("this is r:",r)
        if (not r):
            raise NameError
        
def add_companies(company:Companies)->None:
    with connection.cursor() as cursor:
        companyid=getcompanyid_fromcompany(company.name)
        if(companyid != ""):
            raise NameError
        query="""INSERT INTO companies(name,company_img_url,about_us,website_link) VALUES (%s,%s,%s,%s)"""
        values=(company.name,company.company_img_url,company.about_us,company.website_link)
        cursor.execute(query,values)
        connection.commit()
        company.company_id=str(cursor.lastrowid)

def get_all_companies() ->list[Companies]:
    cp=[]
    with connection.cursor() as cursor:
        cursor.execute("""SELECT * FROM `companies`""")
        results=cursor.fetchall()
        for element in results:
            company=Companies(company_id=element['company_id'],name=element['name'],company_img_url=element['company_img_url'],
                              about_us=element['about_us'],website_link=element['website_link'])
            cp.append(company)
    return cp

def get_company_by_id(companyid:str)->Optional[Companies]:
    ##print("Debugging for get_company_by_id function")
    with connection.cursor() as cursor:
        cursor.execute("""SELECT * FROM `companies` WHERE `company_id`=%s""",companyid)
        ##print("query executed for get_company_by_id function")
        r=cursor.fetchone()
        ##print("type:",r)
        ##print("this is r:",r)
        if (not r):
            raise NameError
        company=Companies(company_id=r['company_id'],name=r['name'],company_img_url=r['company_img_url'],
                          about_us=r['about_us'],website_link=r['website_link'])
        ##print("type:",type(company))
        ##print("this is company:",company)
        return company
        

#CONTRACTORS
#contractor email-id is assumed to be unique for every contractor
def getcontractorid_fromcontractoremail(contractoremail:str)->str:
    with connection.cursor() as cursor:
        cursor.execute("""SELECT `contractor_id` FROM `contractors` WHERE `email`=%s""",contractoremail)
        r=cursor.fetchone()
        if (r):
            contractor_id=r['contractor_id']
            return contractor_id
        ##print("Empty string is returned from getcontractor_fromcontractoremail")
        return ""
    
def getcompanyid_fromcontractorid(contractorid:str)->str:
    with connection.cursor() as cursor:
        cursor.execute("""SELECT `company_id` FROM `contractors` WHERE `contractor_id`=%s""",contractorid)
        r=cursor.fetchone()
        if (r):
            companyid=r['company_id']
            return companyid
        ##print("getcontractor_fromcontractorid is not returning anything")
        return ""

def add_contractors(contractor:Contractors) -> None:
    with connection.cursor() as cursor:
        contractorid=getcontractorid_fromcontractoremail(contractor.email)
        if(contractorid != ""):
            raise NameError
        query="""INSERT INTO contractors(name,email,address,phone_no,company_id) VALUES (%s,%s,%s,%s,%s)"""
        values=(contractor.name,contractor.email,contractor.address,contractor.phone_no,contractor.company_id)
        cursor.execute(query,values)
        connection.commit()
        contractor.contractor_id=str(cursor.lastrowid)

def check_contractor_exists(contractorid:str)->None:
    ##print("Debugging for check_contractor_exists function")
    with connection.cursor() as cursor:
        cursor.execute("""SELECT * FROM `contractors` WHERE `contractor_id`=%s""",contractorid)
        ##print("query executed for check_contractor_exists function")
        r=cursor.fetchone()
        ##print("this is r:",r)
        if (not r):
            raise NameError
        

def get_all_contractors() -> list[Contractors]:

    cr=[]
    with connection.cursor() as cursor:
        cursor.execute("""SELECT * FROM `contractors`""")
        results=cursor.fetchall()
        for element in results:
            contractor=Contractors(contractor_id=element['contractor_id'], name=element['name'],email=element['email'],
                                   address=element['address'],phone_no=element['phone_no'],company_id=element['company_id'])
            cr.append(contractor)
    return cr

def get_contractor_by_id(contractorid:str)->Optional[Contractors]:
    ##print("Debugging for getcontractor_by_id function")
    with connection.cursor() as cursor:
        cursor.execute("""SELECT * FROM `contractors` WHERE `contractor_id`=%s""",contractorid)
        ##print("query executed for get_contractor_by_id function")
        r=cursor.fetchone()
        ##print("type:",type(r))
        ##print("this is r:",r)
        if (not r):
            raise NameError
        contractor=Contractors(contractor_id=r['contractor_id'],name=r['name'],email=r['email'],
                               address=r['address'],phone_no=r['phone_no'],company_id=r['company_id']) 
        ##print("type:",type(contractor))  
        ##print("this is contractor:",contractor)    
        return contractor

#BOOKMARKS
def add_bookmarks(bookmark:BookmarkRequest) -> None:
    with connection.cursor() as cursor:
        query="""INSERT INTO bookmarks (cus_uid,p_uid) VALUES (%s,%s)"""
        values=(bookmark.cus_uid,bookmark.p_uid)
        cursor.execute(query,values)
        connection.commit()
        bookmark.id=str(cursor.lastrowid)

def getbookmarks_fromcusid(cusid:str)->list[Bookmarks]:
    bk=[]
    with connection.cursor() as cursor:
        cursor.execute("""SELECT * FROM `bookmarks` WHERE `cus_uid`=%s""",cusid)
        results=cursor.fetchall()
        for element in results:
            product=getproduct_frompuid(element['p_uid'])
            bookmark=Bookmarks(id=element['id'],cus_uid=element['cus_uid'],product=product)
            bk.append(bookmark)
    return bk

def getbookmark_fromid(queryid:str,bookmarkid:str)->Optional[Bookmarks]:
    with connection.cursor() as cursor:
        cursor.execute("""SELECT * FROM `bookmarks` WHERE `id`=%s""",bookmarkid)
        element=cursor.fetchone()
        if (not element):
            raise NameError
        product=getproduct_frompuid(element['p_uid'])
        bookmark=Bookmarks(id=element['id'],cus_uid=element['cus_uid'],product=product)    
        return bookmark

def deletebookmark_fromid(queryid:str,bookmarkid:str)->None:
    with connection.cursor() as cursor:
        cursor.execute("""DELETE FROM `bookmarks` WHERE `id`=%s""",bookmarkid)
        connection.commit()

#LOCATIONS

def getlocationid_fromlocation(location:str)->str:
    with connection.cursor() as cursor:
        cursor.execute("""SELECT `id` FROM `locations` WHERE `name`=%s""",location)
        r=cursor.fetchone()
        if (r):
            locationid=r['id']
            return locationid
        ##print("Empty string is returned from getlocationid_fromlocation")
        return ""
    
def getlocation_fromlocationid(locationid:str)->str:
    with connection.cursor() as cursor:
        cursor.execute("""SELECT * FROM `locations` WHERE `id`=%s""",locationid)
        r=cursor.fetchone()
        if (r):
            location=r['name']
            return location
        ##print("Empty string is returned from getlocation_fromlocationid")
        return ""

def add_locations(location:Locations) -> None:
    with connection.cursor() as cursor:
        locationid=getlocationid_fromlocation(location.name)
        if (locationid != ""):
            return
        query="INSERT INTO locations(name) VALUES (%s)"
        values=(location.name)
        cursor.execute(query,values)
        connection.commit()
        location.id=str(cursor.lastrowid)

def get_all_locations() -> list[Locations]:

    lc=[]
    with connection.cursor() as cursor:
        cursor.execute("""SELECT * FROM `locations`""")
        results=cursor.fetchall()
        for element in results:
            location=Locations(id=element['id'],name=element['name'])
            lc.append(location)
    return lc

#CATEGORIES

def getcategoryid_fromcategory(category:str)->str:
    with connection.cursor() as cursor:
        cursor.execute("""SELECT `id` FROM `categories` WHERE `name`=%s""",category)
        r=cursor.fetchone()
        if (r):
            categoryid=r['id']
            return categoryid
        ##print("Empty string is returned from getcategoryid_fromcategory")
        return ""
    
def getcategory_fromcategoryid(categoryid:str)->str:
    with connection.cursor() as cursor:
        cursor.execute("""SELECT `name` FROM `categories` WHERE `id`=%s""",categoryid)
        r=cursor.fetchone()
        if (r):
            category=r['name']
            return category
        ##print("Empty string is returned from getcategory_fromcategoryid")
        return ""

def add_categories(category:Categories) -> None:
     with connection.cursor() as cursor:
        categoryid=getcategoryid_fromcategory(category.name)
        if (categoryid != ""):
            return
        query="INSERT INTO categories(name) VALUES (%s)"
        values=(category.name)
        cursor.execute(query,values)
        connection.commit()
        category.id=str(cursor.lastrowid)

def get_all_categories() -> list[Categories]:
    cg=[]
    with connection.cursor() as cursor:
        cursor.execute("""SELECT * FROM categories""")
        results=cursor.fetchall()
        for element in results:
            category=Categories(id=element['id'],name=element['name'])
            cg.append(category)
    return cg    

#PRODUCTS     

def getpuid_fromcontractorid(contractor_id:str)->str:
    with connection.cursor() as cursor:
        cursor.execute("""SELECT `p_uid` FROM `products` WHERE `contractor_id`=%s""",contractor_id)
        r=cursor.fetchone()
        if (r):
            puid=r['p_uid']
            return puid
        ##print("Empty string is returned from getpuid_fromcontractorid")
        return ""
    
def getcontractorid_frompuid(puid:str)->str:
    with connection.cursor() as cursor:
        cursor.execute("""SELECT `contractor_id` FROM `products` WHERE `p_uid`=%s""",puid)
        element=cursor.fetchone()
        if (element):
            contractorid=element['contractor_id']
            return contractorid
        ##print("Empty string is returned from getcontractorid_frompuid")
        return ""
    
def getproductimgurl_frompuid(puid:str)->str:
    with connection.cursor() as cursor:
        cursor.execute("""SELECT `product_img_url` FROM `products` WHERE `p_uid`=%s""",puid)
        element=cursor.fetchone()
        if (element):
            productimgurl=element['product_img_url']
            return productimgurl
        ##print("Empty string is returned from getproductimgurl_frompuid")
        return ""
    
            
def add_products(product:Products) -> None:
    with connection.cursor() as cursor:
        puid=getpuid_fromcontractorid(product.contractor_id)
        if(puid != ""):
            raise NameError
        locationid=getlocationid_fromlocation(product.location)
        categoryid=getcategoryid_fromcategory(product.category)
        query = "INSERT INTO products (location_id,category_id,product_img_url,product_description,contractor_id) VALUES (%s,%s,%s,%s,%s)"
        values = (locationid,categoryid,product.product_img_url,product.product_description,product.contractor_id)
        cursor.execute(query,values)
        connection.commit()
        product.p_uid=str(cursor.lastrowid)

def check_product_exists(puid:str)->None:
    with connection.cursor() as cursor:
        cursor.execute("""SELECT * FROM `products` WHERE `p_uid`=%s""",puid)
        r=cursor.fetchone()
        if (not r):
            raise NameError
        
def get_all_products()->list[Products]:
    pr=[]
    with connection.cursor() as cursor:
        cursor.execute("""SELECT * FROM `products`""")
        results=cursor.fetchall()
        for element in results:
            location=getlocation_fromlocationid(element['location_id'])
            category=getcategory_fromcategoryid(element['category_id'])
            companyid=getcompanyid_fromcontractorid(element['contractor_id'])
            company_img_url=getcompanyimgurl_fromcompanyid(companyid)
            company_name=getcompanyname_fromcompanyid(companyid)
            contractor=get_contractor_by_id(element['contractor_id']) #get object Contractor from contractorid
            product=Products(p_uid=element['p_uid'],location=location,category=category,
                             product_img_url=element['product_img_url'],product_description=element['product_description'],
                             company_name=company_name,company_id=companyid,company_img_url=company_img_url,contractor_id=element['contractor_id'],
                             contractor_name=contractor.name)
            pr.append(product)
    return pr
               
def getproduct_frompuid(puid:str)->Optional[Products]:

    with connection.cursor() as cursor:
        cursor.execute("""SELECT * FROM `products` WHERE `p_uid`=%s""",puid)
        element=cursor.fetchone()
        if (not element):
            raise NameError
        
        location=getlocation_fromlocationid(element['location_id'])
        category=getcategory_fromcategoryid(element['category_id'])
        companyid=getcompanyid_fromcontractorid(element['contractor_id'])
        company_img_url=getcompanyimgurl_fromcompanyid(companyid)
        company_name=getcompanyname_fromcompanyid(companyid)
        contractor=get_contractor_by_id(element['contractor_id'])
        product=Products(p_uid=element['p_uid'],location=location,category=category,
                            product_img_url=element['product_img_url'],product_description=element['product_description'],
                            company_name=company_name,company_id=companyid,company_img_url=company_img_url,
                            contractor_id=element['contractor_id'],contractor_name=contractor.name)
        return product

def getproduct_fromlocationandcategory(location:str,category:str)->list[Products]:

    pr=[]
    with connection.cursor() as cursor:
        locationid=getlocationid_fromlocation(location)
        categoryid=getcategoryid_fromcategory(category)
        cursor.execute("""SELECT * FROM `products` WHERE `location_id`=%s AND `category_id`=%s""",(locationid,categoryid))
        results=cursor.fetchall()

        for element in results:
            location=getlocation_fromlocationid(element['location_id'])
            category=getcategory_fromcategoryid(element['category_id'])
            companyid=getcompanyid_fromcontractorid(element['contractor_id'])
            company_img_url=getcompanyimgurl_fromcompanyid(companyid)
            company_name=getcompanyname_fromcompanyid(companyid)
            contractor=get_contractor_by_id(element['contractor_id'])
            product=Products(p_uid=element['p_uid'],location=location,category=category,
                             product_img_url=element['product_img_url'],product_description=element['product_description'],
                             company_name=company_name,company_id=companyid,company_img_url=company_img_url,
                             contractor_id=element['contractor_id'],contractor_name=contractor.name)
            pr.append(product)

    return pr

def getproduct_fromlocation(location:str)->list[Products]:

    pr=[]
    with connection.cursor() as cursor:
        locationid=getlocationid_fromlocation(location)
        cursor.execute("""SELECT * FROM `products` WHERE `location_id`=%s""",locationid)
        results=cursor.fetchall()

        for element in results:
            location=getlocation_fromlocationid(element['location_id'])
            category=getcategory_fromcategoryid(element['category_id'])
            companyid=getcompanyid_fromcontractorid(element['contractor_id'])
            company_img_url=getcompanyimgurl_fromcompanyid(companyid)
            company_name=getcompanyname_fromcompanyid(companyid)
            contractor=get_contractor_by_id(element['contractor_id'])
            product=Products(p_uid=element['p_uid'],location=location,category=category,
                             product_img_url=element['product_img_url'],product_description=element['product_description'],
                             company_name=company_name,company_id=companyid,company_img_url=company_img_url,
                             contractor_id=element['contractor_id'],contractor_name=contractor.name)
            pr.append(product)

    return pr

def getproduct_fromcategory(category:str)->list[Products]:

    pr=[]
    with connection.cursor() as cursor:
        categoryid=getcategoryid_fromcategory(category)
        cursor.execute("""SELECT * FROM `products` WHERE `category_id`=%s""",categoryid)
        results=cursor.fetchall()

        for element in results:
            location=getlocation_fromlocationid(element['location_id'])
            category=getcategory_fromcategoryid(element['category_id'])
            companyid=getcompanyid_fromcontractorid(element['contractor_id'])
            company_img_url=getcompanyimgurl_fromcompanyid(companyid)
            company_name=getcompanyname_fromcompanyid(companyid)
            contractor=get_contractor_by_id(element['contractor_id'])
            product=Products(p_uid=element['p_uid'],location=location,category=category,
                             product_img_url=element['product_img_url'],product_description=element['product_description'],
                             company_name=company_name,company_id=companyid,company_img_url=company_img_url,
                             contractor_id=element['contractor_id'],contractor_name=contractor.name)
            pr.append(product)

    return pr

#ORDERS
def add_orders(order:Orders) -> None:
    with connection.cursor() as cursor:
        query="""INSERT INTO orders(cus_uid,order_date_time,p_uid,message) VALUES (%s,%s,%s,%s)"""
        values=(order.cus_uid,order.order_date_time,order.p_uid,order.message)
        cursor.execute(query,values)
        connection.commit()
        order.id=str(cursor.lastrowid)

def getorders_fromcusid(cusid:str):

    od=[]
    with connection.cursor() as cursor:
        cursor.execute("""SELECT * FROM `orders` WHERE `cus_uid`=%s""",cusid)
        results=cursor.fetchall()
        for element in results:
            puid = element['p_uid']
            cursor.execute("""SELECT `location_id` FROM `products` WHERE `p_uid`=%s""",puid)
            result = cursor.fetchone()
            locid = result['location_id']
            cursor.execute("""SELECT `category_id` FROM `products` WHERE `p_uid`=%s""",puid)
            result = cursor.fetchone()
            catid = result['category_id']
            cursor.execute("""SELECT `name` FROM `locations` WHERE `id`=%s""",locid)
            location = (cursor.fetchone())['name']
            cursor.execute("""SELECT `name` FROM `categories` WHERE `id`=%s""",catid)
            category=(cursor.fetchone())['name']

            productimgurl=getproductimgurl_frompuid(element['p_uid'])
            contractorid=getcontractorid_frompuid(element['p_uid'])
            companyid=getcompanyid_fromcontractorid(contractorid)
            companyname=getcompanyname_fromcompanyid(companyid)
            companyimgurl=getcompanyimgurl_fromcompanyid(companyid)

            order={"id":element['id'],"cus_uid":element['cus_uid'],"order_date_time":element['order_date_time'],
                        "p_uid":element['p_uid'],"product_img_url":productimgurl,"company_name":companyname,
                        "company_img_url":companyimgurl,"message":element['message'],"location":location,"category":category,
                        "contractor_id":contractorid,"company_id":companyid}
            
            
            od.append(order)

    return od

def getorder_fromid(orderid:str)->Optional[Orders]:

    with connection.cursor() as cursor:
        cursor.execute("""SELECT * FROM `orders` WHERE `id`=%s""",orderid)
        element=cursor.fetchone()

        if(not element):
            raise NameError
        
        productimgurl=getproductimgurl_frompuid(element['p_uid'])
        contractorid=getcontractorid_frompuid(element['p_uid'])
        companyid=getcompanyid_fromcontractorid(contractorid)
        companyname=getcompanyname_fromcompanyid(companyid)
        companyimgurl=getcompanyimgurl_fromcompanyid(companyid)

        order=Orders(id=element['id'],cus_uid=element['cus_uid'],order_date_time=element['order_date_time'],
                    p_uid=element['p_uid'],product_img_url=productimgurl,company_name=companyname,
                    company_img_url=companyimgurl,message=element['message'])
    
        return order    

 #REVIEWS
def add_reviews(review:Reviews) -> None:
    with connection.cursor() as cursor:

        query="""INSERT INTO reviews(cus_uid,p_uid,review) VALUES (%s,%s,%s)"""
        values=(review.cus_uid,review.p_uid,review.review)
        cursor.execute(query,values)
        connection.commit()
        review.id=str(cursor.lastrowid)       
        
def getreviews_frompuid(puid:str)->list[Reviews]:

    rw=[]
    with connection.cursor() as cursor:
        cursor.execute("""SELECT * FROM `reviews` WHERE `p_uid`=%s""",puid)
        results=cursor.fetchall()
        for element in results:
                customer=get_customer_by_id(element['cus_uid'])
                review=Reviews(name=customer.name,id=element['id'],cus_uid=element['cus_uid'],p_uid=element['p_uid'],review=element['review'])
                rw.append(review)
    return rw

def deletereviews_fromreviewid(reviewid:str)->Optional[Reviews]:

    with connection.cursor() as cursor:
        cursor.execute("""DELETE FROM `reviews` WHERE `id`=%s""",reviewid)
        connection.commit()
