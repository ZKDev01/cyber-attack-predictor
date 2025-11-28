#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
import joblib
import os
import sys

# Añadimos el directorio raíz al path para importar módulos propios
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.preprocessing.data_processor import DataProcessor

app = Flask(__name__)

# Cargamos el modelo
MODEL_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../models/cyberattack_predictor_model'))

# Inicializamos el procesador de datos
data_processor = DataProcessor()

@app.route('/health', methods=['GET'])
def health_check():
  """
  Endpoint para verificar que la API está funcionando.
  """
  return jsonify({
    'status': 'ok',
    'message': 'API de predicción de ciberataques funcionando correctamente'
  })

@app.route('/predict', methods=['POST'])
def predict():
  """
  Endpoint para realizar predicciones de ciberataques.
  
  Espera recibir un JSON con las características del tráfico de red.
  """
  try:
    # Obtenemos los datos de la solicitud
    data = request.json
    
    if not data:
      return jsonify({
        'error': 'No se proporcionaron datos para la predicción'
      }), 400
    
    # Convertimos los datos a DataFrame
    if isinstance(data, list):
      # Si es una lista de registros
      df = pd.DataFrame(data)
    else:
      # Si es un solo registro
      df = pd.DataFrame([data])
    
    # Cargamos el modelo
    try:
      model = joblib.load(MODEL_PATH)
    except FileNotFoundError:
      return jsonify({
        'error': 'Modelo no encontrado. Asegúrate de haber entrenado y guardado el modelo.'
      }), 500
    
    # Preprocesamos los datos
    try:
      X = data_processor.transform(df)
    except Exception as e:
      # Si el preprocesador no está ajustado, generamos datos sintéticos para ajustarlo
      # Esto es solo para el MVP, en producción debería estar ajustado previamente
      synthetic_df = data_processor.generate_synthetic_data(n_samples=1000)
      data_processor.fit_transform(synthetic_df)
      X = data_processor.transform(df)
    
    # Realizamos la predicción
    predictions = model.predict(X)
    probabilities = model.predict_proba(X)[:, 1] if hasattr(model, 'predict_proba') else None
    
    # Preparamos la respuesta
    results = []
    for i, pred in enumerate(predictions):
      result = {
        'prediction': int(pred),
        'is_attack': bool(pred == 1),
      }
      
      if probabilities is not None:
        result['probability'] = float(probabilities[i])
      
      results.append(result)
    
    # Si solo hay un resultado, lo devolvemos directamente
    if len(results) == 1:
      return jsonify(results[0])
    
    return jsonify(results)
  
  except Exception as e:
    return jsonify({
      'error': f'Error al procesar la solicitud: {str(e)}'
    }), 500

@app.route('/generate_sample', methods=['GET'])
def generate_sample():
  """
  Endpoint para generar datos de ejemplo.
  
  Útil para probar la API.
  """
  try:
    # Generamos un registro de ejemplo
    n_samples = int(request.args.get('n', 1))
    if n_samples > 100:
      n_samples = 100  # Limitamos a 100 muestras
    
    # Generamos datos sintéticos
    df = data_processor.generate_synthetic_data(n_samples=n_samples)
    
    # Eliminamos las columnas de ataque para que el usuario solo vea las características
    sample_data = df.drop(['attack', 'attack_type'], axis=1).to_dict('records')
    
    return jsonify(sample_data)
  
  except Exception as e:
    return jsonify({
      'error': f'Error al generar datos de ejemplo: {str(e)}'
    }), 500

if __name__ == '__main__':
  # Verificamos si el modelo existe
  if not os.path.exists(MODEL_PATH):
    print(f"ADVERTENCIA: El modelo no existe en {MODEL_PATH}")
    print("Puedes entrenar el modelo ejecutando el notebook en notebooks/automl_cyberattack_prediction.ipynb")
  
  # Iniciamos la API
  app.run(debug=True, host='0.0.0.0', port=5000)