import os
current_directory = os.getcwd()
current_directory=current_directory+"/static/"
final_directory = os.path.join(current_directory, 'ne_folder')
if not os.path.exists(final_directory):
   os.makedirs(final_directory)