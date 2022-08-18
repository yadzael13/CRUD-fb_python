#------------------------------- CRUD con Firebase ---------------------------------
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
from http import HTTPStatus
print(HTTPStatus.INTERNAL_SERVER_ERROR.value)
# ---------------------  Create  -------------------------------------
#merge ----- añade elementos a cuerpo existente sin sobrescribir el json
#set ---- añade elemento (json)
#add --- añade documento con id automatica
db=firestore.client()
data = {'name' : "Yadzaaaa", "age" : 24}
#--Add element with auto ID
"""
db.collection("persons").add(data)
"""
#--Set for doc with ID assigned
"""
db.collection("persons").document("yod").set(data)
"""
#--Merging(to add fields in to existing data)
"""
db.collection("persons").document("yod").set({'address': 'Canada'}, merge = True)
"""
#--------------------------------------------------------------------


# ---------------------  Read  -------------------------------------
"""
result = db.collection("persons").document("yod").get()
if result.exists:
    print(result.to_dict())
    """
#- Get all
"""
docs = db.collection("persons").get()
for doc in docs:
    print(doc.to_dict())
    """
# -- Query
# -- == != < > >= <=
"""
docs = db.collection("persons").where("age", "==", 4).get()
for doc in docs:
    print(doc.to_dict())
    """
# -- array_contains
"""
docs = db.collection("persons").where("asd", "array_contains", "github").get()
for doc in docs:
    print(doc.to_dict())
    """
# -- specific query where
"""
docs = db.collection("persons").where("address", "in", ["Canada", "Mexico"]).get()
for doc in docs:
    print(doc.to_dict())
    """
#--------------------------------------------------------------------


# ---------------------  Update ------------------------------------
#-- Update data - know id
#db.collection("persons").document("yod").update({"age":12})
# -- Add new field
#db.collection("persons").document("yod").update({"address4":"Amsterdam"})
# -- delete array element (ArrayRemove)
#db.collection("persons").document("yod").update({"asd":firestore.ArrayRemove(["google"])})
# -- Adding an array element, as append (ArrayUnion)
#db.collection("persons").document("yod").update({"asd":firestore.ArrayUnion(["google"])})
#Updating dinamicly - unknow id
"""
docs = db.collection("persons").where("age", ">", 20).get()
for doc in docs:
    key = doc.id
    db.collection("persons").document(key).update({"ageGroup":"Mayor de edad"})
"""
#--------------------------------------------------------------------


# ---------------------  Delete  -----------------------------------
#-- With know id
"""
db.collection("persons").document("qwerty").delete()
"""
#-- Delete data know ID -- field
"""
db.collection("persons").document("qwerty").update("socials": firestore.DELETE_FIELD)
"""
#-- Delete docs unknow ID -
"""
docs = db.collection("persons").where("age", ">", 30).get()
for doc in docs:
    key = doc.id
    db.collection("persons").document(key).delete()
"""
#docs = db.collection("persons").get()
#--------------------------------------------------------------------
