from flask import request, Blueprint, jsonify
from http import HTTPStatus
import logging

from databases.firebase import Crud
v1 = Blueprint("version1", "version1", url_prefix="/v1")
ob = Crud()
@v1.route('/get_info',methods =['GET'])
def get_info():
    try:
        col = ""
        id = request.args.get("id")
        aux = id.split("_")
        if aux[0] == "pet":
            col = "pets"
        elif aux[0] == "own":
            col = "owners"
        response ={
            f"{id}" : f"{col}",
            "data" : ob.get_info_by_id_fb(id)
        }
        return response
    except Exception as e:
        logging.error(f"""\n -------------------------------- \n
        Error en get_info, paths ---------- \n
        {e} \n --------------------------------""")
        response = {
            "message" : f"Error getting info from {id}"
        }
        return response, 500

@v1.route('/owners',methods =['GET', 'POST', 'PUT', 'DELETE'])
def owners_mets():
    if request.method == 'GET':
        try:
            response = {
                "HTTPstatus" : f"{HTTPStatus.OK.value}",
                "response" : ob.get_owners_fb()
            }
            return response
        except Exception as e:
            logging.error(f"""\n -------------------------------- \n
            Error en get_owner, paths ---------- \n
            {e} \n --------------------------------""")
            response = {
                "message" : "Error getting owners"
            }
            return response, 500
    elif request.method == 'POST':
        try:
            body = request.get_json()
            return ob.create_owner_fb(body)
        except Exception as e:
            logging.error(f"""\n -------------------------------- \n
            Error en create_owner, paths ---------- \n
            {e} \n --------------------------------""")
            response = {
                "message" : "Error creating owner"
            }
            return response, 500
    elif request.method == 'PUT':
        try:
            ret = {}
            id = request.args.get('id')
            body = request.get_json()
            ret |= ob.update_data_fb(id, body)

            return ret | {
                "HTTPstatus" : f"{HTTPStatus.OK.value}",
                "Actualization_for_id" : f"{id}",
                "new_body" : ob.get_info_by_id_fb(id)

            }
        except Exception as e:
            logging.error(f"""\n -------------------------------- \n
            Error en owners_update, paths ---------- \n
            {e} \n --------------------------------""")
            response = {
                "message" : "Error updating owners"
            }
            return response, 500
    elif request.method == "DELETE":
        try:
            id = request.args.get("id")
            ob.delete_doc_fb(id)
            return {
                "message" : f"{id} deleting suscesfully"
            }
        except Exception as e:
            logging.error(f"""\n -------------------------------- \n
            Error en Delete_owner, paths ---------- \n
            {e} \n --------------------------------""")
            response = {
                "message" : "Error getting pets"
            }
            return response, 500

@v1.route('/pets',methods =['GET','POST', 'PUT', 'DELETE'])
def pet_mets():
    if request.method == "GET":
        try:
            response = {
                "HTTPstatus" : f"{HTTPStatus.OK.value}",
                "response" : ob.get_pets_fb()
            }
            return response
        except Exception as e:
            logging.error(f"""\n -------------------------------- \n
            Error en pets_get, paths ---------- \n
            {e} \n --------------------------------""")
            response = {
                "message" : "Error getting pets"
            }
            return response, 500
    elif request.method == "POST":
        try:
            body = request.get_json()
            return ob.create_pet_fb(body)
        except Exception as e:
            logging.error(f"""\n -------------------------------- \n
            Error en pets_post, paths ---------- \n
            {e} \n --------------------------------""")
            response = {
                "message" : "Error creating pet"
            }
            return response, 500
    elif request.method == 'PUT':
        try:
            ret = {}
            id = request.args.get('id')
            body = request.get_json()
            ret |= ob.update_data_fb(id, body)

            return ret | {
                "HTTPstatus" : f"{HTTPStatus.OK.value}",
                "Actualization_for_id" : f"{id}",
                "new_body" : ob.get_info_by_id_fb(id)

            }
        except Exception as e:
            logging.error(f"""\n -------------------------------- \n
            Error en pets_update, paths ---------- \n
            {e} \n --------------------------------""")
            response = {
                "message" : "Error updating pets"
            }
            return response, 500
    elif request.method == "DELETE":
        try:
            id = request.args.get("id")
            ob.delete_doc_fb(id)
            return {
                "message" : f"{id} deleting suscesfully"
            }
        except Exception as e:
            logging.error(f"""\n -------------------------------- \n
            Error en Delete_pets, paths ---------- \n
            {e} \n --------------------------------""")
            response = {
                "message" : "Error getting pets"
            }
            return response, 500

@v1.route('/members', methods = ['GET'])
def get_members():
    try:
        return {
            "Members" : ob.get_members_fb()
            }
    except Exception as e:
        logging.error(f"""\n -------------------------------- \n
        Error en get_pet_by_owner, paths ---------- \n
        {e} \n --------------------------------""")
        response = {
            "message" : "Error getting pet by owner"
        }
        return response, 500

@v1.route('/no_members', methods = ['GET'])
def get_no_members():
    try:
        return {
            "No_Members" : ob.get_no_members_fb()
            }
    except Exception as e:
        logging.error(f"""\n -------------------------------- \n
        Error en get_pet_by_owner, paths ---------- \n
        {e} \n --------------------------------""")
        response = {
            "message" : "Error getting pet by owner"
        }
        return response, 500

@v1.route('/pet_by_owner', methods = ['GET'])
def get_pet_by_owner():
    try:
        id_own = request.args.get("id")
        return ob.get_pet_by_owner_fb(id_own)
    except Exception as e:
        logging.error(f"""\n -------------------------------- \n
        Error en get_pet_by_owner, paths ---------- \n
        {e} \n --------------------------------""")
        response = {
            "message" : "Error getting pet by owner"
        }
        return response, 500
@v1.route('/fields', methods = ['POST', 'DELETE'])
def fields_mets():
    if request.method == "POST":
        try:
            id = request.args.get("id")
            body = request.get_json()
            return ob.insert_field_fb(id, body)
        except Exception as e:
            logging.error(f"""\n -------------------------------- \n
            Error en fields_mets_insert, paths ---------- \n
            {e} \n --------------------------------""")
            response = {
                "message" : f"Error inserting field on {id}"
            }
            return response, 500
    elif request.method == "DELETE":
        try:
            field = request.args.get("del")
            id = request.args.get("id")
            ob.delete_field_fb(id, field)
            response = {
                "message" : f"'{field}' has been correctly removed from firebase'"
            }
            return response
        except Exception as e:
            logging.error(f"""\n -------------------------------- \n
            Error en fields_mets_delete, paths ---------- \n
            {e} \n --------------------------------""")
            response = {
                "message" : f"Error deleting field on {id}"
            }
            return response, 500
