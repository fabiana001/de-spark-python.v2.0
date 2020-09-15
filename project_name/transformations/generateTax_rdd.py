from pyspark.sql import Row


def processCustomers(r:Row,metrics)->tuple:
    Name = str(r.Name).upper()
    tax  = int(r.cost*0.15)
    return(Name,r.FirstName,r.LastName,r.Address,r.mail,r.cost,r.purchasedate,tax)