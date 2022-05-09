# -*- coding: utf-8 -*-
"""
Created on Mon May  7 11:14:57 2022

@author: Cesar Skarbnik
"""

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from ColorLabel import ColorLabel
from kivy.uix.textinput import TextInput
import json
import pymysql.cursors

def byte2Per(nbyte):
	return nbyte*(1/255)


class Acceso(App):
    def botonok_press(self,obj):
        if self.connection:
            nick = self.inputUsuario.text
            password = self.inputUsuario.text
            Mi_cursor = self.connection.cursor()
            #SQL a ejecutar
            SQL = 'Select * from usuario where nick = %s and password = sha2(%s,256)'
            #Print Sql
            Mi_cursor.execute(SQL,[nick,password])
            Resultado = Mi_cursor.fetchone()
            if Resultado:
                self.columna2.text = 'Acceso concedido'
                print('Acceso concedido')
            else:self.columna2.text = 'Acceso denegado'
            print('Acceso denegado')
        else:
            print('Error')
    def iniciarBD(self):
        self.conf= None
        with open('db.json') as jsonfile:
            self.conf = json.load(jsonfile)
            
        self.connection = pymysql.connect(
            host=self.conf['HOST'], user=self.conf['DBUSR'],
            password=self.conf['DBPASS'], database=self.conf['DBNAME'],
            charset='utf8mb4', port=self.conf['PORT']
            )
        
    def build(self):
		# Vamos a definir un layout
        self.gdl_principal = GridLayout(cols=3)
        self.gdl_medio = GridLayout(rows =5)
		############################################
        self.labelusuario = ColorLabel(text='Usuario')
        self.labelusuario.background_color=[1,0,0,1]
        self.inputUsuario = TextInput(text='', multiline =False)
        self.labelpassword = ColorLabel(text='Contraseña')
        self.labelpassword.background_color=[1,0,0,1]
        self.inputpassword = TextInput(text='', password =True,multiline=False)
        self.botonok = Button(text='Accesar')
        self.botonok.background_color=[0,0,0,1]
        
		############################################
        self.gdl_medio.add_widget(self.labelusuario)
        self.gdl_medio.add_widget(self.inputUsuario)
        self.gdl_medio.add_widget(self.labelpassword)
        self.gdl_medio.add_widget(self.inputpassword)
        self.gdl_medio.add_widget(self.botonok)
        #############################################
        self.botonok.bind(on_press=self.botonok_press)
        ###############################################
        columna1=ColorLabel(text='')
        columna1.background_color=[0.5,0.7,1,1]
        self.columna2=ColorLabel(text='')
        self.columna2.background_color=[0.5,0.7,1,1]
        self.gdl_principal.add_widget(columna1)
        self.gdl_principal.add_widget(self.gdl_medio)
        self.gdl_principal.add_widget(self.columna2)
        return self.gdl_principal
        

if __name__ == '__main__':
    SQLApp = Acceso()
    SQLApp.iniciarBD()
    SQLApp.run()
    #Esto ejecuta el ent
