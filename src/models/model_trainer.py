#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, roc_auc_score
import matplotlib.pyplot as plt
import seaborn as sns

class ModelTrainer:
  """
  Clase para el entrenamiento y evaluación de modelos de predicción de ciberataques.
  
  Esta clase implementa métodos para entrenar, evaluar y guardar modelos
  de machine learning para la predicción de ciberataques.
  """
  
  def __init__(self, random_state=42):
    """
    Inicializa el entrenador de modelos.
    
    Args:
      random_state: Semilla para reproducibilidad
    """
    self.random_state = random_state
    self.models = {
      'random_forest': RandomForestClassifier(random_state=random_state),
      'gradient_boosting': GradientBoostingClassifier(random_state=random_state),
      'logistic_regression': LogisticRegression(random_state=random_state, max_iter=1000)
    }
    self.best_model = None
    self.best_model_name = None
    self.feature_importances = None
  
  def train_test_split(self, X, y, test_size=0.3):
    """
    Divide los datos en conjuntos de entrenamiento y prueba.
    
    Args:
      X: Características
      y: Variable objetivo
      test_size: Proporción del conjunto de prueba
      
    Returns:
      X_train, X_test, y_train, y_test: Conjuntos de entrenamiento y prueba
    """
    X_train, X_test, y_train, y_test = train_test_split(
      X, y, test_size=test_size, random_state=self.random_state, stratify=y
    )
    return X_train, X_test, y_train, y_test
  
  def train_models(self, X_train, y_train):
    """
    Entrena varios modelos y selecciona el mejor.
    
    Args:
      X_train: Características de entrenamiento
      y_train: Variable objetivo de entrenamiento
      
    Returns:
      best_model: El mejor modelo entrenado
      best_model_name: Nombre del mejor modelo
    """
    results = {}
    
    for name, model in self.models.items():
      print(f"Entrenando modelo: {name}")
      model.fit(X_train, y_train)
      y_pred = model.predict(X_train)
      accuracy = accuracy_score(y_train, y_pred)
      results[name] = {
        'model': model,
        'accuracy': accuracy
      }
      print(f"  Accuracy en entrenamiento: {accuracy:.4f}")
    
    # Seleccionamos el mejor modelo basado en accuracy
    self.best_model_name = max(results, key=lambda k: results[k]['accuracy'])
    self.best_model = results[self.best_model_name]['model']
    
    # Guardamos las importancias de características si el modelo las tiene
    if hasattr(self.best_model, 'feature_importances_'):
      self.feature_importances = self.best_model.feature_importances_
    
    return self.best_model, self.best_model_name
  
  def optimize_hyperparameters(self, X_train, y_train, model_name=None):
    """
    Optimiza los hiperparámetros del modelo seleccionado.
    
    Args:
      X_train: Características de entrenamiento
      y_train: Variable objetivo de entrenamiento
      model_name: Nombre del modelo a optimizar (si es None, se usa el mejor modelo)
      
    Returns:
      best_model: Modelo optimizado
    """
    if model_name is None:
      if self.best_model_name is None:
        raise ValueError("No se ha seleccionado un modelo. Entrena los modelos primero.")
      model_name = self.best_model_name
    
    if model_name not in self.models:
      raise ValueError(f"Modelo no encontrado: {model_name}")
    
    # Definimos los hiperparámetros a optimizar según el modelo
    param_grids = {
      'random_forest': {
        'n_estimators': [100, 200, 300],
        'max_depth': [None, 10, 20, 30],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4]
      },
      'gradient_boosting': {
        'n_estimators': [100, 200, 300],
        'learning_rate': [0.01, 0.1, 0.2],
        'max_depth': [3, 5, 7],
        'min_samples_split': [2, 5, 10]
      },
      'logistic_regression': {
        'C': [0.001, 0.01, 0.1, 1, 10, 100],
        'penalty': ['l1', 'l2'],
        'solver': ['liblinear', 'saga']
      }
    }
    
    print(f"Optimizando hiperparámetros para: {model_name}")
    
    # Creamos una instancia del modelo
    model = self.models[model_name]
    
    # Configuramos la búsqueda de hiperparámetros
    grid_search = GridSearchCV(
      estimator=model,
      param_grid=param_grids[model_name],
      cv=5,
      scoring='accuracy',
      n_jobs=-1,
      verbose=1
    )
    
    # Ejecutamos la búsqueda
    grid_search.fit(X_train, y_train)
    
    # Actualizamos el mejor modelo
    self.best_model = grid_search.best_estimator_
    self.best_model_name = model_name
    
    print(f"Mejores hiperparámetros: {grid_search.best_params_}")
    print(f"Mejor accuracy CV: {grid_search.best_score_:.4f}")
    
    # Actualizamos las importancias de características si el modelo las tiene
    if hasattr(self.best_model, 'feature_importances_'):
      self.feature_importances = self.best_model.feature_importances_
    
    return self.best_model
  
  def evaluate_model(self, X_test, y_test, model=None):
    """
    Evalúa el rendimiento del modelo en el conjunto de prueba.
    
    Args:
      X_test: Características de prueba
      y_test: Variable objetivo de prueba
      model: Modelo a evaluar (si es None, se usa el mejor modelo)
      
    Returns:
      metrics: Diccionario con métricas de rendimiento
    """
    if model is None:
      if self.best_model is None:
        raise ValueError("No se ha seleccionado un modelo. Entrena los modelos primero.")
      model = self.best_model
    
    # Realizamos predicciones
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1] if hasattr(model, 'predict_proba') else None
    
    # Calculamos métricas
    metrics = {
      'accuracy': accuracy_score(y_test, y_pred),
      'classification_report': classification_report(y_test, y_pred),
      'confusion_matrix': confusion_matrix(y_test, y_pred)
    }
    
    if y_prob is not None:
      metrics['roc_auc'] = roc_auc_score(y_test, y_prob)
    
    # Imprimimos resultados
    print(f"Accuracy: {metrics['accuracy']:.4f}")
    if 'roc_auc' in metrics:
      print(f"ROC AUC: {metrics['roc_auc']:.4f}")
    print("\nInforme de clasificación:")
    print(metrics['classification_report'])
    
    # Visualizamos la matriz de confusión
    plt.figure(figsize=(8, 6))
    sns.heatmap(metrics['confusion_matrix'], annot=True, fmt='d', cmap='Blues', cbar=False)
    plt.title('Matriz de Confusión')
    plt.xlabel('Predicción')
    plt.ylabel('Valor Real')
    plt.show()
    
    return metrics
  
  def plot_feature_importance(self, feature_names=None):
    """
    Visualiza la importancia de las características.
    
    Args:
      feature_names: Lista con los nombres de las características
    """
    if self.feature_importances is None:
      print("Este modelo no proporciona importancia de características.")
      return
    
    if feature_names is None:
      feature_names = [f"Feature {i}" for i in range(len(self.feature_importances))]
    
    # Creamos un DataFrame para visualización
    importance_df = pd.DataFrame({
      'Feature': feature_names,
      'Importance': self.feature_importances
    })
    
    # Ordenamos por importancia
    importance_df = importance_df.sort_values('Importance', ascending=False)
    
    # Visualizamos
    plt.figure(figsize=(10, 8))
    sns.barplot(x='Importance', y='Feature', data=importance_df.head(20))
    plt.title('Importancia de Características')
    plt.tight_layout()
    plt.show()
  
  def save_model(self, file_path):
    """
    Guarda el modelo en un archivo.
    
    Args:
      file_path: Ruta donde guardar el modelo
    """
    if self.best_model is None:
      raise ValueError("No hay un modelo para guardar. Entrena un modelo primero.")
    
    # Guardamos el modelo
    joblib.dump(self.best_model, file_path)
    print(f"Modelo guardado en: {file_path}")
  
  def load_model(self, file_path):
    """
    Carga un modelo desde un archivo.
    
    Args:
      file_path: Ruta del archivo del modelo
      
    Returns:
      model: Modelo cargado
    """
    # Cargamos el modelo
    self.best_model = joblib.load(file_path)
    print(f"Modelo cargado desde: {file_path}")
    return self.best_model