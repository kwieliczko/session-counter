from builtins import staticmethod


class GeneralFunctions():
    
    
    @staticmethod
    def print_error(error_message, optional_variable=""):
        print("\n\n**********************************************")
        print("***   ", error_message, optional_variable)
        print("**********************************************\n\n")
        
    
    
    
    # Calculates the percentage of the current number of connections for a given snapshot in the context 
	# of the maximum and minimum number of connections
    @staticmethod
    def calculate_percentages(current_connections, min_connenctions, max_connenctions):
            return (current_connections - min_connenctions)/(max_connenctions-min_connenctions)*100
    
    
    
    
    @staticmethod
    def choose_color(current_connections, min_connenctions, max_connenctions):
        
        precentage = GeneralFunctions.calculate_percentages(current_connections, min_connenctions, max_connenctions)
        
		
        if precentage  >= 90:
            foreground_cell_color = '69bc6e'
        elif precentage <= 90 and precentage >= 80:
            foreground_cell_color = '8cca8b'
        elif precentage <= 80 and precentage >= 70:
            foreground_cell_color = '9ed2a2'
        elif precentage <= 70 and precentage >= 60:
            foreground_cell_color = 'cbe5c8'
        elif precentage <= 60 and precentage >= 50:
            foreground_cell_color = 'e6f3e2'
        elif precentage <= 50 and precentage >= 40:
            foreground_cell_color = 'e9f7ea'
        elif precentage <= 40 and precentage >= 30:
            foreground_cell_color = 'f2f7f0'
        elif precentage <= 30 and precentage >= 20:
            foreground_cell_color = 'f5fcf5'
        elif precentage <= 20 and precentage >= 10:
            foreground_cell_color = 'f6fdf8'
        elif precentage <= 10 and precentage >= 0:
            foreground_cell_color = 'ffffff'


        return foreground_cell_color
        