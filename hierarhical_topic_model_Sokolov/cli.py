#!/usr/bin/python
import optparse
import sys, os
import artm
import menu
from matplotlib import pyplot as plt
#from collections import Counter
#import tempfile
#import pickle
#import codecs


artm.version()

num_document_passes = 10
num_collection_passes = 40
regularizer_tau = 10 ** 5
parent_level_weight = 1
num_topics_level0 = 25
num_topics_level1 = 60


# Main definition - constants
menu_actions  = {} 


#batch_vectorizer = artm.BatchVectorizer(data_path='train.vw',
#                                        data_format='vowpal_wabbit',
#                                        target_folder='my_collection_batches',
#                                        gather_dictionary=False)

#my_dictionary = artm.Dictionary()
#my_dictionary.gather(data_path='my_collection_batches')
#my_dictionary.filter(min_df_rate=0.01, max_df_rate=30)


#model_Hartm = artm.hARTM(dictionary=my_dictionary,
#                            cache_theta=True,
#                            num_document_passes=num_document_passes,
#                            theta_columns_naming='title').load("hierarhical_model")
                            
#model_Hartm = artm.hARTM().load                         
#model_Hartm.save("hierarhical_model")


print("Everything is ok")


def main_menu():
    mainMenu = menu.Menu("Interactive Topic Model")
    
    mainMenu.explicit()
    options = [{"name":"Base Model","function":topicModel},
           {"name":"Hierarhical Model","function":hTopicModel},
           {"name":"Quit","function":exit}]
    mainMenu.addOptions(options)
    
    mainMenu.open()
    return

# Menu for basic
def topicModel():
    return
 
def topicModelBuilding():
    os.system('clear')
    return
    
def topicModelView():
    os.system('clear')
    return
    
# Menu for hierarhical
def hTopicModel():
    hTopicModelMenu = menu.Menu("Hierarhical Topic Model Menu")
    
    options = [{"name":"Use prebuild model","function":hTopicModelView},
           {"name":"Build New Model","function":hModelBuilding},
           {"name":"Back Menu","function":main_menu},
           {"name":"Quit","function":exit}]
    hTopicModelMenu.addOptions(options)
    hTopicModelMenu.open()
    return  

def hModelBuilding():
    return

def hTopicModelView():
    os.system('clear')
    print "Wait for dictionary loading\t\t\t",
    batch_vectorizer = artm.BatchVectorizer(data_path='train.vw',
                                        data_format='vowpal_wabbit',
                                        target_folder='my_collection_batches',
                                        gather_dictionary=False)

    my_dictionary = artm.Dictionary()
    my_dictionary.gather(data_path='my_collection_batches')
    my_dictionary.filter(min_df_rate=0.01, max_df_rate=30)
    
    print "OK"
    
    print "Wait for model loading\t\t\t",
    model_Hartm = artm.hARTM(dictionary=my_dictionary,
                            cache_theta=True,
                            num_document_passes=num_document_passes,
                            theta_columns_naming='title')
    model_Hartm.load("hierarhical_model")

    print "OK"

    print("Current hierarhical model properties:")
    print("Number of levels: " + str(model_Hartm.num_levels))
    
    for num in range(0,model_Hartm.num_levels):
        print("Level " + str(num) + " info:")
        #print('Level ' + str(num+1) + ': ')
        phi = model_Hartm[num].get_phi()
        print("Doc/Topics matrix size: " + str(phi.shape))
        #theta = model_Hartm1[num].get_theta()
        #print("Theta sizes: " + str(theta.shape))
        if num != 0:
            psi = model_Hartm[num].get_psi()
            print("Topics/Subtopics matrix size: " + str(psi.shape))
        
        
        print("--------------------------------")

    print("Choose commands for additional information retrieving.")
    #while(True):
    #    print(">>")
    
    return
# Back to main menu
def back():
    return
 
# Exit program
def exit():
    sys.exit()  
# =======================
#      MAIN PROGRAM
# =======================
 
# Main Program
if __name__ == "__main__":
    # Launch main menu
    main_menu()
