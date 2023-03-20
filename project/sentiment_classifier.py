# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 20:53:21 2020

@author: artem
"""
import pickle


class LogRegTfidfClf(object):
    def __init__(self):
        try:
            self.model = pickle.load(open("clf_LR.sav", 'rb'))  #подгрузка модели
        except:
            print('Load error!')
        
    @staticmethod
    def check_lang(text):#проверяет язык и корректность отзыва в первом приближении
        return any(ord(c) > 128 for c in text)
         	
    
    def predict_class(self, text):#предсказание класса
        try:
            return self.model.predict([text])
                 
        except:
            print("prediction error")
            return -1
    
    
    def predict_prob(self, text):#предсказание вероятности класса
        try:
            return self.model.predict_proba([text])
                 
        except:
            print("prediction error")
            return [0,0]
        
    #Основной метод, проверяет язык, предсказывает класс и вероятность класса, выдает сообщение    
    def get_prediction_message(self, text):
        if not self.check_lang(text):
            prediction_message = 'Введите корректный отзыв!'
            return prediction_message
        
               
        try:
            class_label = self.predict_class(text)
            probability = self.predict_prob(text)
            if class_label==1:
                prediction_message = 'Отзыв положительный с вероятностью: '+\
                str(round(probability[0,1]*100,2))+' %'
            else:        
                prediction_message = 'Отзыв отрицательный с вероятностью: '+\
                str(round(probability[0,0]*100,2))+' %'
            return prediction_message
        
        except:
            print('Произошла ошибка в работе модели')
            prediction_message = 'произошла ошибка в работе приложения, проверьте модель!'            
            return prediction_message