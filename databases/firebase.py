import firebase_admin
import logging
from firebase_admin import credentials
from firebase_admin import firestore
#Credenciales para modificar la db
cred = credentials.Certificate("serviceAccountKey.json")
#
firebase_admin.initialize_app(cred)
db=firestore.client()
class Crud:
    #Local funct
    def get_col(self, id):
        ret = ""
        col = id.split("_")
        if col[0] == "own":
            ret = "owners"
        elif col[0] == "pet":
            ret = "pets"
        return ret
    #Local funct
    def get_id(self, col):
        lis = []
        docs = db.collection(col).get()
        if len(docs) > 0:
            for doc in docs:
                doc_id = doc.id
                lis.append(doc_id)
            last = lis[-1]
            last = last.split("_")
            return last[0]+"_"+str(int(last[1])+1)
        else:
            aux = col[0] + col[1] + col[2]
            return aux+"_1"

    def get_info_by_id_fb(self, id):
        try:

            ret = db.collection(self.get_col(id)).document(id).get().to_dict()

            return ret
        except Exception as e:
            logging.error(f"""\n -------------------------------- \n
            Error en get_info_by_id_fb ---------- \n
            {e} \n --------------------------------""")

    def get_members_fb(self):
        try:
            ret = {}
            owners = db.collection("owners").where("member", "==", True).get()
            for own in owners:
                aux = {own.id : own.to_dict()}
                ret |= aux
            return ret
        except Exception as e:
            logging.error(f"""\n -------------------------------- \n
            Error en get_members_fb ---------- \n
            {e} \n --------------------------------""")

    def get_no_members_fb(self):
        try:
            ret = {}
            owners = db.collection("owners").where("member", "==", False).get()
            for own in owners:
                aux = {own.id : own.to_dict()}
                ret |= aux
            return ret
        except Exception as e:
            logging.error(f"""\n -------------------------------- \n
            Error en get_no_members_fb ---------- \n
            {e} \n --------------------------------""")

    def get_owners_fb(self):
        try:
            docs = db.collection("owners").stream()
            ret = {}
            for doc in docs:
                aux = {doc.id : doc.to_dict() }
                ret |= aux
            return ret
        except Exception as e:
            logging.error(f"""\n -------------------------------- \n
            Error en get_owners_fb ---------- \n
            {e} \n --------------------------------""")

    def get_pets_fb(self):
        try:
            docs = db.collection("pets").stream()
            ret = {}
            for doc in docs:
                aux = {doc.id : doc.to_dict() }
                ret |= aux
            return ret
        except Exception as e:
            logging.error(f"""\n -------------------------------- \n
            Error en get_pets_fb ---------- \n
            {e} \n --------------------------------""")

    def create_owner_fb(self, json_own):
        try:
            id_ow = self.get_id('owners')
            js = {
                "direccion": "",
                "edad": 0,
                "member": False,
                "name" : "Default"
                }
            for item in json_own:
                if item in js:
                    js[item] = json_own[item]
                else:
                    print(f"Error, {item} has not founded on owner body")
                    continue
            db.collection("owners").document(id_ow).set(js)
            response = {
                    "message" : "Operacion valida, Dueño creado"
                }
            return response
        except Exception as e:
            logging.error(f"""\n -------------------------------- \n
            Error en create_owner_fb ---------- \n
            {e} \n --------------------------------""")

    def create_pet_fb(self, json_pet):
            try:
                id_pet = self.get_id('pets')
                js = {
                    "nombre" : "",
                    "edad" : 0,
                    "especie" : "",
                    "foto" : "",
                    "owner": "",
                    "habilidades" : [],
                    "excelencia" : False
                    }
                for item in json_pet:
                    if item in js:
                        js[item] = json_pet[item]
                    else:
                        print(f"Error, {item} has not founded on pet body")
                        continue
                db.collection("pets").document(id_pet).set(js)
                response = {
                        "message" : "Operacion valida, Mascota creada"
                    }
                return response
            except Exception as e:
                logging.error(f"""\n -------------------------------- \n
                Error en create_pet_fb ---------- \n
                {e} \n --------------------------------""")

    def get_pet_by_owner_fb(self, id_own):
        try:

            docs = db.collection("pets").where("owner", "==", f"{id_own}").get()
            ret = {}
            for doc in docs:

                aux ={
                    f"{doc.id}" : f"{doc.to_dict()['nombre']}"
                    }
                ret |= aux
            return {
                f"{id_own}" : ret
            }
        except Exception as e:
            logging.error(f"""\n -------------------------------- \n
            Error en get_pet_by_owner_fb ---------- \n
            {e} \n --------------------------------""")

    def update_data_fb(self, id, body):
        try:
            resp = {}
            info = self.get_info_by_id_fb(id)
            col = self.get_col(id)

            for el in body:
                if el in info:
                    db.collection(col).document(id).update({el: body[el]})
                    resp |= {f"{el}": f"correctly updated on {id}"}
                else:
                    resp |= {f"{el}": f"does not exist on {id}"}
                    continue
            return {
                "status" : resp
            }
        except Exception as e:
            logging.error(f"""\n -------------------------------- \n
            Error en update_data_fb ---------- \n
            {e} \n --------------------------------""")

    def insert_field_fb(self, id, body):
        try:
            col = self.get_col(id)
            db.collection(col).document(id).update(body)
            ret = {"status" : f"field updating succesfully on id: {id} from {col}"}
            return ret
        except Exception as e:
                logging.error(f"""\n -------------------------------- \n
                Error en insert_field_fb ---------- \n
                {e} \n --------------------------------""")

    def delete_doc_fb(self, id):
        try:
            col = self.get_col(id)
            db.collection(col).document(id).delete()
        except Exception as e:
                logging.error(f"""\n -------------------------------- \n
                Error en delete_doc_fb ---------- \n
                {e} \n --------------------------------""")

    def delete_field_fb(self, id, field):
        try:
            col = self.get_col(id)
            db.collection(col).document(id).update({field : firestore.DELETE_FIELD})
        except Exception as e:
                logging.error(f"""\n -------------------------------- \n
                Error en delete_field_fb ---------- \n
                {e} \n --------------------------------""")
