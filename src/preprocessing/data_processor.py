#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

class DataProcessor:
  """
  Clase para el preprocesamiento de datos de ciberataques.
  
  Esta clase implementa métodos para cargar, limpiar y transformar datos
  relacionados con ciberataques para su uso en modelos de machine learning.
  """
  
  def __init__(self):
    """
    Inicializa el procesador de datos.
    """
    self.numeric_transformer = None
    self.categorical_transformer = None
    self.preprocessor = None
    self.numeric_features = None
    self.categorical_features = None
  
  def fit_transform(self, df, target_col='attack'):
    """
    Ajusta los transformadores y transforma los datos.
    
    Args:
      df: DataFrame con los datos a procesar
      target_col: Nombre de la columna objetivo
      
    Returns:
      X_transformed: Características transformadas
      y: Variable objetivo
    """
    # Separamos características y variable objetivo
    X = df.drop(columns=[target_col], errors='ignore')
    y = df[target_col] if target_col in df.columns else None
    
    # Identificamos columnas numéricas y categóricas
    self.numeric_features = X.select_dtypes(include=['int64', 'float64']).columns
    self.categorical_features = X.select_dtypes(include=['object', 'category']).columns
    
    # Creamos transformadores para cada tipo de columna
    self.numeric_transformer = Pipeline(steps=[
      ('imputer', SimpleImputer(strategy='median')),
      ('scaler', StandardScaler())
    ])
    
    self.categorical_transformer = Pipeline(steps=[
      ('imputer', SimpleImputer(strategy='most_frequent')),
      ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])
    
    # Combinamos transformadores en un preprocesador
    self.preprocessor = ColumnTransformer(
      transformers=[
        ('num', self.numeric_transformer, self.numeric_features),
        ('cat', self.categorical_transformer, self.categorical_features)
      ])
    
    # Ajustamos y transformamos los datos
    X_transformed = self.preprocessor.fit_transform(X)
    
    return X_transformed, y
  
  def transform(self, df):
    """
    Transforma nuevos datos utilizando los transformadores ajustados.
    
    Args:
      df: DataFrame con los datos a transformar
      
    Returns:
      X_transformed: Características transformadas
    """
    if self.preprocessor is None:
      raise ValueError("El preprocesador no ha sido ajustado. Llama a fit_transform primero.")
    
    # Transformamos los datos
    X_transformed = self.preprocessor.transform(df)
    
    return X_transformed
  
  def generate_synthetic_data(self, n_samples=1000):
    """
    Genera datos sintéticos para simular características de ciberataques.
    
    Args:
      n_samples: Número de muestras a generar
      
    Returns:
      DataFrame con datos sintéticos
    """
    # Características simuladas de tráfico de red
    np.random.seed(42)
    
    # Generamos características que podrían ser relevantes para detectar ciberataques
    data = {
      'packet_rate': np.random.exponential(scale=100, size=n_samples),  # Tasa de paquetes por segundo
      'avg_packet_size': np.random.normal(loc=500, scale=150, size=n_samples),  # Tamaño promedio de paquetes
      'connection_duration': np.random.exponential(scale=30, size=n_samples),  # Duración de conexión en segundos
      'port_number': np.random.randint(1, 65536, size=n_samples),  # Número de puerto
      'protocol_type': np.random.choice(['TCP', 'UDP', 'ICMP'], size=n_samples, p=[0.7, 0.2, 0.1]),  # Tipo de protocolo
      'src_bytes': np.random.exponential(scale=1000, size=n_samples),  # Bytes enviados desde origen
      'dst_bytes': np.random.exponential(scale=2000, size=n_samples),  # Bytes enviados desde destino
      'login_attempts': np.random.poisson(lam=0.5, size=n_samples),  # Intentos de inicio de sesión
      'num_failed_logins': np.random.poisson(lam=0.2, size=n_samples),  # Número de inicios de sesión fallidos
      'num_compromised': np.random.poisson(lam=0.1, size=n_samples),  # Número de condiciones comprometidas
      'root_shell': np.random.binomial(1, 0.05, size=n_samples),  # Si se obtuvo shell de root
      'num_root': np.random.poisson(lam=0.1, size=n_samples),  # Número de accesos root
      'num_file_creations': np.random.poisson(lam=1, size=n_samples),  # Número de operaciones de creación de archivos
      'num_shells': np.random.poisson(lam=0.01, size=n_samples),  # Número de prompts de shell
      'num_access_files': np.random.poisson(lam=0.5, size=n_samples),  # Número de operaciones en archivos de control de acceso
      'count': np.random.poisson(lam=5, size=n_samples),  # Número de conexiones al mismo host
      'srv_count': np.random.poisson(lam=3, size=n_samples),  # Número de conexiones al mismo servicio
      'serror_rate': np.random.beta(0.5, 10, size=n_samples),  # Porcentaje de conexiones con errores SYN
      'srv_serror_rate': np.random.beta(0.5, 10, size=n_samples),  # Porcentaje de conexiones con errores SYN al mismo servicio
      'rerror_rate': np.random.beta(0.5, 10, size=n_samples),  # Porcentaje de conexiones con errores REJ
      'srv_rerror_rate': np.random.beta(0.5, 10, size=n_samples),  # Porcentaje de conexiones con errores REJ al mismo servicio
      'same_srv_rate': np.random.beta(5, 1, size=n_samples),  # Porcentaje de conexiones al mismo servicio
      'diff_srv_rate': np.random.beta(1, 5, size=n_samples),  # Porcentaje de conexiones a diferentes servicios
      'dst_host_count': np.random.poisson(lam=10, size=n_samples),  # Número de conexiones al mismo host destino
      'dst_host_srv_count': np.random.poisson(lam=8, size=n_samples)  # Número de conexiones al mismo servicio destino
    }
    
    # Creamos el DataFrame
    df = pd.DataFrame(data)
    
    # Convertimos protocol_type a variables dummy
    df = pd.get_dummies(df, columns=['protocol_type'], drop_first=True)
    
    # Generamos la variable objetivo (ataque o no ataque)
    # Usamos una combinación de características para determinar si es un ataque
    prob_attack = (0.01 + 
                  0.1 * (df['serror_rate'] > 0.2) + 
                  0.1 * (df['rerror_rate'] > 0.2) + 
                  0.1 * (df['num_failed_logins'] > 0) + 
                  0.2 * (df['num_compromised'] > 0) + 
                  0.2 * (df['root_shell'] > 0) + 
                  0.1 * (df['num_root'] > 0) + 
                  0.1 * (df['num_shells'] > 0) + 
                  0.05 * (df['packet_rate'] > 300))
    
    df['attack'] = np.random.binomial(1, prob_attack)
    
    # Añadimos algunos tipos de ataques para los casos positivos
    attack_types = ['DoS', 'Probe', 'R2L', 'U2R']
    df['attack_type'] = 'normal'
    attack_mask = df['attack'] == 1
    df.loc[attack_mask, 'attack_type'] = np.random.choice(attack_types, size=attack_mask.sum())
    
    return df
  
  def load_data(self, file_path):
    """
    Carga datos desde un archivo.
    
    Args:
      file_path: Ruta al archivo de datos
      
    Returns:
      DataFrame con los datos cargados
    """
    # Determinamos el formato del archivo por su extensión
    if file_path.endswith('.csv'):
      df = pd.read_csv(file_path)
    elif file_path.endswith('.parquet'):
      df = pd.read_parquet(file_path)
    elif file_path.endswith('.json'):
      df = pd.read_json(file_path)
    else:
      raise ValueError(f"Formato de archivo no soportado: {file_path}")
    
    return df
  
  def save_processed_data(self, X, y, file_path):
    """
    Guarda los datos procesados en un archivo.
    
    Args:
      X: Características procesadas
      y: Variable objetivo
      file_path: Ruta donde guardar los datos
    """
    # Convertimos X a DataFrame si es una matriz dispersa
    if hasattr(X, "toarray"):
      X_df = pd.DataFrame(X.toarray())
    else:
      X_df = pd.DataFrame(X)
    
    # Añadimos la variable objetivo
    if y is not None:
      X_df['target'] = y
    
    # Guardamos según la extensión del archivo
    if file_path.endswith('.csv'):
      X_df.to_csv(file_path, index=False)
    elif file_path.endswith('.parquet'):
      X_df.to_parquet(file_path, index=False)
    else:
      X_df.to_csv(file_path + '.csv', index=False)