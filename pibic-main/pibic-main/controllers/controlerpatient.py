import pandas as pd
from flask import Blueprint, request, jsonify
from io import BytesIO, StringIO
from pydantic import ValidationError
from entities.paciente import Paciente
from predictions.predict import predict_and_explain
from shareds.database.comands.pacienteService import *

paciente_bp = Blueprint('paciente', __name__, url_prefix='/paciente')

@paciente_bp.route("", methods=["POST"])
def create_paciente():
    try:
        data = request.get_json()
        instance = Paciente(**data)
        instance.nome = instance.nome.lower()

        prob, pred, img = predict_and_explain(
            instance.pre_hematocrit, instance.pre_hemoglobin, instance.pre_lactate, 
            instance.height,instance.redo, instance.cpb, instance.anoxia,
            instance.female, instance.normothermia
        )
        instance.probability = str(prob)
        instance.prediction = str(pred)
        insert_paciente(instance)

        return jsonify({'message': 'Paciente criado com sucesso'}), 201
    except ValidationError as e:
        return jsonify({'message': 'Erro na validação dos dados', 'error': e.errors()}), 422
    except Exception as e:
        return jsonify({'message': 'Erro ao criar paciente', 'error': str(e)}), 400

@paciente_bp.route("/getallpacientes", methods=["GET"])
def get_all_pacientes():
    try:
        pacientes = paciente_get_all()
        return jsonify({"pacientes": pacientes}), 200
    except Exception as e:
        return jsonify({'message': 'Erro ao buscar pacientes'}), 401

@paciente_bp.route("/getproballpacientes", methods=["GET"])
def get_prob_all_pacientes():
    try:
        pacientes = paciente_prob_get_all()
        return jsonify({"pacientes": pacientes}), 200
    except Exception as e:
        return jsonify({'message': 'Erro ao buscar pacientes'}), 401

@paciente_bp.route("/<cpf>", methods=["GET"])
def get_paciente(cpf):
    paciente = get_by_name_cpf(cpf)
    if paciente:
        return jsonify({"message": paciente}), 200
    return jsonify({'message': 'Paciente não encontrado'}), 404

@paciente_bp.route("/delete/<cpf>", methods=["DELETE"])
def delete_paciente(cpf):
    paciente = verificar_paciente(cpf)
    if paciente:
        delete_paciente_by_name_and_cpf(cpf)
        return jsonify({'message': 'Paciente deletado com sucesso'}), 200
    return jsonify({'message': 'Paciente não encontrado'}), 404

@paciente_bp.route("/update/<cpf>", methods=["PUT"])
def use_update_paciente(cpf):
    data = request.get_json()
    paciente = verificar_paciente(cpf)
    if not paciente:
        return jsonify({'message': 'Paciente não encontrado'}), 404

    try:
        patient_data = Paciente(**data)
        patient_data.nome = patient_data.nome.lower()
        prob, pred, img = predict_and_explain(
            patient_data.pre_hematocrit, patient_data.pre_hemoglobin,patient_data.pre_lactate, 
            patient_data.height,patient_data.redo, patient_data.cpb, patient_data.anoxia,
            patient_data.female, patient_data.normothermia
        )
        patient_data.probability = str(prob)
        patient_data.prediction = str(pred)

        return update_paciente(cpf, patient_data)
    except Exception as e:
        return jsonify({'error': "Erro ao atualizar paciente: " + str(e)}), 400

@paciente_bp.route("/upload", methods=["POST"])
def upload_pacientes():
    try:
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "Nenhum arquivo selecionado"}), 401

        file_extension = file.filename.split('.')[-1].lower()
        if file_extension == 'csv':
            file_data = file.read().decode('utf-8')
            data = pd.read_csv(StringIO(file_data))
        elif file_extension in ['xlsx', 'xls']:
            data = pd.read_excel(BytesIO(file.read()))
        else:
            return jsonify({"error": "Tipo de arquivo não suportado"}), 402

        lista_de_pacientes_n_salvos = []

        for _, row in data.iterrows():
            try:
                data_dict = {
                    "nome": str(row['nome']),
                    "cpf": str(row['cpf']),
                    "pre_hematocrit": float(row['pre_hematocrit']),
                    "pre_hemoglobin": float(row['pre_hemoglobin']),
                    "pre_lactate": float(row['pre_lactate']),
                    "height": float(row['height']),
                    "redo": int(row['redo']),
                    "cpb": float(row['cpb']),
                    "anoxia": float(row['anoxia']),
                    "female": int(row['female']),
                    "normothermia": int(row['normothermia'])
                }

                instance = Paciente(**data_dict)
                instance.nome = instance.nome.lower()

                if not verificar_paciente(instance.cpf):
                    prob, pred, img = predict_and_explain(
                        instance.pre_hematocrit, instance.pre_hemoglobin, instance.pre_lactate, 
                        instance.height,instance.redo, instance.cpb, instance.anoxia,
                        instance.female, instance.normothermia
                    )
                    instance.probability = str(prob)
                    instance.prediction = str(pred)
                    insert_paciente(instance)
                else:
                    lista_de_pacientes_n_salvos.append(data_dict)
            except Exception:
                lista_de_pacientes_n_salvos.append(data_dict)

        if len(lista_de_pacientes_n_salvos) == 0:
            return jsonify({"message": "Todos os pacientes foram salvos com sucesso"}), 200

        return jsonify({
            "message": "Parte dos pacientes foram salvos",
            "nao_salvos": lista_de_pacientes_n_salvos
        }), 207
    except Exception as e:
        return jsonify({"error": str(e)}), 400
